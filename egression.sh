#!/bin/bash

## Eggresion : Test a newtwork's egress controls, and give levels of success and failure.
## by Daniel Miessler
## July 2017

echo ""
echo "Egression : Test a network's egress controls and give levels of of success and failure."
echo "by Daniel Miessler"
echo "July 2017"

cat << "EOF"
                                                      `my                                           
                                                      yd.                                           
                                                     -h:                                            
                                        -+           .`          +`                                 
                                       `d.        + --          sy                                  
                                       --        +:`/          :d`                                  
                                      .-        `. / :         -`/.                                 
                                      +         + :.-/        -`:s                                  
                                     /`        /`.: -        .: -`                                  
       `.....`    `......`........  --   .....:- +.o-.....   o.//....`...    `..`    `..`    ...    
    `omMMMMMMs .yNMMMMMMM-dMMMMMMMMs` /hMMMMMMM`oNMMMMMMMM.:mMMMMMMMM:hMd  +dMMMMNy- :MMN+   yMm    
   .NMd/-.... :MMs-`..... dMh`...+MM:sMMo-....` NMh.....`` dMd-....`` hMd hMm/.`-sMM::MMMMd- yMm    
   +MMMMMMMMd yMm   +MMMM-dMh+MMMMNs`NMMMMMMMM- /mMMMMMMm/ -dMMMMMMmo hMd.MM/     mMy:MMomMMyhMm    
   .NMm/-.... :MMs.  ./MM-dMh/mMN+   sMMs-....`   `....yMM`  `....oMM-hMd dMm:` .sMM/:MM-`oMMMMm    
    `sNMMMMMMs -yNMMMMMMM-dMh -sNMd:  /dMMMMMMM`MMMMMMMMNo mMMMMMMMMs hMd  +mMMMMNh- :MM-  .hMMm    
       .-----.    .------`.-.`/ /---    `.---o- -------o   -------+-  .-.    `--.    `--`    .-.    
                             + `-           --        -`         `/                                 
                            :.             `/                    +                                  
EOF

[ -e ./results.txt ] && rm -rf ./results.txt
#rm -rf ./results.txt

echo ""
echo ""
echo "$(tput setaf 3)== EGRESSION WILL NOW TEST THIS NETWORK'S EGRESS CONTROLS VS. BOTH CONNECTIONS AND SENSITIVE FILE UPLOADS (DLP). ==$(tput sgr 0)"
echo " "

sleep 1

read -n 1 -s -r -p "Press the ANY key to continue."
echo ""
echo ""

echo "======================================================================================"
echo "$(tput setaf 1)EGRESSION INFORMATIONAL :: $(tput setaf 2)PORT CONNECTIONS$(tput sgr 0)"
echo "======================================================================================"

echo ""
echo "$(tput setaf 3)== THESE ARE THE PORTS EGRESSION CAN CONNECT TO FROM THIS NETWORK TO THE INTERNET. ==$(tput sgr 0)"
echo ""

nc -z -v -w3 54.89.49.208 23 2> /dev/null
if [ $? -eq 0 ]
    then
        echo "CONNECTION SUCCESSFUL :: $(tput setaf 2)23 (TELNET)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" >&2
        echo "INFORMATIONAL : It's possible to connect outbound on at least one major port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "PORT :: $(tput setaf 2)23 (TELNET)-- $(tput setaf 4)PASSED$(tput sgr 0)" >&2
fi

sleep 1

nc -z -v -w3 54.89.49.208 22 2> /dev/null
if [ $? -eq 0 ]
    then
        echo "CONNECTION SUCCESSFUL :: $(tput setaf 2)22 (SSH)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" >&2
        echo "INFORMATIONAL : It's possible to connect outbound on at least one major port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "PORT :: $(tput setaf 2)22 (SSH)-- $(tput setaf 4)PASSED$(tput sgr 0)" >&2
fi

sleep 1

nc -z -v -w3 54.89.49.208 80 2> /dev/null
if [ $? -eq 0 ]
    then
        echo "CONNECTION SUCCESSFUL :: $(tput setaf 2)80 (HTTP)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" >&2
        echo "INFORMATIONAL : It's possible to connect outbound on at least one major port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "PORT :: $(tput setaf 2)80 (HTTP)-- $(tput setaf 4)PASSED$(tput sgr 0)" >&2
fi

sleep 1

