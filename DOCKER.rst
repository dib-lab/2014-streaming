Make sure you have Docker installed.  When running Ubuntu 14.04, the
following should suffice on a blank system::

    sudo apt-get update
    wget -qO- https://get.docker.com/ | sudo sh

    sudo usermod -aG docker

Now, build a local image from a Dockerfile::

   curl -O https://raw.githubusercontent.com/ged-lab/2014-streaming/master/pipeline/Dockerfile
   docker build -t titus/test .

Set up your working directory::

   git clone https://github.com/ged-lab/2014-streaming.git /mnt/paper
   cd /mnt/paper/pipeline

   ln /mnt/data/* .

Note, this assumes that your data is in /mnt/data; you can either 'ln'
or 'cp' it into the pipeline directory as you wish.

Now, run the software pipeline::

   docker run -v /mnt/paper:/paper -it titus/test /paper/pipeline/run-in-docker.sh
