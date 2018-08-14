import pickle
import os

class Config:
    def read_or_new_pickle(self, path, default):
        if os.path.isfile(path):
            with open(path, "rb") as f:
                try:
                    return pickle.load(f)
                except StandardError:
                    pass
        with open(path, "wb") as f:
            pickle.dump(default, f)
        return default

    def save_pickle(self, path, data):
        with open(path, "wb") as f:
            try:
                pickle.dump(data, f)
            except StandardError:
                print("erro")
                pass