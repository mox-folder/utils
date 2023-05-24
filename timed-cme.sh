#!/bin/bash

while IFS= read -r ip_address
do
    echo "Running cme for $ip_address..."

    # Run your command with the current IP address, suppressing error messages
    (crackmapexec smb $ip_address -u '' -p '' --shares 2>/dev/null < /dev/null) | tee -a cme-smb-sweep.txt

    # Wait for 5 seconds before the next iteration
    sleep 5 # replace with desired delay
done < ip_list.txt # replace with your file name

echo "Script completed."
