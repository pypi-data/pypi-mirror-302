import os
import yaml

from unittest import TestCase
from unittest import mock

from bitbucket_pipes_toolkit import Pipe
from bitbucket_pipes_toolkit import SharedData


class PipeTestCase(TestCase):

    def setUp(self):
        self.schema = {'MY_VAR': {'type': 'string'}}

    def test_validate_success(self):
        pipe = Pipe(env=dict(MY_VAR='my_var'), schema=self.schema)

        validated_data = pipe.validate()
        self.assertIn('MY_VAR', validated_data)

    def test_validate_special_chars_success(self):
        pipe = Pipe(env=dict(MY_VAR="%M5ghDHTAVg6jVK64FxUH2!$e8F3l&Xj"),
                    schema=self.schema)
        validated_data = pipe.validate()

        self.assertIn('MY_VAR', validated_data)
        self.assertTrue(isinstance(validated_data.get('MY_VAR'), str))

        pipe = Pipe(env=dict(MY_VAR="[my header message] further string"),
                    schema=self.schema)
        validated_data = pipe.validate()

        self.assertIn('MY_VAR', validated_data)
        self.assertTrue(isinstance(validated_data.get('MY_VAR'), str))

        pipe = Pipe(env=dict(MY_VAR="${BITBUCKET_BUILD_NUMBER} deployment"),
                    schema=self.schema)
        validated_data = pipe.validate()

        self.assertIn('MY_VAR', validated_data)
        self.assertTrue(isinstance(validated_data.get('MY_VAR'), str))

        pipe = Pipe(env=dict(MY_VAR="123456"),
                    schema=self.schema)
        validated_data = pipe.validate()

        self.assertIn('MY_VAR', validated_data)
        self.assertTrue(isinstance(validated_data.get('MY_VAR'), str))

    def test_check_newer_version_without_digests(self):
        pipe = Pipe(env=dict(MY_VAR='my_var'), schema=self.schema,
                    pipe_metadata={'image': 'repo:0.1.0',
                                   'repository': 'https://bitbucket.org/atlassian/ssh-run'})
        resp = pipe.check_for_newer_version()
        self.assertTrue(resp)

    def test_check_newer_version_wrong_tag(self):
        pipe = Pipe(env=dict(MY_VAR='my_var'), schema=self.schema,
                    pipe_metadata={'image': 'repo:0.1-0',
                                   'repository': 'https://bitbucket.org/atlassian/ssh-run'})
        resp = pipe.check_for_newer_version()
        self.assertFalse(resp)

    def test_check_newer_version_pipe_not_found_officially(self):
        pipe = Pipe(env=dict(MY_VAR='my_var'), schema=self.schema,
                    pipe_metadata={'image': 'repo:0.0.1',
                                   'repository': 'https://bitbucket.org/atlassian/demo-pipe-python'})
        resp = pipe.check_for_newer_version()
        self.assertFalse(resp)

    def test_check_newer_version_image_is_none(self):
        pipe = Pipe(env=dict(MY_VAR='my_var'), schema=self.schema)
        resp = pipe.check_for_newer_version()
        self.assertFalse(resp)

    def test_check_newer_version_digest_current_version_digest(self):
        pipe = Pipe(env=dict(MY_VAR='my_var'), schema=self.schema,
                    pipe_metadata={'image': 'repo:0.0.0@sha256:fced341',
                                   'repository': 'https://bitbucket.org/atlassian/ssh-run'})
        resp = pipe.check_for_newer_version()
        self.assertTrue(resp)

    @mock.patch('requests.get', mock.Mock(return_value=mock.Mock(**{'ok': False, 'text': 'Error'})))
    def test_check_newer_version_request_getting_official_pipes_failed(self):
        pipe = Pipe(env=dict(MY_VAR='my_var'), schema=self.schema,
                    pipe_metadata={'image': 'repo:0.0.0@sha256:fced341',
                                   'repository': 'https://bitbucket.org/atlassian/ssh-run'})
        resp = pipe.check_for_newer_version()
        self.assertFalse(resp)

    def test_check_newer_version_request_fail(self):
        pipe = Pipe(schema={})
        with self.assertRaises(SystemExit):
            pipe.fail(message="fail message")

    def test_link_to_community_with_tags_is_right(self):
        metadata = {"tags": ["aws", "deployment"]}
        pipe = Pipe(pipe_metadata=metadata, schema=self.schema)
        community_link = pipe.get_community_link()
        expected_community_link = "https://community.atlassian.com/t5/forums/postpage/board-id/bitbucket-pipelines-questions?" \
                                  "add-tags=pipes,aws,deployment"

        self.assertEqual(community_link, expected_community_link)


class PipeMetadataFileTestCase(TestCase):

    def setUp(self):
        self.test_metadata = {
            'image': 'bitbucketpipelines/aws-ecs-deploy:0.0.3',
            'repository': 'https://bitbucket.org/atlassian/aws-ecs-deploy'
        }
        # write test yaml to file
        with open('test.yml', 'w') as test_file:
            yaml.dump(self.test_metadata, test_file, default_flow_style=False)

    def test_pipe_metadata_file_given_success(self):
        pipe = Pipe(pipe_metadata_file='test.yml', schema={})
        self.assertEquals(pipe.metadata, self.test_metadata)

    def test_both_metadata_and_metadata_file_given_fail(self):
        with mock.patch.object(Pipe, 'fail') as mock_fail:
            mock_fail.return_value = None
            Pipe(pipe_metadata=self.test_metadata, pipe_metadata_file='test.yml', schema={})
            message = 'Passing both pipe_metadata and pipe_metadata_file is not allowed. Please use only one of them.'
            mock_fail.assert_called_with(message=message)

    def test_pipe_metadata_file_not_found(self):
        with mock.patch.object(Pipe, 'fail') as mock_fail:
            mock_fail.return_value = None
            Pipe(pipe_metadata_file='not_exists.yml', schema={})
            message = 'File not_exists.yml not found. Please give correct path to file.'
            mock_fail.assert_called_with(message=message)

    def test_pipe_metadata_file_yaml_error(self):
        with open('wrong.yml', 'w') as wrong_file:
            wrong_file.write("Definitely not \nYAML text: ///")
        with mock.patch.object(Pipe, 'fail') as mock_fail:
            mock_fail.return_value = None
            Pipe(pipe_metadata_file='wrong.yml', schema={})
            message = 'Failed to parse wrong.yml file: mapping values are not allowed here\n  in "wrong.yml", line 2, column 10'
            mock_fail.assert_called_with(message=message)
        os.remove('wrong.yml')

    def tearDown(self):
        os.remove('test.yml')


class SharedDataTestCase(TestCase):

    def setUp(self):
        self.shared_data = SharedData('/tmp')

    def tearDown(self):
        self.shared_data.purge()

    def test_set_variable_to_existing(self):
        self.shared_data.set_variable('key1', {'type1': 'value1'})
        self.shared_data.set_variable('key2', {'type2': 'value2'})

        var1 = self.shared_data.get_variable('key1')
        var2 = self.shared_data.get_variable('key2')
        self.assertEqual({'type1': 'value1'}, var1)
        self.assertEqual({'type2': 'value2'}, var2)

    def test_get_variable_file_not_found(self):
        resp = self.shared_data.get_variable('not_found')
        self.assertEqual(resp, None)
