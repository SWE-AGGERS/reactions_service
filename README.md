# reactions_service
## Start Docker 
* docker build .
* docker tag <IMAGE ID> reactions_service
* docker run -p 5000:5000 --name react reactions_service


#### DockerFile:
* Uses a bind volume in order to work without the need of rebuild the image.<br/>
* The app run on 0.0.0.0 otherwise it can't be seen through Docker

#### docker-compose:
* care the ports number for each service
