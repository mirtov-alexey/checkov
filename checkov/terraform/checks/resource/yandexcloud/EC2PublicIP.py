from typing import List, Any

from checkov.common.models.enums import CheckCategories
from checkov.terraform.checks.resource.base_resource_negative_value_check import BaseResourceNegativeValueCheck


class EC2PublicIP(BaseResourceNegativeValueCheck):
    def __init__(self) -> None:
        name = "EC2 instance should not have public IP."
        id = "CKV_YC_2"
        categories = [CheckCategories.NETWORKING]
        supported_resources = ["yandex_compute_instance"]
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_resources=supported_resources,
        )

    def get_inspected_key(self) -> str:
        if self.entity_type == "yandex_compute_instance":
            return "network_interface/[0]/nat"

        return ""

    def get_forbidden_values(self) -> List[Any]:
        return [True]


check = EC2PublicIP()
