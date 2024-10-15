#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prisma RegScale integration"""
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from regscale.core.app.application import Application
from regscale.models.app_models.mapping import Mapping
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.integration_models.prisma import Prisma
from regscale.validation.record import validate_regscale_object


@click.group()
def prisma():
    """Performs actions on Prisma export files."""


@prisma.command(name="show_mapping")
def show_mapping():
    """Show the default mapping for Prisma."""
    import json

    mapping = Prisma.default_mapping().mapping
    console = Console()
    # convert dict to json string
    dat = json.dumps(mapping, indent=4)
    console.print(dat)


@prisma.command(name="import_prisma")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing Nexpose .csv files to process to RegScale.",
    prompt="File path for Prisma files:",
)
@click.option(
    "--header_map_file",
    help="The CLI will use the custom header from the provided mapping file",
    type=click.Path(exists=True),
    default=None,
    required=False,
)
def import_prisma(folder_path: PathLike[str], regscale_ssp_id: int, scan_date: datetime, header_map_file: Path):
    """
    Import scans, vulnerabilities and assets to RegScale from Prisma export files
    """
    import_prisma_data(
        folder_path=folder_path,
        regscale_ssp_id=regscale_ssp_id,
        scan_date=scan_date,
        header_map_file=header_map_file,
    )


def import_prisma_data(
    folder_path: PathLike[str], regscale_ssp_id: int, scan_date: datetime, header_map_file: Optional[Path] = None
) -> None:
    """
    Import Prisma data to RegScale

    :param PathLike[str] folder_path: Path to the folder containing Prisma .csv files
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param datetime scan_date: Date of the scan
    :param Optional[Path] header_map_file: Path to the header mapping file, defaults to None
    :rtype: None
    """
    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    if len(list(Path(folder_path).glob("*.csv"))) == 0:
        app.logger.warning("No Prisma(csv) files found in the specified folder.")
        return
    mapping = None
    if header_map_file:
        # define must have fields
        expected_fields = ["Hostname", "Distro", "CVSS", "CVE ID", "Description", "Fix Status"]
        mapping = Mapping.from_file(file_path=header_map_file, expected_field_names=expected_fields)
    for file in Path(folder_path).glob("*.csv"):
        Prisma(
            name="Prisma", file_path=str(file), regscale_ssp_id=regscale_ssp_id, scan_date=scan_date, mapping=mapping
        )
