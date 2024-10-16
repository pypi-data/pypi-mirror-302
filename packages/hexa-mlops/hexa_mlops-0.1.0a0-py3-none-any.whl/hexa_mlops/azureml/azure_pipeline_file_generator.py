import yaml
from collections import OrderedDict
import logging
from ..base.constants import *
from ..base.file_generator import FileGenerator
import copy
from collections import namedtuple
yaml.add_representer(OrderedDict, FileGenerator.represent_ordereddict)

class AzPipelineFileGenerator(FileGenerator):
    """
    A class that represents an Azure Pipeline File Generator.

    This class is responsible for generating an Azure Pipeline YAML file based on the provided configuration.
    It provides methods to generate pipeline jobs, job inputs, job outputs, and the overall pipeline.

    Attributes:
        config_file_path (str): The path to the config.
        training_file_path (str): The path to the training data.
        output_file_path (str): The path to the generated file.
        pipeline_with_value (bool): Indicates whether to generate a pipeline with global input values. Defaults to True.

    Methods:
        get_training_file_contents(): Load content from the training pipeline file and return the pipeline inputs, outputs, and jobs.
        generate_global_inputs_outputs(item_list: list) -> dict: Generate global input/output based on the given global input/output list.
        generate_job_input(job_input: dict, inputs: dict, command: list) -> dict: Generate the Azure pipeline job inputs.
        generate_job_output(job_output: dict, outputs: dict, command: list) -> dict: Generate the job output for a given pipeline job.
        generate_pipeline_job(config: dict, job: dict) -> tuple: Generate a pipeline job based on the provided config and job information.
        generate_pipeline_jobs(config: dict, pipeline: list) -> OrderedDict: Generate pipeline jobs based on the provided config and pipeline.
        generate() -> yaml: Generate the Azure Pipeline YAML file based on the provided configuration.
    """
    def __init__(self,
                 config_file_path: str, 
                 output_file_path: str,
                 training_file_path: str, 
                 input_file_path: str=None,
                 pipeline_with_value: bool=True,
                
                ):
        """
        Initialize an instance of the AzurePipelineGenerator class.
        Args:
            config_file_path (str): The path to the config.
            training_file_path (str): The path to the training data.
            output_file_path (str): The path to the generated file.
            pipeline_with_value (bool): Indicates whether to generate a pipeline has global input values. Defaults to True.
            input_file_path (str): The path to the input file to be generated. Defaults to None.
        """
   
        super().__init__(config_file_path, output_file_path)
        self.training_file_path = training_file_path
        self.pipeline_with_value = pipeline_with_value
        self.input_file_path = input_file_path

    def get_training_file_contents(self)-> tuple:
        """
        Args:
            training_file_path (str): The path to the training file.
        Returns:
            tuple: A tuple containing the pipeline inputs, pipeline outputs, and pipeline.
        """
        logging.info("Loading training documents from file: {}".format(self.training_file_path))
        
        with open(self.training_file_path, 'r') as file:
            documents = yaml.safe_load(file)

        
        pipeline_inputs = documents.get(INPUTS)
        pipeline_outputs = documents.get(OUTPUTS)
        pipeline = documents.get(STEPS)
        
        if pipeline_inputs is None:
            logging.warning('No inputs found in the training documents.')
   
        if pipeline is None:
            logging.warning('No jobs found in the training documents.')
        
        return pipeline_inputs, pipeline_outputs, pipeline

    def generate_global_inputs_outputs(self, item_list: list)-> dict:
        """
        Generate input and output items based on the given item list. This is the global inputs or global outputs.
        Original yaml format:
        inputs:
            - name: inputX
              path: ./inputX.json
              type: uri_file
        Generated yaml format:
        inputs:
            inputX:
                path: ./inputX.json
                type: uri_file
        Args:
            item_list (list): A list of items.
        Returns:
            dict: A dictionary containing the generated input and output items.
        """
        generated_item = {}
        for item in item_list:
            item_name = item.get(JOB_NAME)
            item.pop(JOB_NAME)
            generated_item[item_name] = item
        return generated_item
    
    def generate_job_input(self, job_input: namedtuple, inputs: dict, command: dict)-> dict:
        """
        Generates the Azure pipeline job inputs. 
        If the job input comes from global pipeline inputs/outputs (contains "parent" string), change the format of the input_value : input_value -> ${{input_value}}
        If the job input comes from a pipeline output (contains "outputs" string), change the format of the input_value : input_value -> ${{parent.jobs.input_value}}

        Args:
            job_input (namedtupled): A namedtuple to store input of a job containing name, path, and type.
            inputs (dict): A dictionary to store the new formatted job inputs
            command (dict): A list to store all the configs (keys of the first key:value pair of the job) to be included in the command of a py scripts, seperated by inputs/outputs key

        Returns:
            dict: A dictionary containing the updated inputs for the job.
        """

        config_name, input_value = list(job_input.items())[0]
        command["inputs"].append(config_name)
        
        # input value always comes from global input or output of another job
        input_value_list = input_value.split(".")
        if "parent" in input_value_list:
            inputs[config_name] = "${{" + input_value + "}}"
            return inputs
            # in this case, the input is the output of another job
        inputs[config_name] = "${{parent.jobs." + input_value + "}}"
        logging.info("Input value is : {}".format(inputs))
        return inputs

    def generate_job_output(self, job_output: dict, outputs: dict, command: dict)-> dict:
        """
        Generates the job output for a given pipeline job.
        If the job output comes from global pipeline outputs (contains "parent" string), change the format of the output_value : output_value -> ${{output_value}}
        If the job output is defined directly in the job, the value should not contain the first key:value pair of job_output

        Args:
            job_output (dict): The job output dictionary storing the job output value
            outputs (dict): The dictionary to store the new formatted job outputs
            command (dict): A list to store all the configs (keys of the first key:value pair of the job) to be included in the command of a py scripts, seperated by inputs/outputs key

        Returns:
            dict: The updated outputs dictionary.
        """
        config_name, output_value = list(job_output.items())[0]
        command["outputs"].append(config_name)

        if not output_value:
            logging.info("Output value is None")
            outputs[config_name] = {}
            return outputs

        output_value_list = output_value.split(".")
        logging.info("output_value_list: {}".format(output_value_list))
        if "parent" in output_value_list:
            outputs[config_name] = "${{" + output_value + "}}"
            logging.info("Output value is from parent: {}".format(outputs[config_name]))
            return outputs

        outputs[config_name] = output_value
        logging.info("Output value is from job: {}".format(outputs[config_name]))
        return outputs
        
    """
        Generate pipeline job method
        * Generates a pipeline job based on the provided config and job information 
        * Environment and compute values are only defined using the value in config file => same compute and environment are used for all the job in the pipeline
        * Logs a warning when the 'training' key is missing from the config or its value is None
        * Returns a tuple containing the job name and the generated job value
        * The job value contains key:value pairs. The keys include: compute, environment, code, type, inputs, outputs, command
    """    
    @staticmethod
    def validate_and_get_required_value(training_config: dict, key: str)-> str:
        """
        Validate the required value in the training config.
        Args:
            training_config (dict): The training config.
            key (str): The key to be validated.
        Returns:
            str: The value of the key.
        """
        value = training_config.get(key, EMPTY_CONSTANT)
        if not value:
            raise ValueError(f"The '{key}' key is missing from the config or its value is None")
        return value
    
    def generate_pipeline_job(self, training_config: dict, job: dict)-> tuple:
        """
        Args:
            training_config (dict): The config information.
            job (dict): The job information.
        Returns:
            tuple: A tuple containing the job name and the generated job value.
            A job value containing key:value pairs. The keys include: compute, environment, code, type, inputs, outputs, command
        """
        job_name = job.get(JOB_NAME)
        job_input_list = job.get(INPUTS)
        print(job_input_list)
        job_output_list = job.get(OUTPUTS)

        job_value = {}
        inputs = {}
        outputs = {}
        command = {INPUTS: [], OUTPUTS: []}

        compute_name = self.validate_and_get_required_value(training_config, COMPUTE_NAME)
        environment_name = self.validate_and_get_required_value(training_config, ENVIRONMENT_NAME)
        environment_version = self.validate_and_get_required_value(training_config, ENVIRONMENT_VERSION)
        source_code_path = self.validate_and_get_required_value(training_config, SOURCE_CODE_PATH)
    
        for job_input in job_input_list:
            input_result = self.generate_job_input(job_input, inputs, command)

        for job_output in job_output_list:
            output_result = self.generate_job_output(job_output, outputs, command) 

        # Generate command string 
        # TODO: Add support for other types of jobs
        command_str = "python " + job_name + PY_EXT
        for param in command[INPUTS]:
            command_str += " --" + param + " ${{inputs." + param + "}}"
        
        for param in command[OUTPUTS]:
            command_str += " --" + param + " ${{outputs." + param + "}}"
        
        job_value[TYPE] = COMMAND
        job_value[COMPUTE] = "azureml:" + str(compute_name)    
        job_value[COMMAND] = command_str
        job_value[CODE] =  str(source_code_path) + "/" + job_name + "/"
        job_value[INPUTS] = input_result
        job_value[OUTPUTS] = output_result 
        job_value[ENVIRONMENT] = "azureml:" + environment_name + ":" + str(environment_version)
      
        return job_name, job_value

    def generate_pipeline_jobs(self, config: dict, pipeline: list) -> OrderedDict:
        """
        Args:
            config: config dictionary
            pipeline: pipeline list containing the pipeline definition.
        Returns:
            pipeline_jobs: An ordered dictionary containing the generated pipeline jobs.
        """
        logging.info("Read training_pipeline file, generating pipeline jobs....")
        pipeline_jobs = OrderedDict()
        for job in pipeline:
            logging.info("Generating job: {}".format(job.get(JOB_NAME)))
            job_name, job_value = self.generate_pipeline_job(config, job)
            pipeline_jobs[job_name] = job_value
        return pipeline_jobs

    def write_file(self, data: OrderedDict, output_file_path: str, file_type: str, is_inputs=False) -> None:
        """
        Write data to a file.
        Args:
            data (dict): The data to write to the file.
            output_file_path (str): The path to the generated file.
            file_type (str): The type of the file to be generated.
            is_inputs (bool): Indicates whether the file is an input file. Defaults to False.
        """
        with open(output_file_path, 'w') as file:
            if not is_inputs:
                yaml.dump(data, file, default_flow_style=False)
            else:
                yaml.dump({"inputs":data}, file, default_flow_style=False)
            logging.info(f" {file_type} generated successfully at {output_file_path}")

    def generate(self) -> None:
        """
        Generate the Azure Pipeline YAML file based on the provided configuration.
        The pipeline.yaml file generated can contains global input value or not, control by value of self.pipeline_with_value
        Returns:
            yaml: The generated Azure Pipeline YAML content.
            The yaml file contains key:value pairs. The keys include: scheme, type, experiment_name, inputs, outputs, jobs.
        """
        try:
            
            config = self.get_config()
            training_config = config.get(TRAINING_PHASE,EMPTY_CONSTANT)
            if not training_config:
                raise ValueError("The 'training' key is missing from the config or its value is None")

            # Get information from training_pipeline file
            pipeline_inputs, pipeline_outputs, pipeline = self.get_training_file_contents()

            # Check which type of pipeline file to be generated
            if not self.pipeline_with_value:
                logging.info("Pipeline.yaml file to be generated is without global input values")
                inputs_list = copy.deepcopy(pipeline_inputs)
                for input in pipeline_inputs:
                    if "path" in input.keys():
                        del input['path']
            else:
                logging.info("Pipeline.yaml file to be generated is with global input values ")

            logging.info("Generating global inputs ...")
            generated_pipeline_inputs = self.generate_global_inputs_outputs(pipeline_inputs)
            logging.info("Generated global inputs: {}".format(generated_pipeline_inputs))

            logging.info("Generating pipeline jobs")
            generated_pipeline_jobs = self.generate_pipeline_jobs(training_config, pipeline)

            pipeline_stream = OrderedDict([
                    ('$schema', PIPELINE_JOB_SCHEMA ),
                    ('type', "pipeline"),
                    ("experiment_name", config.get(EXPERIMENT_NAME,"")),
                    ("inputs", generated_pipeline_inputs),
                    ("jobs", generated_pipeline_jobs),
                ])
            
            if pipeline_outputs:
                logging.info("Generating global outputs ...")
                generated_pipeline_outputs = self.generate_global_inputs_outputs(pipeline_outputs)
                logging.info("Pipeline file to be generated with global outputs")
                pipeline_stream.update({"outputs": generated_pipeline_outputs})
            else: 
                logging.info("Global outputs are not defined. Pipeline file to be generated without global outputs")

            if not self.pipeline_with_value :
                inputs_dct = {}
                for inputs in inputs_list:
                    inputs_dct[inputs["name"]] = {"path":inputs["path"], "type":inputs["type"]}
                self.write_file(inputs_dct, self.input_file_path, "Input file", is_inputs=True)
                
            self.write_file(pipeline_stream, self.output_file_path, "Pipeline file")

        except Exception as e:
            logging.error("Error occurred while generating pipeline file: {}".format(e))

