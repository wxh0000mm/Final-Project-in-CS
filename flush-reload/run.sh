#!/bin/sh

set -o errexit
set -o xtrace
set -o nounset

GPG=/home/alon/Projects/attempt-ff/gnupg-1.4.13/bin/gpg
ADDR=docs/addr/breakpoints1.txt 
MESSAGE=message.txt
OUT=out.txt
CYCLES=$1

bin/probe "${GPG}" ${ADDR} ${OUT} "${CYCLES}" &
PROBE_PID=$!

sleep 0.01
(echo "GPG start"; ${GPG} --yes --sign ${MESSAGE}; echo "GPG end") &
GPG_PID=$!

trap "echo 'Received signal'; kill -TERM ${PROBE_PID} ${GPG_PID}" \
    INT QUIT

wait ${PROBE_PID}
wait ${GPG_PID}

python src/graph.py &
GRAPH_PID=$!

python src/analyze.py ${OUT}



trap "echo 'Killing python'; kill -TERM ${GRAPH_PID}" INT QUIT
wait ${GRAPH_PID}
