 docker rm -f lutece
  docker rm -f lutece2
  docker rm -f storage

  docker rmi -f ow2/lutece:latest
  docker rmi -f ow2/lutece2:latest
  docker rmi -f ow2/mysql:latest
