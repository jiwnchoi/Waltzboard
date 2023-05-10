import time
from typing import Dict


class ExecTimeChecker:
    execution_times: Dict[str, float]

    def __init__(self):
        self.execution_times = {}

    def __str__(self) -> str:
        return "\n".join([f"{k}: {v}" for k, v in self.execution_times.items()])

    def initialize(self):
        """
        Initialize the execution time checker.
        Usage:
            exec_time_checker.initialize()
            print(exec_time_checker)
            >>> (empty)
        """
        self.execution_times = {}

    def record(self, func):
        """
        Decorator to record execution time of a function.
        Args:
            func: Function to be decorated.
        Returns:
            Decorated function.
        Usage:
            @exec_time_checker.record
            def my_function():
                pass
            print(exec_time_checker)
            >>> my_function: 0.000001
        """

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            if func.__name__ not in self.execution_times:
                self.execution_times[func.__name__] = 0
            self.execution_times[func.__name__] += execution_time
            return result

        return wrapper


exec_time_checker = ExecTimeChecker()
