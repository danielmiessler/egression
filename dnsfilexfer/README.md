dnsfilexfer - File transfers via DNS
===========
Just some code to xfer files via DNS lookups. Supports encrypting the on the wire traffic with a short passphrase and can be used to be parsed purely from the output found in a `tcpdump` using `xxd` and the `-X` flag in the sender.

### Installing
Clone the repo, and install the dependencies as put out in `requirements.txt`:

```
% git clone https://github.com/leonjza/dnsfilexfer.git
% cd dnsfilexfer
% sudo pip install -r requirements.txt
```
In case the installation fails because of `pycrypto`, you might need to install `python-dev` manually.

### Sample Usage:

Assuming the receiver `dns_recv.py` is running (where 192.168.10.1 is the server):
```
% echo "This is a test message that will be sent over DNS\n Cool eh?" > /tmp/message
% cat /tmp/message
This is a test message that will be sent over DNS
Cool eh?

% python dns_send.py --server 192.168.10.1 --file /tmp/message --indentifier dns_message_test --secret
What is the secret?
[INFO] Message is encypted with the secret
---START OF MESSAGE---
/lHsvTZT3nJfQgdtUWSpKDqrpKuK+eLrU3bpAp9aNDJt6K/mwEc8sBUaJybPh7r5h2AOkJVezwBBODSV9hFM8w==
---END OF MESSAGE---
[INFO] Sending lookup for : 00006:10000000000000000000000000000000000000000000000000.fake.io
[INFO] Sending lookup for : 0001646e735f6d6573736167655f7465737400000000000000000000.fake.io
[INFO] Sending lookup for : 00028bf2046ae2144be75d2ce780b3f992e2c368021e.fake.io
[INFO] Sending lookup for : 00032f6c487376545a54336e4a6651676474555753704b447172704b754b.fake.io
[INFO] Sending lookup for : 00042b654c7255336270417039614e444a74364b2f6d7745633873425561.fake.io
[INFO] Sending lookup for : 00054a796250683772356832414f6b4a56657a7742424f4453563968464d.fake.io
[INFO] Sending lookup for : 000638773d3d.fake.io
[INFO] Sending lookup for : 00000000000000000000000000000000000000000000000000000000.fake.io
[INFO] Message sent in 8 requests
```

On the server/receiver
```
% sudo python dns_recv.py --listen 0.0.0.0 --secret
Password:
What is the secret?
[INFO] Fake DNS server listening on 0.0.0.0 / 53 with a configured secret.
[INFO] Full resource record query was for: 00006:10000000000000000000000000000000000000000000000000.fake.io.
[INFO] Processing frame 00006:10000000000000000000000000000000000000000000000000
[INFO] Full resource record query was for: 0001646e735f6d6573736167655f7465737400000000000000000000.fake.io.
[INFO] Processing frame 0001646e735f6d6573736167655f7465737400000000000000000000
[INFO] Full resource record query was for: 00028bf2046ae2144be75d2ce780b3f992e2c368021e.fake.io.
[INFO] Processing frame 00028bf2046ae2144be75d2ce780b3f992e2c368021e
[INFO] Full resource record query was for: 00032f6c487376545a54336e4a6651676474555753704b447172704b754b.fake.io.
[INFO] Processing frame 00032f6c487376545a54336e4a6651676474555753704b447172704b754b
[INFO] Full resource record query was for: 00042b654c7255336270417039614e444a74364b2f6d7745633873425561.fake.io.
[INFO] Processing frame 00042b654c7255336270417039614e444a74364b2f6d7745633873425561
[INFO] Full resource record query was for: 00054a796250683772356832414f6b4a56657a7742424f4453563968464d.fake.io.
[INFO] Processing frame 00054a796250683772356832414f6b4a56657a7742424f4453563968464d
[INFO] Full resource record query was for: 000638773d3d.fake.io.
[INFO] Processing frame 000638773d3d
[INFO] Full resource record query was for: 00000000000000000000000000000000000000000000000000000000.fake.io.
[INFO] Processing frame 00000000000000000000000000000000000000000000000000000000
[OK] Message seems to be intact and passes sha1 checksum of 8bf2046ae2144be75d2ce780b3f992e2c368021e
[OK] Message was received in 8 requests
[INFO] Message has been decrypted with the configured secret
Message identifier: dns_message_test

---START OF MESSAGE---
This is a test message that will be sent over DNS
Cool eh?

---END OF MESSAGE---
```

### Options
#### Sender (dns_send.py)
  `-S` SERVER, `--server`=SERVER specify dns server to send requests to  
  `-F` FILE, `--file`=FILE specify the file to send  
  `-I` IDENT, `--indentifier`=IDENT specify a message indentifier  
  `-X`, `--xxd` Enable questions to be `xxd -r` friendly (60 charslong)  
  `-s`, `--secret` Set the secret used for the AES encryption  
  `-d` DOMAIN, `--domain`=DOMAIN fake zone to use for generated lookups  
  
#### Receiver (dns_recv.py)
  `-L` LISTEN, `--listen`=LISTEN specify hostname to listen on  
  `-p` PORT, `--port`=PORT port number to listen on (Defaults: 53)  
  `-O` OUT, `--outfile`=OUT specify a message file destination  
  `-s`, `--secret` Set the secret used for the AES encryption

[Blog Entry](https://leonjza.github.io/2014/03/11/dnsfilexfer-yet-another-take-on-file-transfer-via-dns/)
Contact: [@leonjza](https://twitter.com/leonjza)
