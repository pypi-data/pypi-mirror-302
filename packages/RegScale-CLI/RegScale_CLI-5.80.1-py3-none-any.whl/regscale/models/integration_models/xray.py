"""
Nexpose Scan information
"""

from typing import List, Optional

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import epoch_to_datetime, get_current_datetime
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.vulnerability import Vulnerability


class XRay(FlatFileImporter):
    """JFrog Xray Scan information

    :param str name: Name of the scan
    :param Application app: RegScale Application object
    :param str file_path: Path to the JSON files
    :param int regscale_ssp_id: RegScale System Security Plan ID
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        regscale_ssp_id = kwargs.get("regscale_ssp_id")
        file_path = kwargs.get("file_path")
        self.cvss3_score = "cvss_v3_score"
        self.vuln_title = "cve"
        logger = create_logger()
        super().__init__(
            name=self.name,
            logger=logger,
            app=Application(),
            headers=None,
            parent_id=regscale_ssp_id,
            parent_module="securityplans",
            file_path=file_path,
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            file_type=".json",
        )

    def create_asset(self, dat: Optional[dict] = None) -> Optional[Asset]:
        """
        Create an asset from a row in the Xray JSON file

        :param Optional[dict] dat: Data row from JSON file, defaults to None
        :return: RegScale Asset object
        :rtype: Optional[Asset]
        """

        if asset_name := dat.get("impacted_artifact") if isinstance(dat, dict) else dat:
            return Asset(
                **{
                    "id": 0,
                    "name": asset_name,
                    "ipAddress": "0.0.0.0",
                    "isPublic": True,
                    "status": "Active (On Network)",
                    "assetCategory": "Software",
                    "bLatestScan": True,
                    "bAuthenticatedScan": True,
                    "scanningTool": self.name,
                    "assetOwnerId": self.config["userId"],
                    "assetType": "Other",
                    "fqdn": None,
                    "operatingSystem": "Linux",
                    "systemAdministratorId": self.config["userId"],
                    "parentId": self.attributes.parent_id,
                    "parentModule": self.attributes.parent_module,
                }
            )
        return None

    def create_vuln(self, dat: Optional[dict] = None, **kwargs: dict) -> List[Vulnerability]:
        """
        Create a vulnerability from a row in the JFrog Xray JSON file

        :param Optional[dict] dat: Data row from JSON file, defaults to None
        :param dict **kwargs: Additional keyword arguments
        :return: List of RegScale Vulnerability object, if any
        :rtype: List[Vulnerability]
        """
        asset_match = [asset for asset in self.data["assets"] if asset.name == dat.get("impacted_artifact")]
        asset = asset_match[0] if asset_match else None
        vulns = []
        for vuln in dat.get("cves", []):
            # CVE IS A VULN, A VULN IS A CVE, Finkle is Einhorn
            regscale_vuln = None
            severity = (
                Vulnerability.determine_cvss3_severity_text(float(vuln[self.cvss3_score]))
                if vuln.get(self.cvss3_score)
                else "low"
            )
            if asset_match:
                cves = [c["cve"] for c in dat["cves"] if c.get("cve")]
                for cve in cves:
                    regscale_vuln = Vulnerability(
                        id=0,
                        scanId=0,  # set later
                        parentId=asset.id,
                        parentModule="assets",
                        ipAddress="0.0.0.0",  # No ip address available
                        lastSeen=get_current_datetime(),
                        firstSeen=epoch_to_datetime(self.create_epoch),
                        daysOpen=None,
                        dns=dat.get("impacted_artifact"),
                        mitigated=None,
                        operatingSystem="Linux",
                        severity=severity,
                        plugInName=dat.get("issue_id", "XRay"),
                        plugInId=int(dat.get("issue_id", "Xray-0000")[5:]),
                        cve=cve,
                        vprScore=None,
                        tenantsId=0,  # Need a way to figure this out programmatically
                        title=f"{dat['issue_id'] if dat.get('issue_id') else dat.get('summary', f'XRay Vulnerability from Import {get_current_datetime()}')}",
                        description=dat.get("summary"),
                        plugInText=vuln.get("cve"),
                        extra_data={
                            "references": dat.get("references", "None"),
                            "solution": dat.get("fixed_versions", "None"),
                        },
                    )
                vulns.append(regscale_vuln)
        return vulns
