# Private Search Set python library
This library implements the Private Search Set (PSS) concept to facilitate experimentation and hopefully enhance privacy in data sharing. It's aimed at providing a practical approach to manage and check data against privacy-preserving sets.

# Installation
To install the library, clone the repository and install it in editable mode:
```sh
git clone https://github.com/hashlookup/private-search-set.git
cd private-search-set
pip install -e .
```

# Use
Run the private-search-set CLI with the following options:
```sh
Usage: private-search-set [OPTIONS]

Options:
  --pss-home PATH       PSS working folder.  [required]
  --json-file PATH      Path to the PSS JSON file.
  --ingest / --check    ingest or check stdin into/against PSS files[required]
  --bf                  force check against the bloom filter over the hashset
  --key TEXT            specify key content for HMAC operations
  --debug / --no-debug  print debug information
  --help                Show this message and exit.

```

## Ingesting Data
To create and populate a PSS in a directory (e.g., output), use:
```sh
cat tests/word_list.txt | private-search-set --pss-home=output  --ingest --json-file=pss.json
```
(here we use the json metadata sample as `pss.json`)

## Checking Data
To check data against the hashset with `--check`:
```sh
cat tests/word_list.txt | private-search-set --pss-home=output --check
```
Force the use of the Bloom filter with `--check --bf`:

```sh
cat tests/word_list.txt | private-search-set --pss-home=output --check --bf
```
In both case, each line printed to `stdout` is a match.