FROM ubuntu:14.04
MAINTAINER Titus Brown <titus@idyll.org>
WORKDIR /home

# update ubuntu
RUN apt-get update
RUN apt-get install -y python-virtualenv python-dev git bowtie2 samtools libboost-dev zlib1g-dev

# update setuptools
RUN pip install -U setuptools

# install Jellyfish
RUN apt-get -y install curl
RUN curl http://www.cbcb.umd.edu/software/jellyfish/jellyfish-1.1.11.tar.gz > je
llyfish.tar.gz && \
        tar xzf jellyfish.tar.gz && \
        cd jellyfish-1.1.11 && \
        ./configure && \
        make

# install Quake
RUN curl http://www.cbcb.umd.edu/software/quake/downloads/quake-0.3.5.tar.gz > q
uake.tar.gz && \
        tar xzf quake.tar.gz && \
        cd Quake/src && \
        make

# install khmer and nullgraph
RUN git clone https://github.com/ged-lab/nullgraph.git /home/nullgraph
RUN git clone https://github.com/ged-lab/khmer.git /home/khmer
RUN cd /home/khmer && make install

# the basic command runs 'make' with appropriate paths set to installed sw.
CMD /paper/pipeline/docker-entrypoint.sh
