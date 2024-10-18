from benchmarking_asv import example_module


class TimeSuite:  # pylint: disable=too-few-public-methods
    """An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python."""

    def __init__(self):
        self.d = {}

    def setup(self):
        self.d = {}
        for x in range(500):
            self.d[x] = None

    def time_keys(self):
        """Time first method."""
        example_module.run_time_computation()

    def time_iterkeys(self):
        """Time second method."""
        example_module.run_time_computation()

    def time_range(self):
        """Time third method."""
        example_module.run_time_computation()

    def time_xrange(self):
        """Time fourth method."""
        example_module.run_time_computation()


class MemSuite:  # pylint: disable=too-few-public-methods
    """An example benchmark that times memory consumption."""

    def mem_list(self):
        return example_module.run_mem_computation()
