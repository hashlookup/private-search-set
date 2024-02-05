from abc import ABC, abstractmethod

class BloomFilterBase(ABC):
    @abstractmethod
    def __init__(self, parameters):
        """Initialize the Bloom filter with given parameters."""
        loaded = False
        pass

    @abstractmethod
    def add(self, data):
        """Add data to the Bloom filter."""
        pass

    @abstractmethod
    def check(self, data):
        """Load a Bloom filter from file."""
        pass

    @abstractmethod
    def load(self, data):
        """Load a Bloom filter from file."""
        pass

    @abstractmethod
    def write(self):
        """Write the serialized bloom filter to a file descriptor."""
        pass
