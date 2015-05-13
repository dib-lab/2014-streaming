#! /bin/bash
cd /paper/pipeline
make NULLGRAPH=/home/nullgraph \
    KHMER=/home/khmer \
    JELLYFISH=/home/jellyfish-1.1.11/bin/jellyfish \
    QUAKE=/home/Quake/bin/Quake
