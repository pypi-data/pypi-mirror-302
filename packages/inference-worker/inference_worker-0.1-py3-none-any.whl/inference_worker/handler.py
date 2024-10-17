from input import Input
from exceptions import InferenceError
from .abstraction import InferenceResult
import requests, os, json, importlib

class Handler:

    def __init__(self, config_path='config.json'):
        self.model_builder_class = self._load_implementation(config_path)

    def _load_implementation(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        module_path, class_name = config["model_builder_class"].rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    
    def handle(self, input: Input):
        inputFiles = input.get_input_files()
        modelArtifacts = input.get_model_artifacts()
        
        try:
            modelBuilder = self.model_builder_class()
            model = modelBuilder.build(modelArtifacts)
            result: InferenceResult = model.infer(inputFiles)
            self._handle_success(input, result)
        except InferenceError as e:
            self._handle_error(input, e.code, e.message)

        
    def _handle_success(self, input: Input, result: InferenceResult):
        filename = os.path.basename(result['output'])
        metadta = result['metadata']
        multipart_form_data = {
            'outputFile': (filename, open(result['output'], 'rb')),
        }
        response = requests.post(
            input.outputUrl, 
            files=multipart_form_data,
            data={'metadata': json.dumps(metadta)}
        )

        if response.status_code != 200:
            print(response.content)
            print(response.status_code, response.reason)
        else:
            print('==========SUCESS (Result)===========')
            print(response.json())

    def _handle_error(self, input: Input, code, message):
        
        data = {
            'code': code,
            'message': message
        }

        response = requests.post(input.errorUrl, json=data)
        if (response.status_code != 200):
            print(response.content)
            print(response.status_code, response.reason)

        else:
            print('==========SUCESS (Error)===========')
            print(response.json())