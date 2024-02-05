from flor import BloomFilter
from private_search_set.bloom_filter_base import BloomFilterBase

class BloomFilterDCSO(BloomFilterBase):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.bf = BloomFilter(n=parameters['capacity'], p=parameters['fp-probability'])

    def add(self, data):
        self.bf.add(data)
        pass

    def check(self, data):
        return data in self.bf

    def load(self, fd):
        self.bf.read(fd)
        if self.bf.N == 0:
            self.loaded = False
        else:
            self.loaded = True
        pass

    def write(self, fd):
        self.bf.write(fd)
        pass