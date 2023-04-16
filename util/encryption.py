import math

class Encryption:
    def encrypt(self, *args) -> tuple:
        raise NotImplementedError('Must implement encryption')

    def decrypt(self, *args) -> int:
        raise NotImplementedError('Must implement decryption')

    def encrypt_text(self, text: str) -> list:
        if isinstance(text, str):
            bs = text.encode('utf-8') # byte string representing text
        elif isinstance(text, bytes):
            bs = text
        else:
            raise TypeError('Text must be a string or bytes')
        bytes_per_n = 1 # max(self.k // 8, 1)

        # split text into chunks of k bits and convert them to integers
        ints = []
        for i in range(math.ceil(len(bs) / bytes_per_n)):
            byte_substr = bs[i*bytes_per_n : (i+1)*bytes_per_n]
            ints.append(int(byte_substr.hex(), base=16))

        # encrypt the integer representation of text
        return [self.encrypt(i) for i in ints]

    def decrypt_text(self, cypher: list) -> str:
        text = b''

        for (x, *rest) in cypher:
            m = self.decrypt(x, *rest)
            num_bytes = 1 # if m == 1 else math.ceil(math.log(m)/math.log(256))
            text += m.to_bytes(num_bytes, 'big')

        try:
            return text.decode('utf-8')
        except UnicodeDecodeError:
            return text
