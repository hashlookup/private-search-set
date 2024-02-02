import json 
import os
import sys
import hashlib
from flor import BloomFilter

class PrivateSearchSet:
    def __init__(self, algorithm, bloomfilter, canonicalization_format, description, generated_timestamp, keyid, misp_attribute_types, version):
        self.algorithm = algorithm
        self.bloomfilter = bloomfilter
        self.canonicalization_format = canonicalization_format
        self.description = description
        self.generated_timestamp = generated_timestamp
        self.keyid = keyid
        self.misp_attribute_types = misp_attribute_types
        self.version = version

    def print_private_search_set(private_search_set):
        print("Algorithm:", private_search_set.algorithm)
        print("Bloomfilter:", private_search_set.bloomfilter)
        print("Canonicalization Format:", private_search_set.canonicalization_format)
        print("Description:", private_search_set.description)
        print("Generated Timestamp:", private_search_set.generated_timestamp)
        print("Key ID:", private_search_set.keyid)
        print("MISP Attribute Types:", private_search_set.misp_attribute_types)
        print("Version:", private_search_set.version)

    def load_from_json_specs(json_file):
        with open(json_file) as file:
            json_data = json.load(file)
            data = {k.replace('-', '_'): v for k, v in json_data.items()}
            pss = PrivateSearchSet(**data)  # Create an instance of the PrivateSearchSet class
        if set(data.keys()) == set(pss.__dict__.keys()):
            PrivateSearchSet.print_private_search_set(pss)
            return pss
        else:
            raise ValueError("JSON file does not match the expected format.")
    
    def init_filter(self):
        if self.bloomfilter['format'] == 'dcso-v1':
            self._bf = BloomFilter(n=self.bloomfilter['capacity'], p=self.bloomfilter['fp-probability'])
        else:
            raise ValueError("Bloomfilter format not supported.")

    def ingest_stdin(self):
        # Read bytes from stdin  
        self._ps = set()
        for line in sys.stdin.buffer.read().splitlines():  
            if self.bloomfilter['format'] == 'dcso-v1':
                self._bf.add(line)
            if self.algorithm == 'Blake2':
                # TODO use a salt
                self._ps.add(hashlib.blake2b(line, key=self.keyid.encode()).hexdigest())
        
    def write_to_files(self, pss_home):
        if not os.path.exists(pss_home):
            os.makedirs(pss_home)
        # Write the bloom filter
        file_path = os.path.join(pss_home, 'private-search-set.bloom')
        with open(file_path, 'wb') as f:
            self._bf.write(f)
        # Write the JSON file
        file_path = os.path.join(pss_home, 'private-search-set.json')
        with open(file_path, 'w') as f:
            export = {k: v for k, v in self.__dict__.items() if k.startswith('_') != True}
            f.write(json.dumps(export))
        # Write the private search file
        file_path = os.path.join(pss_home, 'private-search-set.pss')
        with open(file_path, 'w') as f:
            for ps in self._ps:
                f.write(f"{ps}\n")