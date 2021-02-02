import importlib.util
import sys


def load_module(path):
    spec = importlib.util.spec_from_file_location(path, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    mod = load_module(sys.argv[1])
    mod.main(sys.argv[2:])
