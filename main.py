from elgamal import ElGamal

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.set_defaults(cmd=None)
    subparsers = parser.add_subparsers(dest='subparser_name')

    gen_keys_parser = subparsers.add_parser('gen_keys')
    gen_keys_parser.add_argument('n_bits', type=int)
    gen_keys_parser.add_argument('certainty', type=int)
    gen_keys_parser.add_argument('pubkeys_file', type=str)
    gen_keys_parser.add_argument('privkey_file', type=str)

    encrypt_parser = subparsers.add_parser('encrypt')
    encrypt_parser.add_argument('pubkeys_file', type=str)
    encrypt_parser.add_argument('plaintext_file', type=str)
    encrypt_parser.add_argument('encrypted_file', type=str)

    decrypt_parser = subparsers.add_parser('decrypt')
    decrypt_parser.add_argument('pubkeys_file', type=str)
    decrypt_parser.add_argument('privkey_file', type=str)
    decrypt_parser.add_argument('encrypted_file', type=str)
    decrypt_parser.add_argument('decrypted_file', type=str)

    args = parser.parse_args()

    if args.subparser_name == 'gen_keys':
        e = ElGamal(args.n_bits, num_checks=args.certainty)

        with open(args.pubkeys_file, 'w') as f:
            f.write(' '.join(map(str, e.pub_keys)))
        with open(args.privkey_file, 'w') as f:
            f.write(str(e.private_key))

    elif args.subparser_name == 'encrypt':
        with open(args.pubkeys_file, 'r') as f:
            pub_keys = tuple(map(int, f.read().split()))
        with open(args.plaintext_file, 'r') as f:
            text = f.read()

        e = ElGamal(public_keys=pub_keys)
        encrypted = e.encrypt_text(text)
        with open(args.encrypted_file, 'w') as f:
            f.write('\n'.join(map(lambda e: f"{e[0]} {e[1]}", encrypted)))

    elif args.subparser_name == 'decrypt':
        with open(args.pubkeys_file, 'r') as f:
            pub_keys = tuple(map(int, f.read().split()))
        with open(args.privkey_file, 'r') as f:
            priv_key = int(f.read())

        with open(args.encrypted_file, 'r') as f:
            encrypted = f.readlines()
        encrypted = [tuple(map(int, line.split())) for line in encrypted]

        e = ElGamal(public_keys=pub_keys, a=priv_key)
        decrypted = e.decrypt_text(encrypted)

        with open(args.decrypted_file, 'w') as f:
            f.write(decrypted)

    else:
        parser.print_help()
