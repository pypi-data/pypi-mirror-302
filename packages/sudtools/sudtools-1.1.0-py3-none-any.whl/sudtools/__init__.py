import os
from .cmdline import main


class ModelCollection:
    def __init__(self):
        self._model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../') + 'algorithm'
        self.model_path = []

    def model_dir(self):
        return self._model_dir

    def model_list(self):
        self.get_dirlist(self._model_dir)
        return self.model_path

    def get_dirlist(self, path):
        files = os.listdir(path)
        for file in files:
            inn_path = os.path.join(path, file)
            if os.path.isfile(inn_path):
                self.model_path.append(inn_path)
            else:
                self.get_dirlist(inn_path)


collection = ModelCollection()

__all__ = ['collection']
