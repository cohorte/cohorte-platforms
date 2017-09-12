#!/bin/bash
echo "--- Boot of Cohorte Container..."
./opt/init.sh
./usr/lib/systemd/systemd --system
