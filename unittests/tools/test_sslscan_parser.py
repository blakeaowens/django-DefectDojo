from dojo.models import Test
from dojo.tools.sslscan.parser import SslscanParser

from ..dojo_test_case import DojoTestCase


class TestSslscanParser(DojoTestCase):

    def test_parse_file_with_no_vuln_has_no_findings(self):
        with open("unittests/scans/sslscan/sslscan_no_vuln.xml") as testfile:
            parser = SslscanParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(0, len(findings))

    def test_parse_file_with_one_vuln_has_one_findings(self):
        with open("unittests/scans/sslscan/sslscan_one_vuln.xml") as testfile:
            parser = SslscanParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(1, len(findings))
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()

    def test_parse_file_with_multiple_vuln_has_multiple_finding(self):
        with open("unittests/scans/sslscan/sslscan_many_vuln.xml") as testfile:
            parser = SslscanParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(2, len(findings))
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()