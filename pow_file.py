from os import makedirs
from pathlib import Path
from shutil import copy
from subprocess import run
from tempfile import TemporaryDirectory


def pow_build_linux(args):
    """Build pow-runner for linux"""
    srcdir = Path(__file__).parent / "src"
    bindir = Path(__file__).parent / "linux"

    with TemporaryDirectory() as tmpdir:
        run(
            [
                "docker",
                "run",
                "--rm",
                "--volume={}:{}".format(srcdir, "/src"),
                "--volume={}:{}".format(tmpdir, "/dist"),
                "python:3.8.7",
                "bash",
                "-c",
                "pip install pyinstaller && pyinstaller --onefile /src/pow-runner.py",
            ]
        )
        makedirs(bindir, exist_ok=True)
        copy(Path(tmpdir) / "pow-runner", bindir)
