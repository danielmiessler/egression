#!/bin/bash

# Prepare the server
ssh root@tokenscope.com 'rm -rf sensitive.txt'
echo "Deleted the old file…"
ssh root@tokenscope.com 'killall ncat'
echo "Killed the old listener…"
ssh root@tokenscope.com 'ncat -l 1025 > /var/software/Egression/sensitive.txt'

echo "Set up the new listener…"

# Notification
echo "Testing Level 1 Egress Test…"

# Send the file
ncat tokenscope.com 1025 < sensitive.txt

# Check if the file exists

ssh root@tokenscope.com 'sh /var/software/Egression/check.sh'
