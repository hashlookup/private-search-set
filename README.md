# Private Search Set (PSS)

Private Search Set (PSS) is an extension to [standard Bloom filter](https://github.com/hashlookup/fleur) or a standalone hash file to describe and share private set.

## Features

- Fast lookup of values (such as indicators, hashes or any text) without disclosing the values
- Easily distribute private sets to a group of users or organisations
- Watermarking and tracking down potential leak of a private search set (PSS)
- Offline private search
- Flexible meta-format to describe and extend the private search set (PSS)

## Overview of creation and lookup of PSS

~~~~mermaid
flowchart TD
    Y["canonize(foobar.onion)"] --> A
    A["insert keyhashed(foobar.onion)"] -->|key, Blake2| B[key-hashed]
    B --> |insert| C[Distributed PSS file]
    B --> |insert| D[Distributed PSS Bloomfilter]
    style B fill:#0f0,stroke:#333,stroke-width:4px
    style Y fill:#0f0,stroke:#333,stroke-width:4px
    style A fill:#0f0,stroke:#333,stroke-width:4px
    style Z fill:#fff,stroke:#333,stroke-width:4px
    Z["search keyhashed(canonized foobar.onion)"] -->|search| C
    Z["search keyhashed(canonized foobar.onion)"] -->|search| D
~~~~

## Meta format

|Key name|Type|Description|Required|
|:-------|:----|:---|:---:|
|`version`|`number`|Version of the Private Search Set (PSS)|&check;|
|`description`|`string`|Human readable description of the set |&check;|
|`algorithm`|`string`|Keyed-hash message authentication. Available:<br/> - Blake2b<br/> - Blake3<br/> - HMAC-SHA-256<br /> - HMAC-SHA-512  |&check;|
|`keyid`|`string`|The reference to the key used in the keyed-hash message authentication algorithm.|&check;|
|`bloomfilter`|`hash`|The BloomFilter description along with its format and model.|&check;|
|`misp-attribute-types`|`array`|Array of `string` with the types covered by the private search set. Types can be any from types [mentioned in the default MISP types](https://www.circl.lu/doc/misp/categories-and-types/#types). If not specified, all types are covered.|-|
|`canonicalization-format`|`string`|Meta function used expressed in Python functions. Such as `lower()[:10]`|-|
|`openpgp-encrypted-key`|`string`|Base64 OpenPGP message encrypting the reference `keyid`. This is optional as the key can be distributed in different means such as dedicated MISP API key or other secure channel.|-|

### Meta format `bloomfilter`

|Key name|Type|Description|Required|
|:-------|:----|:---|:---:|
|`capacity`|`number`|Capacity of the BloomFilter|&check;|
|`fp-probability`|`number`|Probability of false-positive|&check;|
|`format`|`string`|Format of the BloomFilter such as `dcso-v1` or `circl-v1`|&check;|

#### List of known `bloomfilter` format

|Name|Description|
|:-------|:----|
|`dcso-v1`|DCSO BloomFilter using 64-bit FNV-1 hash function.|
|`circl-v1`|CIRCL BloomFilter using 64-bit XXH3.|

### Sample 

~~~~json
{  
   "misp-attribute-types" : ["text", "url", "link"]
   "description": "List of Tor hidden services containing child sexual abuse material (CSAM)."
   "keyid": "tor-csam-lea"
   "algorithm": "Blake2"
   "canonicalization-format`": ".lower"
   "version": 1
}
~~~~

### Feed format

The feed format is composed of a directory with the following structure:

- `private-search-set.pss` - Private search as a standalone file. `required`
- `private-search-set.json` - Meta data of the private search file. `required`
- `private-search-set.bloom` - Bloomfilter file of the pss set. `required`

Those two files can be included in a MISP feed format export.

### MISP Object template

A private-search-set MISP oject template will be created to be able to share PSS via MISP.

