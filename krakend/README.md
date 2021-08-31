To run:
--------
cp /krakend_config/krakend.json /tmp/krakend/.   
docker-compose build
docker-compose up

# (1) krakend.json is the configuration for krakend. It needs to be in a folder
# accessible as a Docker volume (a shared folder on wsl$ for PC, /tmp or similar
# on a Mackintosh). Copy the config there and update docker-compose.yml.
#
# (2) Run 'docker-compose build' to build the test webapp (pingtest).
#
# After that 'docker-compose up' will start the containers.

# endpoint:
#  'localhost:12380/ping' - direct ping
#  'localhost:12381/ping' - ping redirected via krakend
