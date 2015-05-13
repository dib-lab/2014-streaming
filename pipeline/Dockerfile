FROM ubuntu:14.04
MAINTAINER Titus Brown <titus@idyll.org>
RUN apt-get update
RUN apt-get install -y python-virtualenv python-dev git bowtie2 samtools libboost-dev zlib1g-dev
RUN pip install -U setuptools
RUN git clone https://github.com/ged-lab/nullgraph.git /home/nullgraph
RUN git clone https://github.com/ged-lab/khmer.git /home/khmer
RUN cd /home/khmer && make install
CMD /paper/pipeline/docker-entrypoint.sh

