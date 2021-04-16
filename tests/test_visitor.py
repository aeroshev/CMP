import os
from typing import Iterator, Tuple

import pytest
from _pytest.fixtures import SubRequest

from cmp.ast import FileAST
from cmp.grammar import Parser
from cmp.traverse import Visitor

MATLAB_SAMPLES = './matlab_samples/'
PYTHON_OUTPUT = './python_output/'


@pytest.fixture(params=[
    (os.path.join(MATLAB_SAMPLES, 'sample_1.m'), os.path.join(PYTHON_OUTPUT, 'output_sample_1.py')),
    (os.path.join(MATLAB_SAMPLES, 'sample_2.m'), os.path.join(PYTHON_OUTPUT, 'output_sample_2.py')),
    (os.path.join(MATLAB_SAMPLES, 'sample_3.m'), os.path.join(PYTHON_OUTPUT, 'output_sample_3.py')),
    (os.path.join(MATLAB_SAMPLES, 'sample_4.m'), os.path.join(PYTHON_OUTPUT, 'output_sample_4.py')),
    (os.path.join(MATLAB_SAMPLES, 'sample_5.m'), os.path.join(PYTHON_OUTPUT, 'output_sample_5.py')),
    (os.path.join(MATLAB_SAMPLES, 'sample_6.m'), os.path.join(PYTHON_OUTPUT, 'output_sample_6.py')),
    (os.path.join(MATLAB_SAMPLES, 'sample_7.m'), os.path.join(PYTHON_OUTPUT, 'output_sample_7.py')),
    (os.path.join(MATLAB_SAMPLES, 'sample_8.m'), os.path.join(PYTHON_OUTPUT, 'output_sample_8.py'))
])
def sample(request: SubRequest) -> Iterator[Tuple[str, str]]:
    with open(request.param[0], "r") as matlab_file, open(request.param[1], "r") as python_file:
        matlab_str = matlab_file.read()
        python_str = python_file.read()

        yield matlab_str, python_str


@pytest.fixture
def ast(sample: Tuple[str, str]) -> FileAST:
    matlab_input, _ = sample
    parser = Parser(yacc_debug=False)
    ast = parser.parse(text=matlab_input, debug_level=False)
    return ast


def test_traverse(sample: Tuple[str, str], ast: FileAST) -> None:
    _, python_output = sample
    visitor = Visitor()
    res_string = visitor.traverse_ast(root=ast)

    assert res_string == python_output
