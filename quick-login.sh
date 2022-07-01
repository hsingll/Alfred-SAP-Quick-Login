#!/bin/bash

set -e

QUERY=$1
PATH=/usr/local/bin:$PATH

prlctl exec {45b9de62-8177-4e2b-8724-b91f837c38f8} --current-user sapshcut.exe $QUERY