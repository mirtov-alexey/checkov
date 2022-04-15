from checkov.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from checkov.common.models.enums import CheckCategories


class S3_SSE(BaseResourceValueCheck):

    def __init__(self):
        name = "Ensure that bucket are encrypted"
        id = "CKV_YC_3"
        supported_resources = ['yandex_storage_bucket']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "server_side_encryption_configuration/[0]/rule/[0]/apply_server_side_encryption_by_default/[0]/kms_master_key_id"

check = S3_SSE()