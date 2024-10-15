"""Ticketing Connector Model"""

import base64
import os
import tempfile
from typing import Any, Optional, Tuple

import rich.progress
from pathlib import Path
from pydantic import ConfigDict
from synqly import engine
from synqly.engine.resources.ticketing.types.ticket import Ticket

from regscale.core.app.utils.app_utils import (
    check_file_path,
    compute_hashes_in_directory,
    error_and_exit,
    get_current_datetime,
)
from regscale.integrations.commercial.synqly.synqly_model import SynqlyModel
from regscale.models.integration_models.synqly_models.tenants import Tenant
from regscale.models.regscale_models import File, Issue


class Ticketing(SynqlyModel):
    """Ticketing Connector Model"""

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True, arbitrary_types_allowed=True)

    integration_id_field: str = ""
    has_integration_field: bool = False
    update_issues: list = []
    new_regscale_issues: list = []
    update_counter: list = []
    integration_config: Any = None

    def __init__(self, integration: str, **kwargs: dict):
        super().__init__(connector_type=self.__class__.__name__, integration=integration, **kwargs)
        self.integration_id_field = f"{self.integration[0].lower()}{self.integration[1:]}Id"
        self.has_integration_field = hasattr(Issue(), self.integration_id_field)
        self.logger.debug(f"{self._connector_type} connector for {integration} initialized.")

    def download_issue_attachments_to_directory(
        self,
        directory: str,
        integration_issue: Ticket,
        regscale_issue: Issue,
    ) -> tuple[str, str]:
        """
        Function to download attachments from the integration via Synqly and RegScale issues to a directory

        :param str directory: Directory to store the files in
        :param Ticket integration_issue: Issue to download the attachments for
        :param Issue regscale_issue: RegScale issue to download the attachments for
        :return: Tuple of strings containing the Integration and RegScale directories
        :rtype: tuple[str, str]
        """
        # determine which attachments need to be uploaded to prevent duplicates by checking hashes
        synqly_dir = os.path.join(directory, self.integration)
        check_file_path(synqly_dir, False)
        # download all attachments from Integration via Synqly to the synqly directory in temp_dir
        self.download_attachments(ticket_id=integration_issue.id, download_dir=synqly_dir)
        # get the regscale issue attachments
        regscale_issue_attachments = File.get_files_for_parent_from_regscale(
            api=self.api,
            parent_id=regscale_issue.id,
            parent_module="issues",
        )
        # create a directory for the regscale attachments
        regscale_dir = os.path.join(directory, "regscale")
        check_file_path(regscale_dir, False)
        # download regscale attachments to the directory
        for attachment in regscale_issue_attachments:
            with open(os.path.join(regscale_dir, attachment.trustedDisplayName), "wb") as file:
                file.write(
                    File.download_file_from_regscale_to_memory(
                        api=self.api,
                        record_id=regscale_issue.id,
                        module="issues",
                        stored_name=attachment.trustedStorageName,
                        file_hash=(attachment.fileHash if attachment.fileHash else attachment.shaHash),
                    )
                )
        return synqly_dir, regscale_dir

    def download_attachments(self, ticket_id: str, download_dir: str) -> int:
        """
        Downloads attachments from a ticket via Synqly

        :param str ticket_id: Ticket ID to download attachments from
        :param str download_dir: Directory to download attachments to
        :return: # of Synqly attachments downloaded
        :rtype: int
        """
        attachments = self.client.ticketing.list_attachments_metadata(ticket_id)
        self.logger.debug("Found %i attachments for ticket %s", len(attachments.result), ticket_id)
        for attachment in attachments.result:
            download_response = self.client.ticketing.download_attachment(
                ticket_id=ticket_id, attachment_id=attachment.id
            )
            output_path = os.path.join(download_dir, attachment.file_name)
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(download_response.result.content))
            self.logger.debug(
                "Downloaded attachment: %s and wrote its contents to %s",
                download_response.result.file_name,
                attachment.file_name,
            )
        return len(attachments.result)

    def upload_synqly_attachments(self, ticket_id: str, file_path: Path) -> None:
        """
        Uploads an attachment to a ticket via Synqly

        :param str ticket_id: Ticket ID to attach the file to
        :param Path file_path: Path to the file to attach
        :rtype: None
        """
        with open(file_path.absolute(), "rb") as file:
            content = base64.b64encode(file.read())
        self.logger.debug("Creating attachment for ticket %s", ticket_id)
        self.client.ticketing.create_attachment(
            ticket_id=ticket_id,
            request=engine.CreateAttachmentRequest(
                file_name=file_path.name,
                content=content,
            ),
        )
        self.logger.info("Added an attachment to %s ticket %s", self.integration, ticket_id)

    def compare_files_for_dupes_and_upload(self, connector_issue: Ticket, regscale_issue: Issue) -> None:
        """
        Compare attachments for provided Integration and RegScale issues via hash to prevent duplicates

        :param Ticket connector_issue: Connector issue object to compare attachments from
        :param Issue regscale_issue: RegScale issue object to compare attachments from
        :rtype: None
        """
        connector_uploaded_attachments = []
        regscale_uploaded_attachments = []
        # create a temporary directory to store the downloaded attachments from desired connector and RegScale
        with tempfile.TemporaryDirectory() as temp_dir:
            # write attachments to the temporary directory
            connector_dir, regscale_dir = self.download_issue_attachments_to_directory(
                directory=temp_dir,
                integration_issue=connector_issue,
                regscale_issue=regscale_issue,
            )
            # get the hashes for the attachments in the RegScale and connector directories
            # iterate all files in the connector directory and compute their hashes
            ticket_attachment_hashes = compute_hashes_in_directory(connector_dir)
            regscale_attachment_hashes = compute_hashes_in_directory(regscale_dir)

            # check where the files need to be uploaded to before uploading
            for file_hash, file in regscale_attachment_hashes.items():
                if file_hash not in ticket_attachment_hashes:
                    try:
                        self.upload_synqly_attachments(
                            ticket_id=connector_issue.id,
                            file_path=Path(file),
                        )
                        connector_uploaded_attachments.append(file)
                    except TypeError as ex:
                        self.logger.error(
                            "Unable to upload %s to %s issue %s.\nError: %s",
                            Path(file).name,
                            self.integration,
                            connector_issue.id,
                            ex,
                        )
            for file_hash, file in ticket_attachment_hashes.items():
                if file_hash not in regscale_attachment_hashes:
                    with open(file, "rb") as in_file:
                        if File.upload_file_to_regscale(
                            file_name=f"{self.integration}_attachment_{Path(file).name}",
                            parent_id=regscale_issue.id,
                            parent_module="issues",
                            api=self.api,
                            file_data=in_file.read(),
                        ):
                            regscale_uploaded_attachments.append(file)
                            self.logger.debug(
                                "Uploaded %s to RegScale issue #%i.",
                                Path(file).name,
                                regscale_issue.id,
                            )
                        else:
                            self.logger.warning(
                                "Unable to upload %s to RegScale issue #%i.",
                                Path(file).name,
                                regscale_issue.id,
                            )
        self.log_upload_outcome(
            regscale_uploads=regscale_uploaded_attachments,
            connector_uploads=connector_uploaded_attachments,
            regscale_issue=regscale_issue,
            connector_issue=connector_issue,
        )

    def log_upload_outcome(
        self, regscale_uploads: list, connector_uploads: list, regscale_issue: Issue, connector_issue: Ticket
    ) -> None:
        """
        Log the outcome of the attachment uploads

        :param list regscale_uploads: List of RegScale attachments uploaded
        :param list connector_uploads: List of Connector attachments uploaded
        :param Issue regscale_issue: RegScale issue object
        :param Ticket connector_issue: Connector issue object
        :rtype: None
        """
        if regscale_uploads and connector_uploads:
            self.logger.info(
                "%i file(s) uploaded to RegScale issue #%i and %i file(s) uploaded to %s ticket %s.",
                len(regscale_uploads),
                regscale_issue.id,
                len(connector_uploads),
                self.integration,
                connector_issue.id,
            )
        elif connector_uploads:
            self.logger.info(
                "%i file(s) uploaded to %s ticket %s.",
                len(connector_uploads),
                self.integration,
                connector_issue.id,
            )
        elif regscale_uploads:
            self.logger.info(
                "%i file(s) uploaded to RegScale issue #%i.",
                len(regscale_uploads),
                regscale_issue.id,
            )

    def validate_params(self, **kwargs) -> bool:
        """
        Validate the params are provided for the integration

        :param dict **kwargs: Secrets to validate
        :return: True if all required secrets are provided, False otherwise
        :rtype: bool
        """
        missing_params = {}
        for param in self.optional_params:
            if param not in kwargs:
                missing_params[param] = self.optional_params[param]
        if missing_params:
            self.logger.error("Missing parameters:")
            for param, data in missing_params.items():
                self.logger.error(f"{param} ({data['type']}) - {data['description']}")
            error_and_exit("Please provide the required parameters mentioned above.")
        return len(missing_params) == 0

    def run_sync(self, regscale_id: int, regscale_module: str, sync_attachments: bool = True, **kwargs: dict) -> None:
        """
        Syncs RegScale issues with Ticketing connector using Synqly

        :param int regscale_id: RegScale record ID Number to sync issues to
        :param str regscale_module: RegScale module to sync issues to
        :param bool sync_attachments: Flag to determine if attachments should be synced, defaults to True
        :param dict **kwargs: Additional arguments to pass to the sync process
        :raises Exception: If an error occurs during the sync process
        :rtype: None
        """
        self.create_config_and_validate_secrets(**kwargs)
        # TODO: need a better way seeing if params are required or optional
        # self.validate_params(**kwargs)
        # TODO: store this in the application and fetch it from there
        synqly_access_token = os.getenv("SYNQLY_ACCESS_TOKEN") or self.app.config["synqlyAccessToken"]

        # Initialize tenants within our Application
        tenant_name = f"RegScale-CLI - {self.app.config.get('domain')} {self.integration}"
        try:
            self.new_tenant(synqly_access_token, tenant_name)
            self.logger.debug(f"{tenant_name} created")
        except Exception as e:
            self.logger.error(f"Error creating Tenant {tenant_name}:" + str(e))
            self._cleanup_handler()
            raise e

        # Configure a mock integration for tenant ABC and a JIRA Integration for Tenant XYZ
        try:
            self.configure_integration(tenant_name, self.integration_config)
        except Exception as e:
            print(f"Error configuring provider integration for Tenant {tenant_name}: " + str(e))
            self._cleanup_handler()
            raise e

        # Start a background job to generate data
        try:
            self.logger.info(f"Fetching tickets from {self.integration}...")
            integration_issues = self.fetch_integration_issues(**kwargs)
            self.logger.info(f"Found {len(integration_issues)} ticket(s) in {self.integration}")
            self.logger.info("Fetching issues from RegScale...")
            (
                regscale_issues,
                regscale_attachments,
            ) = Issue.fetch_issues_and_attachments_by_parent(
                app=self.app,
                parent_id=regscale_id,
                parent_module=regscale_module,
                fetch_attachments=sync_attachments,
            )
            self.logger.info(f"Found {len(regscale_issues)} issue(s) in RegScale")

            self.process_regscale_issues(
                regscale_issues=regscale_issues,
                regscale_attachments=regscale_attachments,
                sync_attachments=sync_attachments,
                **kwargs,
            )

            self.process_integration_issues(
                integration_issues=integration_issues,
                regscale_issues=regscale_issues,
                regscale_id=regscale_id,
                regscale_module=regscale_module,
                sync_attachments=sync_attachments,
            )
        except Exception as e:
            print("Error running background job: " + str(e))
            self._cleanup_handler()
            raise e

        self._cleanup_handler()

    def fetch_integration_issues(self, **kwargs: dict) -> list[Ticket]:
        """
        Fetch all issues from the integration

        :param Tenant tenant: Tenant object to fetch issues from
        :param dict **kwargs: Additional arguments to pass to the sync
        :return: List of all issues from the integration
        :rtype: list[Ticket]
        """
        # TODO: know the correct way to filter these issues for other integrations
        query_filter = f"project[eq]{kwargs['project']}"
        integration_issues: list[Ticket] = []
        fetch_res = self.tenant.engine_client.ticketing.query_tickets(
            filter=query_filter,
            limit=100,
        )
        integration_issues.extend(fetch_res.result)
        # check and handle pagination
        while int(fetch_res.cursor) == len(integration_issues):
            fetch_res = self.tenant.engine_client.ticketing.query_tickets(
                filter=query_filter,
                limit=100,
                cursor=fetch_res.cursor,
            )
            integration_issues.extend(fetch_res.result)
        return integration_issues

    def process_regscale_issues(
        self,
        regscale_issues: list[Issue],
        regscale_attachments: Optional[dict] = None,
        sync_attachments: bool = True,
        **kwargs: dict,
    ) -> None:
        """
        Process RegScale issues and sync them to the Integration

        :param list[Issue] regscale_issues: List of RegScale issues to process
        :param dict regscale_attachments: Dictionary of RegScale attachments
        :param bool sync_attachments: Flag to determine if attachments should be synced, defaults to True
        :param dict **kwargs: Additional arguments to pass to the sync process
        :rtype: None
        """
        if regscale_issues:
            # sync RegScale issues to Integration
            self.sync_regscale_to_integration(
                regscale_issues=regscale_issues,
                sync_attachments=sync_attachments,
                attachments=regscale_attachments,
                **kwargs,
            )
            if self.regscale_objects_to_update:
                with self.job_progress as job_progress:
                    # create task to update RegScale issues
                    updating_issues = job_progress.add_task(
                        f"[#f8b737]Updating {len(self.regscale_objects_to_update)} RegScale issue(s) from {self.integration}...",
                        total=len(self.regscale_objects_to_update),
                    )
                    # create threads to analyze Jira issues and RegScale issues
                    self.app.thread_manager.submit_tasks_from_list(
                        self.update_regscale_issues,
                        (
                            self.regscale_objects_to_update,
                            updating_issues,
                        ),
                    )
                    results = self.app.thread_manager.execute_and_verify(check_for_failures=False)
                    # output the failed results
                    for success, result in results:
                        if not success:
                            self.logger.error(f"Task failed with error: {result}")
                    self.logger.info(
                        "%i/%i issue(s) updated in RegScale.",
                        len(self.updated_regscale_objects),
                        len(self.regscale_objects_to_update),
                    )
        else:
            self.logger.info("No issues need to be updated in RegScale.")

    def process_integration_issues(
        self,
        integration_issues: list[Ticket],
        regscale_issues: list[Issue],
        regscale_id: int,
        regscale_module: str,
        sync_attachments: bool = True,
    ) -> None:
        """
        Process Integration issues and sync them to RegScale

        :param list[Ticket] integration_issues: List of Integration issues to process
        :param list[Issue] regscale_issues: List of RegScale issues to process
        :param int regscale_id: RegScale record ID Number to sync issues to
        :param str regscale_module: RegScale module to sync issues to
        :param bool sync_attachments: Flag to determine if attachments should be synced, defaults to True
        :rtype: None
        """
        if integration_issues:
            # sync integration issues to RegScale
            with self.job_progress as job_progress:
                # create task to create RegScale issues
                creating_issues = job_progress.add_task(
                    f"[#f8b737]Analyzing {len(integration_issues)} {self.integration} ticket(s)"
                    f" and {len(regscale_issues)} RegScale issue(s)...",
                    total=len(integration_issues),
                )
                # create threads to analyze Jira issues and RegScale issues
                self.app.thread_manager.submit_tasks_from_list(
                    self.create_and_update_regscale_issues,
                    integration_issues,
                    (
                        regscale_issues,
                        sync_attachments,
                        regscale_id,
                        regscale_module,
                        creating_issues,
                    ),
                )
                results = self.app.thread_manager.execute_and_verify(check_for_failures=False)
                # output the failed results
                for success, result in results:
                    if not success:
                        self.logger.error(f"Task failed with error: {result}")
                self.logger.info(
                    "Analyzed %i %s ticket(s), created %i issue(s) and updated %i issue(s) in RegScale.",
                    len(integration_issues),
                    self.integration,
                    len(self.created_regscale_objects),
                    len(self.updated_regscale_objects),
                )
        else:
            self.logger.info(f"No tickets need to be analyzed from {self.integration}.")

    def create_and_update_regscale_issues(self, *args: Tuple, **kwargs: dict) -> None:
        """
        Function to create or update issues in RegScale from Jira

        :param Tuple args: Tuple of args to use during the process
        :param dict **kwargs: Additional arguments to pass
        :rtype: None
        """
        # set up local variables from the passed args
        integration_issue: Ticket = args[0]  # type: ignore
        (
            regscale_issues,
            add_attachments,
            parent_id,
            parent_module,
            task,
        ) = args[1]
        if self.has_integration_field:
            regscale_issue: Optional[Issue] = next(
                (
                    issue
                    for issue in regscale_issues
                    if getattr(issue, self.integration_id_field) == integration_issue.id
                ),
                None,
            )
        else:
            # use the manualDetectionSource and manualDetectionId fields
            regscale_issue: Optional[Issue] = next(
                (
                    issue
                    for issue in regscale_issues
                    if issue.manualDetectionSource == self.integration
                    and issue.manualDetectionId == integration_issue.id
                ),
                None,
            )
        # see if the Jira issue needs to be created in RegScale
        if integration_issue.status.lower() == "done" and regscale_issue:
            # update the status and date completed of the RegScale issue
            regscale_issue.status = "Closed"
            regscale_issue.dateCompleted = get_current_datetime()
            # update the issue in RegScale
            self.updated_regscale_objects.append(regscale_issue.save())
        elif regscale_issue:
            # update the issue in RegScale
            self.updated_regscale_objects.append(regscale_issue.save())
        else:
            # map the jira issue to a RegScale issue object
            issue = self.mapper.to_regscale(
                connector=self,
                oscf_object=integration_issue,
                config=self.app.config,  # type: ignore
                parent_id=parent_id,
                parent_module=parent_module,
                **kwargs,
            )
            # create the issue in RegScale
            if regscale_issue := issue.create():
                self.logger.debug(
                    "Created issue #%i-%s in RegScale.",
                    regscale_issue.id,
                    regscale_issue.title,
                )
                self.created_regscale_objects.append(regscale_issue)
            else:
                self.logger.warning("Unable to create issue in RegScale.\nIssue: %s", issue.dict())
        if add_attachments and regscale_issue:
            # check if the integration issue has attachments
            attachment_count = self.get_integration_attachment_count(integration_issue.id)
            if attachment_count > 0:
                # determine which attachments need to be uploaded to prevent duplicates by
                # getting the hashes of all Jira & RegScale attachments
                self.compare_files_for_dupes_and_upload(
                    connector_issue=integration_issue,
                    regscale_issue=regscale_issue,
                )
        # update progress bar
        self.job_progress.update(task, advance=1)

    def get_integration_attachment_count(self, ticket_id: str) -> int:
        """
        Get the number of attachments for a ticket in Synqly

        :param str ticket_id: Ticket ID to get the attachments for
        :return: Number of attachments for the ticket
        :rtype: int
        """
        try:
            attachments = self.client.ticketing.list_attachments_metadata(ticket_id)
            return len(attachments.result)
        except Exception as ex:
            self.logger.error(f"Unable to get attachments for ticket {ticket_id}.\nError: {ex}")
            return 0

    def update_regscale_issues(self, *args: Tuple, **kwargs: dict) -> None:
        """
        Function to compare Integration issues and RegScale issues

        :param Tuple *args: Tuple of args to use during the process
        :param dict **kwargs: Additional arguments to pass to the sync
        :rtype: None
        """
        # set up local variables from the passed args
        regscale_issue: Issue = args[0]  # type: ignore
        task: rich.progress.TaskID = args[1]  # type: ignore
        # update the issue in RegScale
        regscale_issue.save()
        self.logger.info(
            "RegScale Issue %i was updated with the %s link.",
            regscale_issue.id,
            self.integration.title(),
        )
        self.update_counter.append(regscale_issue)
        # update progress bar
        self.job_progress.update(task, advance=1)

    def create_issue_in_integration(
        self,
        issue: Issue,
        add_attachments: Optional[bool] = False,
        attachments: list[File] = None,
        **kwargs: dict,
    ) -> Optional[Ticket]:
        """
        Create a new issue in the integration

        :param Issue issue: RegScale issue object
        :param Optional[bool] add_attachments: Flag to determine if attachments should be added to the issue
        :param list[File] attachments: List of attachments to add to the issue
        :param dict **kwargs: Additional arguments to pass to the sync process
        :return: Newly created issue in Jira
        :rtype: Optional[Ticket]
        """
        try:
            new_issue = self.mapper.to_oscf(issue, **kwargs)
            create_response = self.client.ticketing.create_ticket(request=new_issue)
        except Exception as ex:
            self.logger.error(f"Unable to create {self.integration} ticket.\nError: {ex}")
            return None
        if add_attachments and attachments:
            self.compare_files_for_dupes_and_upload(
                connector_issue=create_response.result.Ticket,
                regscale_issue=issue,
            )
        self.logger.info("Created ticket: {}".format(create_response.result.name))
        return create_response.result

    def sync_regscale_to_integration(
        self,
        regscale_issues: list[Issue],
        sync_attachments: bool = True,
        attachments: Optional[dict] = None,
        **kwargs: dict,
    ) -> list[Issue]:
        """
        Sync issues from RegScale to Jira

        :param list[Issue] regscale_issues: list of RegScale issues to sync to Jira
        :param bool sync_attachments: Flag to determine if attachments should be synced, defaults to True
        :param Optional[dict] attachments: Dictionary of attachments to sync, defaults to None
        :param dict **kwargs: Additional arguments to pass to the sync process
        :return: list of RegScale issues that need to be updated
        :rtype: list[Issue]
        """
        for issue in regscale_issues:
            # see if integration field is an option
            if (self.has_integration_field and not getattr(issue, self.integration_id_field, None)) or (
                issue.manualDetectionSource != self.integration and not issue.manualDetectionId
            ):
                if new_issue := self.create_issue_in_integration(
                    issue=issue,
                    add_attachments=sync_attachments,
                    attachments=attachments,
                    **kwargs,
                ):
                    self.created_integration_objects.append(new_issue)
                    if self.has_integration_field:
                        # update the RegScale issue for the integration link
                        setattr(issue, self.integration_id_field, new_issue.id)
                    else:
                        # use the manualDetectionSource and manualDetectionId fields
                        issue.manualDetectionSource = self.integration
                        issue.manualDetectionId = new_issue.id
                    self.regscale_objects_to_update.append(issue)
        # output the final result
        self.logger.info("%i new ticket(s) opened in %s.", len(self.created_integration_objects), self.integration)
        return self.regscale_objects_to_update
