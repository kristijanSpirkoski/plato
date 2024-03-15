#!/bin/bash

echo "Adding $1 to Pi-Hole whitelist. You can now use it!"
pihole --white-regex *$1*
pihole restartdns