<img width="800" alt="screen shot 2017-07-23 at 1 48 48 pm" src="https://user-images.githubusercontent.com/50654/28538157-16095534-7062-11e7-8efe-f53c750faa76.png">

## Description

EGRESSION is a tool that provides an instant view of how easy it is to upload sensitive data from any given network.

It starts with a sensitive file with these contents, which is stored locally in plaintext. This file is used to test the egress / DLP controls on the network.

- //US Social
- 567-24-4901
- //Credit card numbers
- 4111111111111111
- 5105105105105100
- 4222222222222
- //Dates of birth
- 12.12.94
- 12/12/1994
- 12/12/94
- 12 July 1994
- //Canadian SIN
- 202 275 186
- //UK National Insurance Number (NINO)
- ST 68 86 80 B

## Testing procedure

<img width="600" alt="screen shot 2017-07-24 at 11 30 06 am" src="https://user-images.githubusercontent.com/50654/28538557-7a4cea46-7063-11e7-9c05-001be31b2ab3.png">

It has four (4) levels of testing.

1. INFORMATIONAL: Tells you if it can connect to ports ont he internet.
2. LEVEL 0: Tells you if it can FTP a file to the internet in cleartext.
3. LEVEL 1: Tells you if it can SCP files to the internet over various ports.
4. LEVEL 2: Tells you if it can send the same sensitive file to the internet via DNS queries.

It does each of these in succession and then reports on which levels it failed to block.

<img width="750" alt="screen shot 2017-07-24 at 11 27 51 am" src="https://user-images.githubusercontent.com/50654/28538460-2b3d39d8-7063-11e7-8438-b13e275c4786.png">

## Installation

The tool is made to be as self-contained as possible and easy to run. You can install the dependencies like so:

1. Ensure you have <code>python</code> installed.
2. Ensure you have <code>curl</code> installed.
3. Ensure you have <code>nc</code> installed.

NOTE: Most of these are installed natively on both MacOS and Linux.

## Presentations

- Blackhat Arsenal 2017

## Next Steps

Plans for the project include:

- Adding additional levels, with additional egress methods, e.g.: sending data over NTP, ICMP, etc.
- Additional fault checking for various scenarios

## Credits and Thanks

- Hat tip to William Coppola for previous and complementary work he's done in this space with his Fillabuster tool, which he also presented at BlackHat Arsenal back in 2015.
- Thanks to Sasa Zdjelar and Jason Haddix for giving feedback on the tool.
