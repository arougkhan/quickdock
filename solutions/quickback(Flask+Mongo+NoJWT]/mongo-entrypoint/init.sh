#!/usr/bin/env bash
echo "Creating mongo users..."
mongo --authenticationDatabase admin --host localhost -u hexterisk -p strongPassword tac --eval "db.createUser({user: 'normal', pwd: 'normal', roles: [{role: 'readWrite', db: 'tac'}]});"
mongo --authenticationDatabase admin --host localhost -u hexterisk -p strongPassword admin --eval "db.createUser({user: 'admin', pwd: 'pass', roles: [{role: 'userAdminAnyDatabase', db: 'admin'}]});"
echo "Mongo users created."