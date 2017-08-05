# The MIT License (MIT)
#
# Copyright (c) 2014-2016 Leon Jacobs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 16

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING


class CryptString:
    """Encryption with AES-128 in CBC mode and random IV plus HMAC-SHA256
    authentication with encrypt-then-MAC method. The key material is derived
    from a password with PBKDF2. Each message uses a newly derived key."""

    def __init__(self, secret):
        # pad the secret to match our block size
        self.secret = secret.ljust(BLOCK_SIZE, PADDING)
        # RNG
        self.rng = Random.new()

    def _gen_keys(self, salt):
        keys = PBKDF2(self.secret, salt, BLOCK_SIZE * 2)
        key_enc = keys[0:BLOCK_SIZE]
        key_auth = keys[BLOCK_SIZE:]

        return key_enc, key_auth

    def encode(self, string):
        iv = self.rng.read(BLOCK_SIZE)

        key_enc, key_auth = self._gen_keys(iv)
        mac = HMAC.new(key_auth, digestmod=SHA256.new())
        cipher = AES.new(key_enc, AES.MODE_CBC, iv)

        ctext = cipher.encrypt(pad(string))
        mac.update(ctext + iv)
        auth = mac.digest()
        return base64.b64encode(iv + auth + ctext)

    def decode(self, string):
        if len(string) < (BLOCK_SIZE * 2 + 32):
            return None

        data = base64.b64decode(string)
        iv = data[0:BLOCK_SIZE]
        auth = data[BLOCK_SIZE:BLOCK_SIZE+32]
        ctext = data[BLOCK_SIZE+32:]
        key_enc, key_auth = self._gen_keys(iv)
        cipher = AES.new(key_enc, AES.MODE_CBC, iv)
        mac = HMAC.new(key_auth, digestmod=SHA256.new())

        mac.update(ctext + iv)
        auth_c = mac.digest()
        if auth_c != auth:
            return None

        ptext = cipher.decrypt(ctext).rstrip(PADDING)
        return ptext
