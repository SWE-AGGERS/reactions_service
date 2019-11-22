# reactions_service

## Build and run docker container

* Uses a bind volume in order to work without the need of rebuild the image.<br/>
* The app run on 0.0.0.0 otherwise it can't be seen through Docker

* In order to use redis with docker, change resis URL in _background.py_:<br/>
`BACKEND = BROKER = 'redis://redis:6379' `<br/>
instead of <br/>
`BACKEND = BROKER = 'redis://127.0.0.1:6379'`<br/>
<br/>**Build and run:**
* docker build .
* docker tag [IMAGE ID] reactions_service
* docker run -p 5000:5000 --name react reactions_service

#### docker-compose:
Care the ports number for each service
* docker-compose build
* docker-compose up