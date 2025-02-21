import os

from checkov.common.images.image_referencer import ImageReferencer
from checkov.common.output.report import CheckType
from checkov.github_actions.checks.job_registry import registry as job_registry
from checkov.yaml_doc.runner import Runner as YamlRunner

WORKFLOW_DIRECTORY = ".github/workflows/"


class Runner(YamlRunner, ImageReferencer):
    check_type = CheckType.GITHUB_ACTIONS
    block_type_registries = {
        'jobs': job_registry,
    }

    def __init__(self):
        super().__init__()

    def require_external_checks(self):
        return False

    def import_registry(self):
        return self.block_type_registries['jobs']

    def _parse_file(self, f):
        if self.is_workflow_file(f):
            return super()._parse_file(f)

    def is_workflow_file(self, file_path):
        """
        :return: True if the file mentioned is in a github action workflow directory and is a YAML file. Otherwise: False
        """
        abspath = os.path.abspath(file_path)
        return WORKFLOW_DIRECTORY in abspath and abspath.endswith(("yml", "yaml"))

    def get_images(self, file_path):
        """
        Get container images mentioned in a file
        :param file_path: File to be inspected
        GitHub actions workflow file can have a job run within a container.

        in the following sample file we can see a node:14.16 image:

        # jobs:
        #   my_job:
        #     container:
        #       image: node:14.16
        #       env:
        #         NODE_ENV: development
        #       ports:
        #         - 80
        #       volumes:
        #         - my_docker_volume:/volume_mount
        #       options: --cpus 1
        Source: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-defining-credentials-for-a-container-registry

        :return: List of container image short ids mentioned in the file.
        Example return value for a file with node:14.16 image: ['sha256:6a353e22ce']
        """

        images = set()

        workflow, workflow_line_numbers = self._parse_file(file_path)
        jobs = workflow.get("jobs", {})
        for job_name, job_object in jobs.items():
            if isinstance(job_object, dict):
                container = job_object.get("container", {})
                image = None
                if isinstance(container, dict):
                    image = container.get("image", "")
                elif isinstance(container, str):
                    image = container
                if image:
                    image_id = self.pull_image(image)
                    if image_id:
                        images.add(image_id)

        return images
