import unittest
import logging
import yaml
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from hexa_mlops.azureml.azure_pipeline_file_generator import AzPipelineFileGenerator


class TestPipelineGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
    def setUp(self):
        self.maxDiff = None
        self.training_file = "test_inputs/training.yaml"
        self.config_file =  "test_inputs/training_config.yaml"
        self.pipeline_file = "test_outputs/pipeline.yaml"
        self.pipeline_no_value_file =  "test_outputs/pipeline_no_value.yaml"
        self.inputs_file_path = "test_outputs/inputs.yaml"
        self.generator_w_value = AzPipelineFileGenerator( self.config_file,self.pipeline_file, self.training_file)
        self.generator_no_value = AzPipelineFileGenerator(self.config_file,self.pipeline_no_value_file, self.training_file, input_file_path=self.inputs_file_path, pipeline_with_value=False)
    
    def test_generating_pipeline_file_w_value(self):
        logging.info("Test generating pipeline file with value ")
        self.generator_w_value.generate()
        with open(self.pipeline_file , 'r') as file:
            result = yaml.safe_load(file)
        expected = {
            '$schema': 'https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json',
            'type': 'pipeline',
            'experiment_name': 'ahp_mlops',
            'inputs': {
                 'data_config': {
                     'path': '../src/download_data/config_AF_new.yaml',
                    'type': 'uri_file'
                    },
                'train_config': {
                    'path': '../src/train/config_GBT.yaml',
                    'type': 'uri_file'
                    }
                    },
            'jobs': {
                'download_data': {
                    'code': '../src/download_data/',
                    'command': 'python download_data.py --data_config ${{inputs.data_config}} --data_folder ${{outputs.data_folder}}',
                    'compute': 'azureml:demo-compute',
                    'environment': 'azureml:h2o_env:3',
                    'inputs': {'data_config': '${{parent.inputs.data_config}}'},
                    'outputs': {'data_folder': {}},
                    'type': 'command'
                    },
                'data_prep': {
                    'code': '../src/data_prep/',
                    'command': 'python data_prep.py --json_folder ${{inputs.json_folder}} --output_folder ${{outputs.output_folder}}',
                    'compute': 'azureml:demo-compute',
                    'environment': 'azureml:h2o_env:3',
                    'inputs': {'json_folder': '${{parent.jobs.download_data.outputs.data_folder}}'},
                    'outputs': {'output_folder': {}},
                    'type': 'command'},
                'train': {
                    'code': '../src/train/',
                    'command': 'python train.py --config ${{inputs.config}} --input ${{inputs.input}} --output ${{outputs.output}}',
                    'compute': 'azureml:demo-compute',
                    'environment': 'azureml:h2o_env:3',
                    'inputs': {
                        'config': '${{parent.inputs.train_config}}',
                        'input': '${{parent.jobs.data_prep.outputs.output_folder}}'
                        },
                    'outputs': {'output': {}},
                    'type': 'command'}}
                    }
        self.assertEqual(result, expected)
    def test_generating_pipeline_file_wo_value(self):
        logging.info("Test generating pipeline file without value")
        self.generator_no_value.generate()
        with open(self.pipeline_file , 'r') as file:
            result = yaml.safe_load(file)
        expected = {
            '$schema': 'https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json',
            'type': 'pipeline',
            'experiment_name': 'ahp_mlops',
            'inputs': {
                 'data_config': {
                    'type': 'uri_file'
                    },
                'train_config': {
                    'type': 'uri_file'
                    }
                    },
            'jobs': {
                'download_data': {
                    'code': '../src/download_data/',
                    'command': 'python download_data.py --data_config ${{inputs.data_config}} --data_folder ${{outputs.data_folder}}',
                    'compute': 'azureml:demo-compute',
                    'environment': 'azureml:h2o_env:3',
                    'inputs': {'data_config': '${{parent.inputs.data_config}}'},
                    'outputs': {'data_folder': {}},
                    'type': 'command'
                    },
                'data_prep': {
                    'code': '../src/data_prep/',
                    'command': 'python data_prep.py --json_folder ${{inputs.json_folder}} --output_folder ${{outputs.output_folder}}',
                    'compute': 'azureml:demo-compute',
                    'environment': 'azureml:h2o_env:3',
                    'inputs': {'json_folder': '${{parent.jobs.download_data.outputs.data_folder}}'},
                    'outputs': {'output_folder': {}},
                    'type': 'command'},
                'train': {
                    'code': '../src/train/',
                    'command': 'python train.py --config ${{inputs.config}} --input ${{inputs.input}} --output ${{outputs.output}}',
                    'compute': 'azureml:demo-compute',
                    'environment': 'azureml:h2o_env:3',
                    'inputs': {
                        'config': '${{parent.inputs.train_config}}',
                        'input': '${{parent.jobs.data_prep.outputs.output_folder}}'
                        },
                    'outputs': {'output': {}},
                    'type': 'command'}}
                    }
    def test_inputs_file_generation(self):
        self.generator_no_value.generate()
        logging.info("Test generating inputs file ")

        with open(self.inputs_file_path , 'r') as file:
            result = yaml.safe_load(file)
        expected = {
            "inputs": {
                "data_config":{
                    "path": "../src/download_data/config_AF_new.yaml", "type": "uri_file"
                },
                "train_config":{
                     "path": "../src/train/config_GBT.yaml", "type":"uri_file"
                }
            }
        }
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()