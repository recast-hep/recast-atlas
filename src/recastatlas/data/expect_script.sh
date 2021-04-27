#!/bin/bash

user=$1
pass=$2

apt-get install -y expect

cat << EOF | expect
set timeout -1

spawn ktutil


expect "ktutil:  "
send -- "add_entry -password -p $user@CERN.CH -k 1 -e aes256-cts-hmac-sha1-96\r"

expect "Password for $user@CERN.CH:"
send -- "$pass\r"

expect "ktutil:  "
send -- "add_entry -password -p $user@CERN.CH -k 1 -e arcfour-hmac\r"

expect "Password for $user@CERN.CH:"
send -- "$pass\r"

expect "ktutil:  "
send -- "write_kt reana_keytab\r"

expect "ktutil:  "
send -- "q\r"
EOF


kdestroy
klist
kinit -kt reana_keytab $user@CERN.CH
klist
