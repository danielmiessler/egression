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

import hashlib
import os.path

from Crypt import CryptString


class ProcessFrame:
    def __init__(self):
        self.position = 0
        self.expected = 0
        self.framestore = []
        self.out_file = ''
        self.secret = None
        self.encrypted = False
        self.identifier = None

        # Other defaults
        self.frame = None
        self.checksum = None

    def set_outfile(self, out_file):
        self.out_file = out_file

    def set_data(self, frame):
        self.frame = frame

    def set_secret(self, secret):
        if secret:
            self.secret = secret

    def process(self):
        print '[INFO] Processing frame', self.frame

        try:
            frame_pos = int(self.frame[0:4])
        except Exception, e:
            print '[CRITICAL] Unable to determine a position. Error:', str(e)
            print '[CRITICAL] Maybe we are not getting a message really or `-X` was used with the sender.'
            return

        # first of all, check of this is not the last frame
        if len(str(self.frame).replace('0', '')) == 0:

            # check that we got all of the parts of the message
            if self.expected <> self.position:
                print '[ERROR] EOF received but complete message was not received.'
                print '[ERROR] Expected:', self.expected
                print '[ERROR] Position:', self.position
                return

            # merge the payloads, and checksum the result
            combined_payloads = ''.join(self.framestore).decode('hex')
            checksum = hashlib.sha1(combined_payloads).hexdigest()

            if self.checksum == checksum:

                print '[OK] Message seems to be intact and passes sha1 checksum of', self.checksum
                print '[OK] Message was received in', self.expected + 2, 'requests'

                # check if self.encrypted & if a key is available.
                # if so, decrypt combined_payloads
                if self.encrypted:
                    if not self.secret:
                        print '[CRITICAL] Message is encrypted, but no secret is available. Set one with `-s`'
                        return

                    # decrypt the message
                    d = CryptString(self.secret)
                    combined_payloads = d.decode(combined_payloads)
                    if not combined_payloads:
                        print '[ERROR] Encrypted message failed to decode'
                        return

                    print '[INFO] Message has been decrypted with the configured secret'

                # if we need to write this too a file, do it
                if self.out_file:
                    print '[OK] Writing contents to', self.out_file

                    # check if self.out_file already exists.
                    if os.path.isfile(self.out_file):
                        print '[INFO]', self.out_file, 'already exists.'

                        if self.identifier:
                            self.out_file = self.out_file + '-' + self.identifier
                        else:
                            self.out_file = self.out_file + '-' + self.checksum[:8]

                    # open the file and write the message
                    print '[INFO] Writing to', repr(os.path.abspath(self.out_file))

                    with open(os.path.abspath(str(self.out_file)), 'w') as f:
                        f.write(combined_payloads)

                    print '[OK] Done writing contents to', self.out_file

                # else, just print it
                else:
                    print 'Message identifier:', self.identifier, '\n'
                    print '---START OF MESSAGE---'
                    print combined_payloads
                    print '---END OF MESSAGE---'

            else:
                print '[CRITICAL] Message does not pass checksum validation. Receive Failed.'
                self.position = 0
                self.expected = 0
                self.framestore = []

            return

        # new input starting, read the amount of expected frames
        if frame_pos == 0:
            # split by : and and get the number of extected frames, minus this one
            self.expected = int(self.frame.split(':')[0])

            # check if the received message will be encrypted
            if int((self.frame.split(':')[1])[:1]) == 1:
                self.encrypted = True

            self.position = 0
            self.framestore = []
            self.identifier = None
            return

        # set the identifier and stip null bytes \x00
        if frame_pos == 1:
            ident = (self.frame[4:].decode('hex')).split(b'\0', 1)[0]
            if ident == 'None':
                self.identifier = None
                return

            self.identifier = ident
            return

        # get the sha1hash of the end message we will be getting
        if frame_pos == 2:
            self.checksum = self.frame[4:]
            self.position = frame_pos
            return

        # if the current frame value is the stored one + 1, then this is the next one
        # to record, do it
        if frame_pos == self.position + 1:
            self.position = frame_pos
            self.framestore.append(self.frame[4:])
            return

        print '[WARNING]: Out of sync frames received! We are expecting frame', self.position + 1, 'but got', frame_pos
