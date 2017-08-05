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
import optparse
import socket

from lib.FrameProcessor import ProcessFrame


def main(ip, port, out_file, secret):
    # setup the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    frame_handler = ProcessFrame()

    # Set the secret if we have one configured
    if secret:
        frame_handler.set_secret(secret)

    print '[INFO] Fake DNS server listening on', ip, '/', port, 'with a configured secret.' if secret else ''

    # if we have a file destination to write to, set it
    if out_file:
        frame_handler.set_outfile(out_file)

    # Start a never ending loop and receive the UDP frames in sock
    # From: http://code.activestate.com/recipes/491264-mini-fake-dns-server/
    while True:

        # read the socket
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes

        # Determine the OPCODE for the query.
        op_code = (ord(data[2]) >> 3) & 15

        # OPCODE 0 == Standard query http://www.networksorcery.com/enp/protocol/dns.htm#Opcode
        if op_code == 0:

            # the raw packet has the name we are querying starting at byte 12
            byte_name_start = 12
            byte_name_length = ord(data[byte_name_start])
            domain = ''

            # set the frame to decode, as we are promarily interested in the
            # first part of the question
            frame_to_decode = data[byte_name_start + 1:byte_name_start + byte_name_length + 1]

            # Continue working with the rest of the request and process a response
            # we will also lookup the state in ProcessFrame to determine the IP
            # response we should be seeing
            while byte_name_length != 0:
                domain += data[byte_name_start + 1:byte_name_start + byte_name_length + 1] + '.'

                byte_name_start += byte_name_length + 1
                byte_name_length = ord(data[byte_name_start])

            print '[INFO] Full resource record query was for:', domain

            # send the frame to the processor
            frame_handler.set_data(frame_to_decode)
            frame_handler.process()

            # prepare the response packet
            response_packet = ''

            if domain:
                response_packet += data[:2] + "\x81\x80"
                response_packet += data[4:6] + data[4:6] + '\x00\x00\x00\x00'  # Questions and Answers Counts
                response_packet += data[12:]  # Original Domain Name Question
                response_packet += '\xc0\x0c'  # Pointer to domain name
                # Response type, ttl and resource data length -> 4 bytes
                response_packet += '\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
                response_packet += str.join('', map(lambda x: chr(int(x)), '127.0.0.1'.split('.')))  # 4bytes of IP

        sock.sendto(response_packet, addr)


if __name__ == '__main__':

    parser = optparse.OptionParser("usage: %prog -L <ip>")
    parser.add_option('-L', '--listen', dest='listen',
                      type='string', help='specify hostname to listen on')
    parser.add_option('-p', '--port', dest='port', default=53,
                      type='int', help='port number to listen on (Defaults: 53)')
    parser.add_option('-O', '--outfile', dest='out', default='',
                      type='string', help='specify a message file destination')
    parser.add_option('-s', '--secret', dest='secret', default=False,
                      action='store_true', help='Set the secret used for the AES encryption')

    (options, args) = parser.parse_args()

    if not options.listen:
        parser.error('At least a listening IP must be provided.')

    if options.secret:
        secret = getpass.getpass(prompt='What is the secret? ')
    else:
        secret = None

    listening_ip = options.listen
    listening_port = options.port
    out_file = options.out

    # kick off the main loop
    main(listening_ip, listening_port, out_file, secret)
