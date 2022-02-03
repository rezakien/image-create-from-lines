NETWORK_NAME=image-create-from-lines
if [ -z $(docker network ls --filter name=^${NETWORK_NAME}$ --format="{{ .Name }}") ] ; then 
     docker network create ${NETWORK_NAME} ; 
fi

docker-compose up --build