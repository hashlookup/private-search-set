import poppy
import pdb
from private_search_set.bloom_filter_base import BloomFilterBase

class BloomFilterPoppy(BloomFilterBase):
    def __init__(self, parameters):
        super().__init__(parameters)
        if "path" in parameters.keys():
            self.bf = poppy.load(parameters['path'])
        elif parameters['format'] == 'dcso-v1':
            self.bf = poppy.BloomFilter(parameters['capacity'], parameters['fp-probability'])
        elif parameters['format'] == 'poppy-v2':
            self.bf = poppy.with_version(2, parameters['capacity'], parameters['fp-probability'])

    def add(self, data):
        self.bf.insert_bytes(data)
        pass

    def check(self, data):
        self.bf.contains_bytes(data)
        pass
        # return data in self.bf

    # requires a path
    def load(self, path):
        self.bf = poppy.load(path)
        if self.bf.N == 0:
            self.loaded = False
        else:
            self.loaded = True
        pass

    # requires a path
    def write(self, path):
        self.bf.save(path)
        pass