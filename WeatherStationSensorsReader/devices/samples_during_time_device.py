from abc import ABC, abstractmethod


class SamplesDuringTimeDevice(ABC):
    """Base class for devices which take samples for a period time"""

    SAMPLES_DURATION_IN_SECONDS = 10

    @abstractmethod
    def get_sample(self):
        pass

    @abstractmethod
    def health_check(self):
        raise NotImplementedError('A sub-class must be implemented.')
