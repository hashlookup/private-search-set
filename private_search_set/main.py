import json 
import os
from flor import BloomFilter
import sys

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

    def ingest_stdin(self):
        if self.bloomfilter['format'] == 'dcso-v1':
            self.bf = BloomFilter(n=self.bloomfilter['capacity'], p=self.bloomfilter['fp-probability'])
            # Read bytes from stdin  
            for line in sys.stdin.buffer.read().splitlines():  
                self.bf.add(line)
        else:
            raise ValueError("Bloomfilter format not supported.")
        
    def write_to_files(self, pss_home):
        if not os.path.exists(pss_home):
            os.makedirs(pss_home)
        file_path = os.path.join(pss_home, 'private-search-set.bloom')
        with open(file_path, 'wb') as f:
            self.bf.write(f)


# Example usage:
# json_data = {
#     "algorithm": "Blake2",
#     "bloomfilter": {
#         "capacity": 10000,
#         "format": "dcso-v1",
#         "fp-probability": 0.001
#     },
#     "canonicalization-format": ".lower",
#     "description": "List of Tor hidden services to filter",
#     "generated-timestamp": 1700731642,
#     "keyid": "tor-csam-lea",
#     "misp-attribute-types": [
#         "text",
#         "url",
#         "link"
#     ],
#     "version": 1
# }

# private_search_set = PrivateSearchSet(**json_data)
