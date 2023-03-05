# elgamal

Basic implementation of naive ElGamal cryptosystem.

## Usage

```
# Help
$ python3.9 main.py -h

# Generate crypto keys
$ python3.9 main.py gen_keys <n_bits> <certainty> <pubkeys_file> <privkey_file>

# Encrypt file
$ python3.9 main.py gen_keys <pubkeys_file> <plaintext_file> <encrypted_file>

# Decrypt file
$ python3.9 main.py decrypt <pubkeys_file> <privkey_file> <encrypted_file> <decrypted_file>
```
