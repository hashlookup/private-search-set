# Private Search Set (PSS)

Private Search Set (PSS) is an extension to [standard Bloom filter](https://github.com/hashlookup/fleur) to describe and share private set.

## Features

- Fast lookup of values (such as indicators, hashes or any text) without disclosing the values
- Easily distribute private sets to a group of users or organisations
- Watermarking and tracking down potential leak of a private search set (PSS)
- Offline private search
- Flexible meta-format to describe and extend the private search set (PSS)

## Meta format

|Key name|Type|Description|Required|
|:-------|:----|:---|:---:|
|`version`|`number`|Version of the Private Search Set (PSS)|&check;|
|`description`|`string`|Human readable description of the set |&check;|
|`algorithm`|`string`|Keyed-hash message authentication. Available:<br/> - Blake2b<br/> - Blake3<br/> - HMAC-SHA-256<br /> - HMAC-SHA-512  |&check;|
|`keyid`|`string`|The reference to the key used in the keyed-hash message authentication algorithm.|&check;|
|`misp-attribute-types`|`array`|Array of `string` with the types covered by the private search set. Types can be any from types [mentioned in the default MISP types](https://www.circl.lu/doc/misp/categories-and-types/#types). If not specified, all types are covered.|-|
|`canonicalization-format`|`string`|Meta function used expressed in Python functions. Such as `lower()[:10]`|-|
|`openpgp-encrypted-key`|`string`|Base64 OpenPGP message encrypting the reference `keyid`. This is optional as the key can be distributed in different means such as dedicated MISP API key or other secure channel.|-|

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
