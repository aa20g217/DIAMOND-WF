FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main

#Install DIAMOND
RUN apt-get update && apt-get install -y git wget
RUN apt-get install -y tar
RUN wget http://github.com/bbuchfink/diamond/releases/download/v2.0.14/diamond-linux64.tar.gz
RUN tar xzf diamond-linux64.tar.gz

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
