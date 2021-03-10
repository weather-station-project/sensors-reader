from abc import ABC, abstractmethod


class SamplesDuringTimeDevice(ABC):
    """Base class for devices which take samples after a period time"""

    @abstractmethod
    def get_sample(self):
        pass
