import zipfile, requests, io, typing, os
from .storage import default_storage


class Input:
    def __init__(self, *, operationId: str, baseUrl: str, inputFilesPath: str, modelArtifactsPath: str, arguments: dict):
        self.operationId = operationId
        self.baseUrl = baseUrl
        self.inputFilesPath = inputFilesPath
        self.modelArtifactsPath = modelArtifactsPath
        self.arguments = arguments
    

    def get_temporary_files_directory(self):
        return default_storage.get_temporary_files_directory()
    
    def get_input_files(self) -> typing.List[str]:
        response = requests.get(self.baseUrl + self.inputFilesPath)
        
        files = []
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            for file_name in zip_file.namelist():
                with zip_file.open(file_name) as extracted_file:
                    file_content = extracted_file.read()
                    filePath = f'{self.get_temporary_files_directory()}/{self.operationId}_{file_name}'
                    with open(filePath, 'wb') as output_file:
                        output_file.write(file_content)
                    
                    files.append(filePath)

        return files
    

    def get_model_artifacts(self) -> typing.List[str]:
        response = requests.get(self.baseUrl + self.modelArtifactsPath)
        files = []
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            for file_name in zip_file.namelist():
                with zip_file.open(file_name) as extracted_file:
                    file_content = extracted_file.read()
                    filePath = f'{self.get_temporary_files_directory()}/{self.operationId}_{file_name}'
                    with open(filePath, 'wb') as output_file:
                        output_file.write(file_content)
                    
                    files.append(filePath)

        return files
    
    @property
    def outputUrl(self) -> str:
        return f"{self.baseUrl}/api/inferences/{self.operationId}/output"
    
    @property
    def errorUrl(self) -> str:
        return f"{self.baseUrl}/api/inferences/{self.operationId}/error"