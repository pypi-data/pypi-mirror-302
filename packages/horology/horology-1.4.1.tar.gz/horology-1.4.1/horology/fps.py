from statistics import median
from time import perf_counter as counter


class FPS:
    def __init__(
            self,
            median_filtering_kernel: int = 4,
            moving_average_factor: float = 0.8,
            epsilon: float = 1e-6
    ):
        self.median_filtering_kernel = median_filtering_kernel
        self.moving_average_factor = moving_average_factor
        self.epsilon = epsilon

        self._intervals = []
        self._last = None
        self._fps = None

    def tick(self) -> float:
        now = counter()
        if self._last is not None:
            self._intervals.append(now - self._last)
        self._last = now

        if len(self._intervals) > self.median_filtering_kernel:
            self._intervals = self._intervals[-self.median_filtering_kernel:]

        interval = median(self._intervals) + self.epsilon
        current_fps = 1 / interval
        if self._fps is None:
            self._fps = current_fps
        else:
            self._fps = self.moving_average_factor * self._fps + (1 - self.moving_average_factor) * current_fps

        return self._fps

    # ideas: pause, reset, __repr__ albo __str__