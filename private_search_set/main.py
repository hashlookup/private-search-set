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
