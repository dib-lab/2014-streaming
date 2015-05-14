#! /bin/bash
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2014-paper-streaming/SRR606249_1.fastq.gz
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2014-paper-streaming/SRR606249_2.fastq.gz
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2014-paper-streaming/mouse-l.fastq.gz
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2014-paper-streaming/mouse-r.fastq.gz
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2014-paper-streaming/mouse-ref.fa.gz
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2014-paper-streaming/podar-1.fastq.gz
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2014-paper-streaming/podar-2.fastq.gz
curl -O http://public.ged.msu.edu.s3.amazonaws.com/2014-paper-streaming/podar-ref.fa.gz
gunzip -f *.fa.gz
