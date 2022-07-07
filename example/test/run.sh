#!/usr/bin/bash

set -eu

http-server $1 &
server_id=$!

node /pyodide-node/example/test.mjs

kill $server_id
