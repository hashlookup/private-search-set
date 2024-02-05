import json 
import os
import sys
import hashlib
from private_search_set.bloom_filter_dcso import BloomFilterDCSO

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
            # PrivateSearchSet.print_private_search_set(pss)
            pss.init_filter_and_set()
            return pss
        else:
            raise ValueError("JSON file does not match the expected format.")
    
    def load_from_pss_home(pss_home):
        if os.path.exists(pss_home):
            file_path = os.path.join(pss_home, 'private-search-set.json')
            if os.path.exists(file_path):
                pss = PrivateSearchSet.load_from_json_specs(file_path)
            else:
                raise ValueError("No JSON file found in the PSS home.")
        file_path = os.path.join(pss_home, 'private-search-set.bloom')
        pss.load_bf_from_file(file_path) 
        file_path = os.path.join(pss_home, 'private-search-set.pss')
        pss._ps = pss.load_pss_from_file(file_path) 
        return pss
    
    def load_bf_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                self._bf.load(f)
    
    def load_pss_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return set(f.read().splitlines())
        else:
            return None
    
    def init_filter_and_set(self):
        # init bloom filter
        if self.bloomfilter['format'] == 'dcso-v1':
            self._bf = BloomFilterDCSO(self.bloomfilter)
        else:
            raise ValueError("Bloomfilter format not supported.")
        
        # init the private search set
        self._ps = set()

    def ingest_stdin(self):
        # Read bytes from stdin  
        for line in sys.stdin.buffer.read().splitlines():  
            self.ingest(line)
   
    def ingest(self, data):
        # HMAC the data
        hashed = b''
        if self.algorithm == 'Blake2':
            # TODO Use a salt
            # TODO We use the keyid as the key for the time being
            hashed_string = hashlib.blake2b(data, key=self.keyid.encode()).hexdigest()
            hashed_bytes = hashed_string.encode()
        else:
            raise ValueError("HMAC algorithm not supported.")

        # add the string digest to the private search set
        self._ps.add(hashed_string)
        # add the utf8 encoded bytes representation of the hexdigest to the bloom filter
        if self.bloomfilter['format'] == 'dcso-v1':
            self._bf.add(hashed_bytes)

    def check_stdin(self):
        # Read bytes from stdin  
        for line in sys.stdin.buffer.read().splitlines():  
            # check hashset in priority
            if self._ps != None:
                if self.check_pss(line):
                    print(line)
            elif self._bf.loaded:
                if self.check_bf(line):
                    print(line)
            else:
                raise ValueError("No private search set or bloom filter loaded.")  
    
    def check_pss(self, data):
        # HMAC the data
        hashed = b''
        if self.algorithm == 'Blake2':
            # TODO Use a salt
            # TODO We use the keyid as the key for the time being
            hashed_string = hashlib.blake2b(data, key=self.keyid.encode()).hexdigest()
        else:
            raise ValueError("HMAC algorithm not supported.")
        if hashed_string in self._ps:
            return True
        else:
            return False
 
    def check_bf(self, data):
        # HMAC the data
        hashed_bytes = b''
        if self.algorithm == 'Blake2':
            # TODO Use a salt
            # TODO We use the keyid as the key for the time being
            hashed_bytes = hashlib.blake2b(data, key=self.keyid.encode()).hexdigest().encode()
        else:
            raise ValueError("HMAC algorithm not supported.")

        if self.bloomfilter['format'] == 'dcso-v1':
            return self._bf.check(hashed_bytes)
        else:
            raise ValueError("Bloomfilter format not supported.")
 
        
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