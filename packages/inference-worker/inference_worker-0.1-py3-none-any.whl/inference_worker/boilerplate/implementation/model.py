from inference_worker import abstraction

class Model(abstraction.Model):

    def infer(self, input_file_paths, *args, arguments={}, **kwargs):

        raise NotImplementedError()
