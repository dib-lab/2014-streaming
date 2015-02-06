#TODO - put in spot checks for the trickier scripts!

NULLGRAPH=~/dev/nullgraph
KHMER=/mnt/khmer

all: compare mcompare compare3 mcompare3 rcompare rcompare3 bam \
	compare4 mcompare4 rcompare4 compare5 compare6 \
	simple-genome-reads-even.sam.errhist \
	simple-genome-reads-even.fa.errhist \
	ecoli1 \
	ecoli-report-untrim.txt \
	ecoli-report-trim.txt \
	ecoli-errfree-report.txt \
	simple-genome-kmers.hist \
	simple-genome-dn-kmers.hist \

bam: simple-genome-reads.sorted.bam simple-metagenome-reads.sorted.bam \
	mrna-reads.sorted.bam

podar-paired: podar \
	trim-at-N \
	podar-mapped \
	podar-reads.sam.pos \
	podar-mapped.fq.gz.abundtrim \
	podar-compare5-pre.txt \
	podar-abundtrim.sam \
	podar-abundtrim.sam.pos \
	podar-compare5-post.txt

mouse-paired: mouse \
	trim-at-N \
	mouse-mapped  \
	mouse-reads.sam.pos \
	mouse-mapped.fq.gz.abundtrim \
	mouse-compare5-pre.txt \
	mouse-abundtrim.sam \
	mouse-abundtrim.sam.pos \
	mouse-compare5-post.txt

clean:
	-rm -f simple-genome.fa simple-genome-reads.dn.kh simple-genome-reads.sam
	-rm -f *-reads.fa
	-rm -f *.abundtrim *.ebwt *.fai *.pos *.keep *.bam *.mut *.bai *.sam *.kh

##### simple genome
include makefile.simple-genome

##### simple metagenome
include makefile.simple-metagenome

##### simple mrna molecule with three isoforms (1234, 124, 134)
include makefile.mrna

#--------------------------------------Podar Work--------------------
podar: podar-1.fastq.gz  podar-ref.fa
	bowtie2-build podar-ref.fa podar \
	samtools faidx podar-ref.fa 

trim-at-N: podar 
	./trim-at-N.py podar-1.fastq.gz | bowtie2 -p 4 -x podar -U - -S podar-reads.sam 

podar-mapped: podar-1.fastq.gz podar-reads-sam 
	./extract-sam-seqs-to-fq.py podar-reads.sam podar-1.fastq.gz > sam-seq \
	gzip -c sam-seq  > podar-mapped.fq.gz

podar-reads.sam.pos: podar-reads.sam podar-ref.fa
	./sam-scan.py podar-ref.fa podar-reads.sam > podar-reads.sam.pos

podar-mapped.fq.gz.abundtrim: podar-mapped.fq.gz 
	/mnt/khmer/sandbox/trim-low-abund.py -V -k 20 -Z 20 -C 3 -x 4e9 -N 4 podar-mapped.fq.gz	

podar-compare5-pre.txt: podar-mapped.fq.gz
	./summarize-pos-file.py podar-reads.sam.pos podar-mapped.fq.gz > podar-compare5-pre.txt

podar-abundtrim.sam: podar-mapped.fq.gz.abundtrim
	bowtie2 -p 4 -x podar -U podar-mapped.fq.gz.abundtrim -S podar-abundtrim.sam

podar-abundtrim.sam.pos: podar-abundtrim.sam
	./sam-scan.py podar-ref.fa podar-abundtrim.sam > podar-abundtrim.sam.pos 
	
podar-compare5-post.txt: podar-abundtrim.sam.pos podar-mapped.fq.gz.abundtrim
	./summarize-pos-file.py podar-abundtrim.sam.pos podar-mapped.fq.gz.abundtrim > podar-compare5-post.txt 

#---------------------------------------Mouse  Work--------------
mouse: mouse.fastq.gz mouse-ref.fa
	bowtie2-build mouse-ref.fa mouse \
	samtools faidx mouse-ref.fa 

trim-at-N: mouse
        ./trim-at-N.py mouse-l.fastq.gz | bowtie2 -p 4 -x mouse -U - -S mouse-reads.sam 

mouse-mapped: mouse-l.fastq.gz mouse-reads-sam
        ./extract-sam-seqs-to-fq.py mouse-reads.sam mouse-l.fastq.gz > sam-seq \
        gzip -c sam-seq  > mouse-mapped.fq.gz

mouse-reads.sam.pos: mouse-reads.sam mouse-ref.fa
        ./sam-scan.py mouse-ref.fa mouse-reads.sam > mouse-reads.sam.pos

mouse-mapped.fq.gz.abundtrim: mouse-mapped.fq.gz
        /mnt/khmer/sandbox/trim-low-abund.py -V -k 20 -Z 20 -C 3 -x 4e8 -N 4 mouse-mapped.fq.gz 

mouse-compare5-pre.txt: mouse-mapped.fq.gz
        ./summarize-pos-file.py mouse-reads.sam.pos mouse-mapped.fq.gz > mouse-compare5-pre.txt

mouse-abundtrim.sam: mouse-mapped.fq.gz.abundtrim
        bowtie2 -p 4 -x mouse -U mouse-mapped.fq.gz.abundtrim -S mouse-abundtrim.sam

