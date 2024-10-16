import unittest
import unittest.mock
from irisml.tasks.call_azure_openai_completion import Task


class TestCallAzureOpenaiCompletion(unittest.TestCase):
    def test_simple(self):
        inputs = Task.Inputs(prompts=['hello', 'world'])
        with unittest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'choices': [{'text': 'test'}], 'usage': {'total_tokens': 10, 'prompt_tokens': 4, 'completion_tokens': 6}}
            outputs = Task(Task.Config(endpoint='https://example.com', deployment_name='deployment_name', api_key='test_api_key')).execute(inputs)
            self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(outputs.texts, ['test', 'test'])

    def test_dry_run(self):
        inputs = Task.Inputs(prompts=['hello', 'world'])
        outputs = Task(Task.Config(endpoint='https://example.com', deployment_name='deployment_name', api_key='test_api_key')).dry_run(inputs)
        self.assertEqual(len(outputs.texts), 2)
