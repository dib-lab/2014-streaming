# ~400 GB disk space, 15 GB RAM

sudo apt-get update && sudo shutdown -r now

sudo apt-get -y install python-virtualenv python-dev git bowtie2 samtools libboost-dev zlib1g-dev

sudo chmod a+rwxt /mnt

python -m virtualenv work
. work/bin/activate

pip install -U setuptools
git clone https://github.com/ged-lab/nullgraph.git
git clone https://github.com/ged-lab/khmer.git
# use master for now, not -b v1.3

cd khmer
make install
cd


cd /mnt

git clone https://github.com/ged-lab/2014-streaming.git
cd 2014-streaming

curl -O http://www.cbcb.umd.edu/software/jellyfish/jellyfish-1.1.11.tar.gz
curl -O http://www.cbcb.umd.edu/software/quake/downloads/quake-0.3.5.tar.gz

tar xzf jellyfish-1.1.11.tar.gz
cd jellyfish-1.1.11/
./configure && make 
cd ../

tar xzf quake-0.3.5.tar.gz 
cd Quake/src
make
cd ../../

cd /mnt/2014-streaming/pipeline

###

###

#curl -O https://s3.amazonaws.com/public.ged.msu.edu/ecoli_ref-5m.fastq.gz

#curl -L -O https://github.com/ctb/edda/raw/master/doc/tutorials-2012/files/ecoliMG1655.fa.gz
#gunzip ecoliMG1655.fa

###

ln -fs /mnt/data/mouse-l.fastq.gz mouse-rnaseq.fq.gz
ln -fs /mnt/data/mouse-ref.fa rna.fa

ln -fs /mnt/data/SRR606249_1.fastq.gz ./podar-1.fastq.gz
ln -fs /mnt/data/podar-ref.fa .

###

make NULLGRAPH=~/nullgraph KHMER=~/khmer