mouse-abundtrim.sam.pos: mouse-abundtrim.sam
        ./sam-scan.py mouse-ref.fa mouse-abundtrim.sam > mouse-abundtrim.sam.pos 
        
mouse-compare5-post.txt: mouse-abundtrim.sam.pos mouse-mapped.fq.gz.abundtrim
        ./summarize-pos-file.py mouse-abundtrim.sam.pos mouse-mapped.fq.gz.abundtrim > mouse-compare5-post.txt

#--------------------------------------------------
ecoli1: ecoli-report.txt ecoli-report-nodn.txt

# bowtie index for ecoliMG1655.fa
ecoli.1.ebwt: ecoliMG1655.fa
	bowtie-build ecoliMG1655.fa ecoli
	samtools faidx ecoliMG1655.fa

# ecoli-reads.sam is the bowtie mapping of the reads to the reference genome.
ecoli-reads.sam: ecoli_ref-5m.fastq.gz ecoli.1.ebwt
	gunzip -c ecoli_ref-5m.fastq.gz | bowtie ecoli -q - -S ecoli-reads.sam

# ecoli-reads.sam.pos is the 'pos' file containing the locations of mismatches,
# i.e. errors, determined from mapping.
ecoli-reads.sam.pos: ecoli-reads.sam
	./sam-scan.py ecoliMG1655.fa ecoli-reads.sam ecoli_ref-5m.fastq.gz > ecoli-reads.sam.pos

# ecoli_ref.kh contains the counting table of k-mers in the raw read data set.
ecoli_ref.kh: ecoli_ref-5m.fastq.gz
	load-into-counting.py ecoli_ref.kh -k 20 -x 2e8 -N 4 ecoli_ref-5m.fastq.gz

ecoli-reads-nodn.errors.pos: ecoli_ref.kh
	./report-errors-by-read.py -C 15 ecoli_ref.kh ecoli_ref-5m.fastq.gz > ecoli-reads-nodn.errors.pos

ecoli-report-nodn.txt: ecoli-reads-nodn.errors.pos
	./compare-pos.py ecoli-reads-nodn.errors.pos ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz > ecoli-report-nodn.txt

# ecoli_ref.dn.kh contains the counting table output by digital normalization
# of the raw E. coli reads.
ecoli_ref.dn.kh: ecoli_ref-5m.fastq.gz
	~/dev/khmer/scripts/normalize-by-median.py -x 1e8 -N 4 -k 20 -C 20 -s ecoli_ref.dn.kh ecoli_ref-5m.fastq.gz -R ecoli-dn-report.txt

# ecoli-reads.errors.pos contains the location of errors according to our
# own algorithm.
ecoli-reads.errors.pos: ecoli_ref-5m.fastq.gz ecoli_ref.dn.kh
	./report-errors-by-read.py ecoli_ref.dn.kh ecoli_ref-5m.fastq.gz > ecoli-reads.errors.pos

# ecoli-report.txt: a comparison of the errors found by mapping and 
# those found by our k-mer spectral error detection implementation.
ecoli-report.txt: ecoli-reads.errors.pos ecoli-reads.sam.pos
	./compare-pos.py ecoli-reads.errors.pos ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz > ecoli-report.txt

# ecoli_ref-5m.fastq.gz.abundtrim contains the k-mer abundance trimmed
# reads, produced by trim-low-abund (streaming k-mer abundance trimming)
ecoli_ref-5m.fastq.gz.abundtrim: ecoli_ref-5m.fastq.gz
	$(KHMER)/sandbox/trim-low-abund.py -k 20 -Z 20 -C 5 -x 1e8 -N 4 ecoli_ref-5m.fastq.gz

# ecoli-abundtrim.sam is the mapping of the abundance-trimmed reads to the
# reference genome.
ecoli-abundtrim.sam: ecoli_ref-5m.fastq.gz.abundtrim
	bowtie ecoli -q ecoli_ref-5m.fastq.gz.abundtrim -S ecoli-abundtrim.sam

# ecoli-abundtrim.sam.pos is the 'pos' file containing the locations of
# mismatches to the reference genome in the reads, based on mapping.
ecoli-abundtrim.sam.pos: ecoli-abundtrim.sam
	./sam-scan.py ecoliMG1655.fa ecoli-abundtrim.sam ecoli_ref-5m.fastq.gz.abundtrim > ecoli-abundtrim.sam.pos

# ecoli-report-untrim.txt - a report on the error rate of the untrimmed reads,
# based on mapping to the reference.
ecoli-report-untrim.txt: ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz
	./summarize-pos-file.py ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz > ecoli-report-untrim.txt

# ecoli-report-untrim.txt - a report on the error rate of the k-mer
# abundance trimmed reads, based on mapping to the reference.
ecoli-report-trim.txt: ecoli-abundtrim.sam.pos ecoli_ref-5m.fastq.gz.abundtrim
	./summarize-pos-file.py ecoli-abundtrim.sam.pos ecoli_ref-5m.fastq.gz.abundtrim > ecoli-report-trim.txt

ecoli-errfree-reads.fa: ecoliMG1655.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e 0 -r 100 -C 100 ecoliMG1655.fa > ecoli-errfree-reads.fa

ecoli-errfree-report.txt: ecoli-errfree-reads.fa
	~/dev/khmer/scripts/normalize-by-median.py -x 1e8 -N 4 -k 20 -C 20 ecoli-errfree-reads.fa -R ecoli-errfree-report.txt
