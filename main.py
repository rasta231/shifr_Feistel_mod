import hashlib

class CustomEncryptor:
    def __init__(self, key, secret):
        self.ROUNDS = 8
        self.BLOCKSIZE = 8
        self.BLOCKSIZE_BITS = 64
        self.key = self.key_256(key, secret)

    def encrypt_message(self, message, mode):
        ciphertext = ""
        n = self.BLOCKSIZE  # 8 bytes (64 bits) per block

        # Split message into 64-bit blocks
        message = [message[i: i + n] for i in range(0, len(message), n)]
        length_of_last_block = len(message[-1])

        if length_of_last_block < self.BLOCKSIZE:
            for i in range(length_of_last_block, self.BLOCKSIZE):
                message[-1] += " "

        key_initial = self.key
        for block in message:
            L = [""] * (self.ROUNDS + 1)
            R = [""] * (self.ROUNDS + 1)
            L[0] = block[0:self.BLOCKSIZE // 2]
            R[0] = block[self.BLOCKSIZE // 2:self.BLOCKSIZE]
            for i in range(1, self.ROUNDS + 1):
                L[i] = R[i - 1]
                if mode == "cbc":
                    if i == 1:
                        key = key_initial
                    else:
                        key = self.subkeygen(L[i], key_initial, i)
                R[i] = self.xor(L[i - 1], self.scramble(R[i - 1], i, key))

            ciphertext += (L[self.ROUNDS] + R[self.ROUNDS])

        return ciphertext

    def decrypt_cipher(self, ciphertext, mode):
        message = ""
        n = self.BLOCKSIZE  # 8 bytes (64 bits) per block

        # Split ciphertext into 64-bit blocks
        ciphertext = [ciphertext[i: i + n] for i in range(0, len(ciphertext), n)]

        length_of_last_block = len(ciphertext[-1])

        if length_of_last_block < self.BLOCKSIZE:
            for i in range(length_of_last_block, self.BLOCKSIZE):
                ciphertext[-1] += " "

        key_initial = self.key
        for block in ciphertext:
            L = [""] * (self.ROUNDS + 1)
            R = [""] * (self.ROUNDS + 1)
            L[self.ROUNDS] = block[0:self.BLOCKSIZE // 2]
            R[self.ROUNDS] = block[self.BLOCKSIZE // 2:self.BLOCKSIZE]

            for i in range(8, 0, -1):
                if mode == "cbc":
                    key = self.subkeygen(L[i], key_initial, i)
                    if i == 1:
                        key = key_initial

                R[i - 1] = L[i]
                L[i - 1] = self.xor(R[i], self.scramble(L[i], i, key))

            message += (L[0] + R[0])

        return message

    def key_256(self, key, secret):
        return hashlib.sha256(key.encode('utf-8') + secret.encode('utf-8')).hexdigest()

    def subkeygen(self, s1, s2, i):
        result = hashlib.sha256(s1.encode('utf-8') + s2.encode('utf-8')).hexdigest()
        return result

    def scramble(self, x, i, k):
        encrypted_x = ""
        k_char = k[i % len(k)]  # Get the i-th character of the key (looping if needed)
        for char in x:
            encrypted_char = chr((ord(char) + (i * ord(k_char))) % 256)  # Ensure it stays within 0-255 ASCII range
            encrypted_x += encrypted_char

        return encrypted_x
    @staticmethod
    def xor(s1, s2):
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

    @staticmethod
    def stobin(s):
        return ''.join('{:08b}'.format(ord(c)) for c in s)

    @staticmethod
    def bintoint(s):
        return int(s, 2)

    @staticmethod
    def itobin(i):
        return bin(i)

    @staticmethod
    def bintostr(b):
        n = int(b, 2)
        return ''.join(chr(int(b[i: i + 8], 2)) for i in range(0, len(b), 8))


# def main():
#     key = 'hello'
#     secret = '3f788083-77d3-4502-9d71-21319f1792b6'
#     custom_encryptor = CustomEncryptor(key, secret)
#
#     plaintext = 'wear you mathfdsfsdfsdfdsfdser'
#     encrypted_text = custom_encryptor.encrypt_message(plaintext, 'cbc')
#     print(encrypted_text)
#
#     decrypted_text = custom_encryptor.decrypt_cipher(encrypted_text, 'cbc')
#     print(decrypted_text)
#
#
# if __name__ == "__main__":
#     main()
