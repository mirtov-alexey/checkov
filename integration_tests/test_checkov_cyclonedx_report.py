import os
import unittest
from xml.dom import minidom

current_dir = os.path.dirname(os.path.realpath(__file__))


class TestCheckovCyclonedxReport(unittest.TestCase):
    def test_terragoat_report(self):
        report_path = os.path.join(os.path.dirname(current_dir), "checkov_report_terragoat_cyclonedx.xml")
        self.validate_report(os.path.abspath(report_path))

    def validate_report(self, report_path: str) -> None:
        with open(report_path) as cyclonedx_file:
            data = minidom.parse(cyclonedx_file)
            self.validate_report_not_empty(data)

    def validate_report_not_empty(self, report: minidom.Document) -> None:
        vulnerability_files = [
            node.getElementsByTagName("name")[0].firstChild.nodeValue
            for node in report.getElementsByTagName("components")[0].getElementsByTagName("component")
        ]
        self.assertTrue(any("db-app.tf" in file for file in vulnerability_files), "Could not find db-app.tf in report")


if __name__ == "__main__":
    unittest.main()