nc -z -v -w3 54.89.49.208 443 2> /dev/null
if [ $? -eq 0 ]
    then
        echo "CONNECTION SUCCESSFUL :: $(tput setaf 2)443 (HTTPS)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" >&2
        echo "INFORMATIONAL : It's possible to connect outbound on at least one major port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "PORT :: $(tput setaf 2)443 (HTTPS)-- $(tput setaf 4)PASSED$(tput sgr 0)" >&2
fi

sleep 1

nc -z -v -w3 54.89.49.208 3389 2> /dev/null
if [ $? -eq 0 ]
    then
        echo "CONNECTION SUCCESSFUL :: $(tput setaf 2)3389 (REMOTE DESKTOP)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" >&2
        echo "INFORMATIONAL : It's possible to connect outbound on at least one major port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "PORT :: $(tput setaf 2)3389 (REMOTE DESKTOP)-- $(tput setaf 4)PASSED$(tput sgr 0)" >&2
fi

sleep 1

nc -z -v -w3 54.89.49.208 5900 2> /dev/null
if [ $? -eq 0 ]
    then
        echo "CONNECTION SUCCESSFUL :: $(tput setaf 2)5900 (VNC)-- $(tput setaf 1)CHECK FAILED$(tput sgr 0)" >&2
        echo "INFORMATIONAL : It's possible to connect outbound on at least one major port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "PORT :: $(tput setaf 2)5900 (VNC)-- $(tput setaf 4)PASSED$(tput sgr 0)" >&2
fi

echo " "

echo "=============================================================================="
echo "$(tput setaf 1)EGRESSION Level 0 :: $(tput setaf 2)FTP File Upload$(tput sgr 0)"
echo "=============================================================================="

echo ""
echo "$(tput setaf 3)== IT'S ONE THING TO BE ABLE TO CONNECT TO PORTS. NOW LET'S SEE IF WE CAN UPLOAD FILES. ==$(tput sgr 0)"
echo ""
echo "$(tput setaf 3)== WE HAVE LOCALLY A PLAINTEXT FILE FULL OF JUICY DETAILS, SUCH AS SOCIAL SECURITY NUMBERS, NATIONAL ID NUMBERS, CREDIT CARDS, DATES OF BIRTH, ETC. ==$(tput sgr 0)"
echo ""
echo "$(tput setaf 3)== WE WILL NOW ATTEMPT TO UPLOAD THIS FILE TO THE INTERNET, VIA CLEARTEXT FTP, TO SEE IF THIS NETWORK ALLOWS IT.$(tput sgr 0) =="

sleep 1

read -n 1 -s -r -p "Press the ANY key to continue."

echo ""
echo ""

curl -sT ./sensitive.docx ftp://54.89.49.208 --user egression:EgressionPWD123!
if [ $? -eq 0 ]
    then
        echo "FILE UPLOAD SUCCESSFUL :: $(tput setaf 2)21 (FTP)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" 
        echo "LEVEL 0 FAILURE: It's possible to upload an unencrypted sensitive file from your network without using encryption." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "FILE UPLOAD FAILED :: $(tput setaf 2)21 (FTP)-- $(tput setaf 7)PASSED $(tput sgr 0)" 
fi

echo " "

echo "=============================================================================="
echo "$(tput setaf 1)EGRESSION Level 1 :: $(tput setaf 2)SSH File Upload$(tput sgr 0)"
echo "=============================================================================="

echo ""
echo "$(tput setaf 3)== WE WILL NOW ATTEMPT TO UPLOAD THE SAME FILE USING SCP OVER VARIOUS PORTS.$(tput sgr 0) =="
echo ""

sleep 1

read -n 1 -s -r -p "Press the ANY key to continue."

echo ""

# SSH Over Port 23


scp -P 23 -i ./key sensitive.docx egression@54.89.49.208:~ 2> /dev/null >&2
if [ $? -eq 0 ]
   then
        echo "SSH FILE UPLOAD SUCCESSFUL :: $(tput setaf 2)23 (TELNET)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" 
        echo "LEVEL 1 FAILURE: It's possible to upload a sensitive file from your network using SSH over at least one port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
   else
        echo "SSH FILE UPLOAD FAILED :: $(tput setaf 2)23 (TELNET)-- $(tput setaf 7)PASSED $(tput sgr 0)" 
fi

# SSH Over Port 80

scp -P 80 -i ./key sensitive.docx egression@54.89.49.208:~ 2> /dev/null >&2
if [ $? -eq 0 ]
    then
        echo "SSH FILE UPLOAD SUCCESSFUL :: $(tput setaf 2)80 (HTTP)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" 
        echo "LEVEL 1 FAILURE: It's possible to upload a sensitive file from your network using SSH over at least one port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
   else
        echo "SSH FILE UPLOAD FAILED :: $(tput setaf 2)80 (HTTP)-- $(tput setaf 7)PASSED $(tput sgr 0)" 
