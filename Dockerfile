# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
# debian docker: https://hub.docker.com/_/debian
FROM debian:latest
MAINTAINER Luca Peretti <lucaperetti.lp@gmail.com>
# RUN git clone dockerize -q https://github.com/SWE-AGGERS/reactions_service.git

RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-setuptools python3-pip git

RUN git clone  --single-branch --branch dockerize -q https://github.com/SWE-AGGERS/reactions_service.git

WORKDIR reactions_service
RUN python3 -m pip install -r requirements.txt
# RUN python3 -m pip freeze
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP service/app.py
EXPOSE 5000
# bind to 0.0.0.0 will make Docker works
CMD ["flask","run","--host", "0.0.0.0"]