"""An example module containing testing of mock functions."""

from benchmarking_asv import example_module


def test_greetings() -> None:
    """Verify the output of the `greetings` function"""
    output = example_module.greetings()
    assert output == "Hello from LINCC-Frameworks!"


def test_meaning() -> None:
    """Verify the output of the `meaning` function"""
    output = example_module.meaning()
    assert output == 42


def test_run_time_computation() -> None:
    output = example_module.run_time_computation()
    assert 0 <= output <= 4


def test_mem_computation() -> None:
    output = example_module.run_mem_computation()
    assert 0 <= len(output) <= 512