fi

# SSH Over Port 443

scp -P 443 -i ./key sensitive.docx egression@54.89.49.208:~ 2> /dev/null >&2
if [ $? -eq 0 ]
    then
        echo "SSH FILE UPLOAD SUCCESSFUL :: $(tput setaf 2)443 (HTTPS)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" 
        echo "LEVEL 1 FAILURE: It's possible to upload a sensitive file from your network using SSH over at least one port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "SSH FILE UPLOAD FAILED :: $(tput setaf 2)443 (HTTPS)-- $(tput setaf 7)PASSED $(tput sgr 0)" 
fi

# SSH Over Port 3389

scp -P 3389 -i ./key sensitive.docx egression@54.89.49.208:~ 2> /dev/null >&2
if [ $? -eq 0 ]
    then
        echo "SSH FILE UPLOAD SUCCESSFUL :: $(tput setaf 2)3389 (REMOTE DESKTOP)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" 
        echo "LEVEL 1 FAILURE: It's possible to upload a sensitive file from your network using SSH over at least one port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "SSH FILE UPLOAD FAILED :: $(tput setaf 2)3389 (REMOTE DESKTOP)-- $(tput setaf 7)PASSED $(tput sgr 0)" 
fi

# SSH Over Port 5900

scp -P 5900 -i ./key sensitive.docx egression@54.89.49.208:~ 2> /dev/null >&2
if [ $? -eq 0 ]
    then
        echo "SSH FILE UPLOAD SUCCESSFUL :: $(tput setaf 2)5900 (VNC)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" 
        echo "LEVEL 1 FAILURE: It's possible to upload a sensitive file from your network using SSH over at least one port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "SSH FILE UPLOAD FAILED :: $(tput setaf 2)5900 (VNC)-- $(tput setaf 7)PASSED $(tput sgr 0)" 
fi

# SSH Over Port 65211

scp -P 65211 -i ./key sensitive.docx egression@54.89.49.208:~ 2> /dev/null >&2
if [ $? -eq 0 ]
    then
        echo "SSH FILE UPLOAD SUCCESSFUL :: $(tput setaf 2)65211 (ARBITRARY HIGH PORT)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" 
        echo "LEVEL 1 FAILURE: It's possible to upload a sensitive file from your network using SSH over at least one port." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "SSH FILE UPLOAD FAILED :: $(tput setaf 2)5900 (ARBITRARY HIGH PORT)-- $(tput setaf 7)PASSED $(tput sgr 0)" 
fi

echo ""
echo ""

echo "=============================================================================="
echo "$(tput setaf 1)EGRESSION Level 2 :: $(tput setaf 2)DNS File Uploads$(tput sgr 0)"
echo "=============================================================================="

echo ""
echo "$(tput setaf 3)== WE WILL NOW ATTEMPT TO UPLOAD THE SAME FILE USING DNS REQUESTS.$(tput sgr 0) =="
echo ""

sleep 1

echo ""

read -n 1 -s -r -p "Press the ANY key to continue."

echo ""
echo ""

python ./dnsfilexfer/dns_send.py --server 54.89.49.208 --file sensitive.docx --indentifier egression -d egressi0n.com >&2

echo ""

if [ $? -eq 0 ]
    then
        echo "DNS UPLOAD SUCCESSFUL :: $(tput setaf 2)53 (DNS UDP)-- $(tput setaf 1)CHECK FAILED $(tput sgr 0)" 
        echo "LEVEL 2 FAILURE: It's possible to upload a file from your network using DNS requests." >> results.txt
        echo "RECOMMENDATION :: Work on making it far harder to upload sensitive content out of the network." >> results.txt
    else
        echo "FILE UPLOAD FAILED :: $(tput setaf 2)53 (DNS UDP)-- $(tput setaf 7)PASSED $(tput sgr 0)" 
fi

echo ""
echo "$(tput setaf 3)== WE WILL NOW DISPLAY THE RESULTS OF THE TESTING.$(tput sgr 0) =="
echo ""

read -n 1 -s -r -p "Press the ANY key to continue."

echo ""

echo ""
echo ""
echo "$(tput setaf 1)#########################################################################"
echo "################################ RESULTS ################################"
echo "#########################################################################"
echo ""
echo ""

cat results.txt | sort -u

echo ""
echo ""
