#!/bin/bash

set -e

QUERY=$1
PATH=/usr/local/bin:$PATH

prlctl exec $VM_UUID --current-user sapshcut.exe $QUERY