#!/bin/bash

cd ~/dev/plato

echo "================================="
echo $(date)
echo "New week has started... Running the randomization algorithm to find this week's schedule!"
python3 -m scripts.week
echo "================================="
