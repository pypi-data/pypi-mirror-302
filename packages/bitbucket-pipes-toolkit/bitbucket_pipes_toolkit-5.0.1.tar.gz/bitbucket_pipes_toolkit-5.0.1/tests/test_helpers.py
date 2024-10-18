import os
import pytest
from unittest import TestCase

from bitbucket_pipes_toolkit import get_variable, get_current_pipeline_url


class GetVariableTest(TestCase):
    def setUp(self):
        os.environ['TEST_GET_VARIABLE'] = 'TEST_VALUE'

    def test_get_variable_returs_correct_value(self):
        value = get_variable('TEST_GET_VARIABLE')
        self.assertEqual(value, 'TEST_VALUE')

    def tearDown(self):
        del os.environ['TEST_GET_VARIABLE']


class GetPipelineMumberTest(TestCase):
    def setUp(self):
        os.environ['BITBUCKET_REPO_OWNER'] = 'testowner'
        os.environ['BITBUCKET_REPO_SLUG'] = 'test-slug'
        os.environ['BITBUCKET_BUILD_NUMBER'] = str(123)

    def test_get_current_pipeline_url(self):
        right_url = 'https://bitbucket.org/testowner/test-slug/addon/pipelines/home#!/results/123'
        url = get_current_pipeline_url()
        self.assertEqual(right_url, url)

    @pytest.mark.last
    def test_get_current_pipeline_url_variable_missing(self):
        del os.environ['BITBUCKET_REPO_OWNER']
        self.assertRaisesRegex(Exception, "variable missing.", get_current_pipeline_url)

    def tearDown(self):
        del os.environ['BITBUCKET_REPO_SLUG']
        del os.environ['BITBUCKET_BUILD_NUMBER']
