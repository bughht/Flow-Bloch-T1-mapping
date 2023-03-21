import yaml


class MRISequence:
    def __init__(self, path=None):
        '''
        path: path to sequence file
        '''
        if path is not None:
            self.load(path)

    def load(self, path):
        # Load sequence
        with open(path, 'r') as f:
            try:
                self.data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise Exception("Failed to load sequence") from exc


if __name__ == "__main__":
    print(molli.data)
