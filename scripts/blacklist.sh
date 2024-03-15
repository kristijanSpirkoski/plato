#!/bin/bash
echo "Adding $1 to Pi-Hole blacklist. You can no longer use it!"
pihole --regex *$1*
pihole restartdns