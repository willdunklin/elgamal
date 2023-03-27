from elgamal import ElGamal
from ec_elgamal import ElGamalEC
import argparse

def read_pub_keys(file):
    with open(file, 'r') as f:
        vals = f.read().split()
    pub_keys = []
    # Read all ints, except for strings that aren't ints
    for v in vals:
        try:
            pub_keys.append(int(v))
        except ValueError:
            pub_keys.append(v)
    return tuple(pub_keys)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.set_defaults(cmd=None)
    parser.add_argument('enc_type', type=str, help='Type of encryption to use: (elgamal, ec_elgamal)')

    subparsers = parser.add_subparsers(dest='subparser_name')

    gen_keys_parser = subparsers.add_parser('gen_keys', help='Generate ElGamal public/private keys')
    gen_keys_parser.add_argument('n_bits', type=int, help='Number of bits in P')
    gen_keys_parser.add_argument('certainty', type=int, help='Certainty of the Miller-Rabin algorithm (100 is reasonable)')
    gen_keys_parser.add_argument('pubkeys_file', type=str, help='File to write public keys to')
    gen_keys_parser.add_argument('privkey_file', type=str, help='File to write private key to')

    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file using ElGamal')
    encrypt_parser.add_argument('pubkeys_file', type=str, help='File containing public keys')
    encrypt_parser.add_argument('plaintext_file', type=str, help='File containing plaintext to encrypt')
    encrypt_parser.add_argument('encrypted_file', type=str, help='File to write encrypted text to')

    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file using ElGamal')
    decrypt_parser.add_argument('pubkeys_file', type=str, help='File containing public keys')
    decrypt_parser.add_argument('privkey_file', type=str, help='File containing private key')
    decrypt_parser.add_argument('encrypted_file', type=str, help='File containing encrypted text')
    decrypt_parser.add_argument('decrypted_file', type=str, help='File to write decrypted text to')

    args = parser.parse_args()

    if args.enc_type == 'elgamal':
        Enc = ElGamal
    elif args.enc_type == 'ec_elgamal':
        Enc = ElGamalEC

    if args.subparser_name == 'gen_keys':
        e = Enc(k=args.n_bits, num_checks=args.certainty)

        with open(args.pubkeys_file, 'w') as f:
            f.write('\n'.join(map(str, e.pub_keys)))
        with open(args.privkey_file, 'w') as f:
            f.write(str(e.private_key))

    elif args.subparser_name == 'encrypt':
        pub_keys = read_pub_keys(args.pubkeys_file)
        with open(args.plaintext_file, 'r') as f:
            text = f.read()

        e = Enc(public_keys=pub_keys)
        encrypted = e.encrypt_text(text)

        with open(args.encrypted_file, 'w') as f:
            f.write('\n'.join(map(lambda e: f"{e[0]} {e[1]}", encrypted)))

    elif args.subparser_name == 'decrypt':
        pub_keys = read_pub_keys(args.pubkeys_file)
        with open(args.privkey_file, 'r') as f:
            priv_key = int(f.read())

        with open(args.encrypted_file, 'r') as f:
            encrypted = f.readlines()
        encrypted = [tuple(map(int, line.split())) for line in encrypted]

        e = Enc(public_keys=pub_keys, priv_key=priv_key)
        decrypted = e.decrypt_text(encrypted)

        with open(args.decrypted_file, 'w') as f:
            f.write(decrypted)

    else:
        parser.print_help()
