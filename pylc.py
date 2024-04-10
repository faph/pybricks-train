import gc
from pybricks.tools import StopWatch, wait

current_scan_time = 0


class ScanTimer:
    def __init__(self, target_scan_time_ms):
        gc.collect()
        gc.disable()
        self.stopwatch = StopWatch()
        self._target_scan_time_ms = target_scan_time_ms

    def __enter__(self):
        self.stopwatch.reset()

    def __exit__(self, exc_type, exc_value, traceback):
        global current_scan_time
        gc.collect()
        execution_time = self.stopwatch.time()
        wait(max(0, self._target_scan_time_ms - execution_time))
        current_scan_time = self.stopwatch.time()
