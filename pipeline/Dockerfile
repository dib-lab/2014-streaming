FROM ubuntu:14.04
MAINTAINER Titus Brown <titus@idyll.org>
RUN apt-get update && apt-get install -y python-virtualenv python-dev git bowtie2 samtools libboost-dev zlib1g-dev
git clone https://github.com/ged-lab/nullgraph.git
git clone https://github.com/ged-lab/khmer.git
cd khmer && make install
EOF
