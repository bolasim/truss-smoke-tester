from copier import run_copy
from pathlib import Path
from tempfile import TemporaryDirectory

PYTHON_VERSION = {
    "py38",
    "py39",
    "py310",
    "py311",
}

USE_GPU = {
    True,
    False,
}

ACCELERATORS = {
    "T4",
    "A10G",
    "A100",
}

TRUSS_VERSION_UNDER_TEST = "v0.4.10rc9"

TEMPLATE_DIR = Path(__file__).parent.parent / "copier_truss_template"


def generate_and_push_truss(data: dict):
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
    data["project_name"] = project_name
    with TemporaryDirectory() as truss_parent_dir:
        run_copy(str(TEMPLATE_DIR), truss_parent_dir, data)
        # TODO: run truss push and wait on predict


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
