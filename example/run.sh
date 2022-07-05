#!/usr/bin/bash

set -eux

http-server @1 &
server_id=$!

echo $(npm root -g)
node -e "console.log(global.module.paths)"
ls /node_modules

node /example/test.mjs

kill $server_id
