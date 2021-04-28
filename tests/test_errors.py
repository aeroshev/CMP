import os
from typing import Iterator, Tuple

import pytest
from _pytest.fixtures import SubRequest

from cmp.grammar import Parser

MATLAB_SAMPLES = './error_samples/'


@pytest.fixture(params=[
    (os.path.join(MATLAB_SAMPLES, 'error_sample_1.matlab'), 3)
])
def sample(request: SubRequest) -> Iterator[Tuple[str, int]]:
    with open(request.param[0], "r") as matlab_file:
        matlab_str = matlab_file.read()
        yield matlab_str, request.param[1]


def test_traverse(sample: Tuple[str, int]) -> None:
    matlab_str, qty_err = sample
    parser = Parser(yacc_debug=False)
    parser.parse(text=matlab_str, debug_level=False)
    assert len([_ for _ in parser.errors()]) == qty_err
