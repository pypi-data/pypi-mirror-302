import os
from unittest import mock

from bitbucket_pipes_toolkit.test import PipeTestCase


class PipeTestCaseTestCase(PipeTestCase):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.getcwd(), 'Dockerfile'), 'w') as f:
            f.write("FROM alpine")
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.join(os.getcwd(), 'Dockerfile'))
        super().tearDownClass()

    def test_the_test(self):
        result = self.run_container('echo hello world')
        self.assertIn('hello world', result)

    def test_variables(self):
        result = self.run_container('env')
        self.assertIn('bitbucketpipelines', result)

    def test_test_variables(self):
        variables = {
            'BITBUCKET_BUILD_NUMBER': 'test',
            'BITBUCKET_PARALLEL_STEP': 'test',
            'BITBUCKET_PARALLEL_STEP_COUNT': 'test',
            'BITBUCKET_PROJECT_UUID': 'test',
            'BITBUCKET_PROJECT_KEY': 'test'
        }

        with mock.patch.dict('os.environ', variables):
            result = self.run_container('env')
            self.assertIn('test', result)

    def test_none_variables(self):
        variables = {
            'BITBUCKET_BUILD_NUMBER': '',
            'BITBUCKET_PARALLEL_STEP': '',
            'BITBUCKET_PARALLEL_STEP_COUNT': '',
            'BITBUCKET_PROJECT_UUID': '',
            'BITBUCKET_PROJECT_KEY': ''
        }

        with mock.patch.dict('os.environ', variables):
            result = self.run_container('env')
            self.assertIn('local', result)
