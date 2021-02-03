#!/usr/bin/env bash

PIP_LINUX="requirements.txt"
PIP_MAC="requirements-mac.txt"

if [ "$1" = "mac" ]; then
  REQUIREMENTS="$PIP_MAC"
else
  REQUIREMENTS="$PIP_LINUX"
fi

echo "\n\nInstalling $1 requirements from $REQUIREMENTS\n\n"

while read p; do
  pip3 install $p
done < $REQUIREMENTS