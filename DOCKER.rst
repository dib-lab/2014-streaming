Running the paper pipeline in Docker
====================================

Installing Docker on Ubuntu 14.04 / Amazon AWS
----------------------------------------------

Make sure you have Docker installed.  When running Ubuntu 14.04, the
following should suffice on a blank system.

First, update your Debian packages -- ::

    sudo apt-get update

Then, install docker::

    wget -qO- https://get.docker.com/ | sudo sh

And, finally, update the default user 'ubuntu' to be able to run docker::

    sudo usermod -aG docker ubuntu

If '/mnt' is your working directory, as assumed below, you should also make
it world-writeable::

    sudo chmod a+rwxt /mnt

Running the data analysis pipeline with our Docker container
------------------------------------------------------------

We've provided a public Docker container (built from the `Dockerfile
<https://github.com/ged-lab/2014-streaming/blob/master/pipeline/Dockerfile>`__)
for you to use.

Set up your working directory::

   git clone https://github.com/ged-lab/2014-streaming.git /mnt/paper
   cd /mnt/paper/pipeline

Grab the data::

   ./download-data.sh

And now run the software pipeline::

   docker run -v /mnt/paper:/paper -it titus/2014-streaming

Building a local Docker image & running the data analysis pipeline
------------------------------------------------------------------

You can also build your own local image from the Dockerfile::

   curl -O https://raw.githubusercontent.com/ged-lab/2014-streaming/master/pipeline/Dockerfile
   docker build -t titus/test .

Then, to run it, set up your working directory::

   git clone https://github.com/ged-lab/2014-streaming.git /mnt/paper
   cd /mnt/paper/pipeline

Grab the data::

   ./download-data.sh

And now run the software pipeline::

   docker run -v /mnt/paper:/paper -it titus/test
