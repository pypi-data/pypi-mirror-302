from unittest import TestCase


class SmokeTest(TestCase):
    def test_imports(self):
        from bitbucket_pipes_toolkit.helpers import success
        from bitbucket_pipes_toolkit.test import PipeTestCase
