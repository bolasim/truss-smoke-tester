from copier import run_copy
from pathlib import Path
from tempfile import TemporaryDirectory
import truss
from truss.cli import push as truss_push
import subprocess
import sys

import requests

from datetime import datetime, timedelta


PYTHON_VERSION = {
    "py38",
    # "py39",
    # "py310",
    # "py311",
}

USE_GPU = {
    True,
    # False,
}

ACCELERATORS = {
    "T4",
    # "A10G",
    # "A100",
}

TRUSS_VERSION_UNDER_TEST = truss.__version__

TEMPLATE_DIR = Path(__file__).parent.parent / "copier_truss_template"

REQURED_SUCCESSUL_PREDICTS = 50
MAX_BUILD_TIME_SECONDS = 600

project_count = 0

def generate_and_push_truss(data: dict):
    global project_count
    project_count += 1
    project_name = "_".join(
        [
            TRUSS_VERSION_UNDER_TEST,
            *list(
                map(
                    str,
                    data.values(),
                )
            ),
        ]
    )
    print(project_name)
    data["project_name"] = project_name
    with TemporaryDirectory() as truss_parent_dir:
        run_copy(str(TEMPLATE_DIR), truss_parent_dir, data)
        # TODO: run truss push and wait on predict
        for draft in [True]:# , False]:
            model_name=f"{project_name}_{'Draft' if draft else 'Published'}"
            print(model_name)
            subprocess.check_output(
                f"truss push {truss_parent_dir}/{project_name} --remote=baseten-staging --model-name={model_name} --publish={not draft}",
                stderr=sys.stderr,
                # stdout=sys.stdout,
                shell=True,
            )
            # start_build_time = datetime.now()
            # first_predict_pass = False
            # while not first_predict_pass and (datetime.now() - start_build_time) < timedelta(seconds=MAX_BUILD_TIME_SECONDS):
            #     res = 
            
        


def run():
    for py_version in PYTHON_VERSION:
        data = {"python_version": py_version}
        for use_gpu in USE_GPU:
            data["use_gpu"] = use_gpu
            if use_gpu:
                for acc in ACCELERATORS:
                    data["accelerator"] = acc
                    generate_and_push_truss(data)
            else:
                data["accelerator"] = "null"
                generate_and_push_truss(data)
    print(project_count)

