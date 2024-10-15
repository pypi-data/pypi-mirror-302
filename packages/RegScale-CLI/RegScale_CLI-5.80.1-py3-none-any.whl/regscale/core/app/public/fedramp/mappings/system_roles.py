"""Mappings for System Roles."""

from lxml import etree

from regscale.core.app.application import Application
from regscale.core.app.public.fedramp.mappings.values import (
    UUID,
    FunctionPerformed,
    Title,
)
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models.system_roles import SystemRoles


def create_system_role(element: etree._Element) -> SystemRoles:
    """
    Create a SystemRoles object from an XML Element

    :param etree._Element element: The XML Element to parse
    :return: A SystemRoles object
    :rtype: SystemRoles
    """
    data = {}
    for field in [UUID, Title, FunctionPerformed]:
        for elem in element:
            if results := field.parse_from_element(elem):
                data[field.value] = results[1]
    app = Application()
    data["id"] = 0
    data["createdById"] = app.config.get("userId")
    data["lastUpdatedById"] = app.config.get("userId")
    data["dateCreated"] = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")
    data["dateLastUpdated"] = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")
    return SystemRoles(**data)
