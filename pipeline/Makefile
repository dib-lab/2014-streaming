#TODO - put in spot checks for the trickier scripts!

#SHELL=/bin/bash
NULLGRAPH=~/dev/nullgraph
KHMER=~/dev/khmer
QUAKE=../Quake
JELLYFISH=/usr/local/bin/jellyfish

all: compare mcompare compare3 mcompare3 rcompare rcompare3 bam \
	compare4 mcompare4 rcompare4 compare5 compare6 \
	simple-genome-reads-even.sam.errhist \
	simple-genome-reads-even.fa.errhist \
	simple-genome-kmers.hist \
	simple-genome-dn-kmers.hist \
	ecoli \
	ecoli-errfree-report.txt ecoli_corr \
	rseq podar readstats.txt kmer-counts.txt

readstats.txt: podar-mapped.fq.gz.keep rseq-mapped.fq.gz.keep ecoli-mapped.fq.gz.keep
	readstats.py simple-*.fa{,.keep} *-mapped.fq.gz{,.keep} -o readstats.txt

kmer-counts.txt:
	echo ecoli > kmer-counts.txt
	$(KHMER)/sandbox/unique-kmers.py -k 20 ecoli-mapped.fq.gz >> kmer-counts.txt
	echo ecoli-dn >> kmer-counts.txt
	$(KHMER)/sandbox/unique-kmers.py -k 20 ecoli-mapped.fq.gz.keep >> kmer-counts.txt
	echo rseq >> kmer-counts.txt
	$(KHMER)/sandbox/unique-kmers.py -k 20 rseq-mapped.fq.gz >> kmer-counts.txt
	echo rseq-dn >> kmer-counts.txt
	$(KHMER)/sandbox/unique-kmers.py -k 20 rseq-mapped.fq.gz.keep >> kmer-counts.txt
	echo podar >> kmer-counts.txt
	$(KHMER)/sandbox/unique-kmers.py -k 20 podar-mapped.fq.gz >> kmer-counts.txt
	echo podar-dn >> kmer-counts.txt
	$(KHMER)/sandbox/unique-kmers.py -k 20 podar-mapped.fq.gz.keep >> kmer-counts.txt

# delete the targets of rules on an error
.DELETE_ON_ERROR:

bam: simple-genome-reads.sorted.bam simple-metagenome-reads.sorted.bam \
	simple-mrna-reads.sorted.bam

#---------------Podar and mouse --------

podar-paired: podar \
	trim-at-N \
	podar-reads.sam \
	podar-mapped.fq.gz \
	podar-reads.sam.pos \
	podar-dn-report.txt \
	podar-mapped.fq.gz.abundtrim \
	podar_compare5_pre.txt \
	podar-abundtrim.sam \
	podar-abundtrim.sam.pos \
	podar_compare5_post.txt


mouse-paired: mouse \
	mouse-reads.sam \
	mouse-mapped.fq.gz \
	mouse-reads.sam.pos \
	mouse-dn-report.txt \
	mouse-mapped.fq.gz.abundtrim \
	mouse_compare5_pre.txt \
	mouse-abundtrim.sam \
	mouse-abundtrim.sam.pos \
	mouse_compare5_post.txt





#------------------
clean:
	-rm -f simple-genome.fa simple-genome-reads.dn.kh simple-genome-reads.sam
	-rm -f *-reads.fa
	-rm -f rseq_compare*.txt
	-rm -f *.abundtrim *.ebwt *.fai *.pos *.keep *.bam *.mut *.bai *.sam *.kh
	-rm -f *.errhist *.abundfilt *.hicov.fq *.lowcov.fq *.report
	-rm -f *.txt repgenome* repeat* *.out *.cov
	-rm -f *.bt2 *.hist *.info *.dict *.covhist *.covdict

##### simple genome
include makefile.simple-genome

##### simple metagenome
include makefile.simple-metagenome

##### simple mrna molecule with three isoforms (1234, 124, 134)
include makefile.simple-mrna

##### mouse 1m rnaseq data set (real)
include makefile.rseq

##### E. coli genome data set (real)
include makefile.ecoli

##### shotgun metagenome data set (real)
include makefile.podar

# final set of big analyses
include makefile.big

#####

repeat-10.fa:
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 1 > repeat-1.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 2 > repeat-2.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 3 > repeat-3.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 4 > repeat-4.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 5 > repeat-5.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 6 > repeat-6.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 7 > repeat-7.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 8 > repeat-8.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 9 > repeat-9.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 10 > repeat-10.fa

repgenome-10.fa: repeat-10.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-1.fa > repgenome-1.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-2.fa > repgenome-2.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-3.fa > repgenome-3.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-4.fa > repgenome-4.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-5.fa > repgenome-5.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-6.fa > repgenome-6.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-7.fa > repgenome-7.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-8.fa > repgenome-8.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-9.fa > repgenome-9.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-10.fa > repgenome-10.fa

repgenome-10-reads.fa: repgenome-10.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-1.fa --mutation-details repgenome-1-reads.mut > repgenome-1-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-2.fa --mutation-details repgenome-2-reads.mut > repgenome-2-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-3.fa --mutation-details repgenome-3-reads.mut > repgenome-3-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-4.fa --mutation-details repgenome-4-reads.mut > repgenome-4-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-5.fa --mutation-details repgenome-5-reads.mut > repgenome-5-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-6.fa --mutation-details repgenome-6-reads.mut > repgenome-6-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-7.fa --mutation-details repgenome-7-reads.mut > repgenome-7-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-8.fa --mutation-details repgenome-8-reads.mut > repgenome-8-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-9.fa --mutation-details repgenome-9-reads.mut > repgenome-9-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-10.fa --mutation-details repgenome-10-reads.mut > repgenome-10-reads.fa

repgenome-10-reads.mut.pos: repgenome-10-reads.mut repgenome-10.fa
	./convert-mut-to-pos.py repgenome-1-reads.mut repgenome-1-reads.mut.pos
	./convert-mut-to-pos.py repgenome-2-reads.mut repgenome-2-reads.mut.pos
	./convert-mut-to-pos.py repgenome-3-reads.mut repgenome-3-reads.mut.pos
	./convert-mut-to-pos.py repgenome-4-reads.mut repgenome-4-reads.mut.pos
	./convert-mut-to-pos.py repgenome-5-reads.mut repgenome-5-reads.mut.pos
	./convert-mut-to-pos.py repgenome-6-reads.mut repgenome-6-reads.mut.pos
	./convert-mut-to-pos.py repgenome-7-reads.mut repgenome-7-reads.mut.pos
	./convert-mut-to-pos.py repgenome-8-reads.mut repgenome-8-reads.mut.pos
	./convert-mut-to-pos.py repgenome-9-reads.mut repgenome-9-reads.mut.pos
	./convert-mut-to-pos.py repgenome-10-reads.mut repgenome-10-reads.mut.pos

repgenome-10-reads.dn.kh: repgenome-10-reads.fa
	normalize-by-median.py -k 20 -C 20 repgenome-1-reads.fa -s repgenome-1-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-2-reads.fa -s repgenome-2-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-3-reads.fa -s repgenome-3-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-4-reads.fa -s repgenome-4-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-5-reads.fa -s repgenome-5-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-6-reads.fa -s repgenome-6-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-7-reads.fa -s repgenome-7-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-8-reads.fa -s repgenome-8-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-9-reads.fa -s repgenome-9-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-10-reads.fa -s repgenome-10-reads.dn.kh -x 2e6 -N 4

repgenome-10-reads.calc.pos: repgenome-10-reads.dn.kh
	./report-errors-by-read.py repgenome-1-reads.dn.kh repgenome-1-reads.fa > repgenome-1-reads.calc.pos
	./report-errors-by-read.py repgenome-2-reads.dn.kh repgenome-2-reads.fa > repgenome-2-reads.calc.pos
	./report-errors-by-read.py repgenome-3-reads.dn.kh repgenome-3-reads.fa > repgenome-3-reads.calc.pos
	./report-errors-by-read.py repgenome-4-reads.dn.kh repgenome-4-reads.fa > repgenome-4-reads.calc.pos
	./report-errors-by-read.py repgenome-5-reads.dn.kh repgenome-5-reads.fa > repgenome-5-reads.calc.pos
	./report-errors-by-read.py repgenome-6-reads.dn.kh repgenome-6-reads.fa > repgenome-6-reads.calc.pos
	./report-errors-by-read.py repgenome-7-reads.dn.kh repgenome-7-reads.fa > repgenome-7-reads.calc.pos
	./report-errors-by-read.py repgenome-8-reads.dn.kh repgenome-8-reads.fa > repgenome-8-reads.calc.pos
	./report-errors-by-read.py repgenome-9-reads.dn.kh repgenome-9-reads.fa > repgenome-9-reads.calc.pos
	./report-errors-by-read.py repgenome-10-reads.dn.kh repgenome-10-reads.fa > repgenome-10-reads.calc.pos

repgenome-compare.txt: repgenome-10-reads.calc.pos repgenome-10-reads.mut.pos
	./compare-pos-2.py 1 repgenome-1-reads.mut.pos repgenome-1-reads.calc.pos repgenome-1-reads.fa > repgenome-compare.txt
	./compare-pos-2.py 2 repgenome-2-reads.mut.pos repgenome-2-reads.calc.pos repgenome-2-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 3 repgenome-3-reads.mut.pos repgenome-3-reads.calc.pos repgenome-3-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 4 repgenome-4-reads.mut.pos repgenome-4-reads.calc.pos repgenome-4-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 5 repgenome-5-reads.mut.pos repgenome-5-reads.calc.pos repgenome-5-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 6 repgenome-6-reads.mut.pos repgenome-6-reads.calc.pos repgenome-6-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 7 repgenome-7-reads.mut.pos repgenome-7-reads.calc.pos repgenome-7-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 8 repgenome-8-reads.mut.pos repgenome-8-reads.calc.pos repgenome-8-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 9 repgenome-9-reads.mut.pos repgenome-9-reads.calc.pos repgenome-9-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 10 repgenome-10-reads.mut.pos repgenome-10-reads.calc.pos repgenome-10-reads.fa >> repgenome-compare.txt

####

#--------------------------------------Podar Work--------------------
podar: podar-1.fastq.gz podar-2.fastq.gz podar-ref.fa
	bowtie2-build podar-ref.fa podar \
	samtools faidx podar-ref.fa 

trim-at-N: podar 
	./trim-at-N.py podar-1.fastq.gz >p1.fastq \
	./trim-at-N.py podar-2.fastq.gz >p2.fastq  \
	gzip -c p1.fastq >p1.fastq.gz \
	gzip -c p2.fastq >p2.fastq.gz

podar-reads.sam: p1.fastq.gz p2.fastq.gz 
	bowtie2 -p 4 -x podar -1 p1.fastq.gz -2 p2.fastq.gz -S podar-reads.sam \

podar-mapped.fq.gz: podar-reads.sam
	./extract-sam-seqs-to-fq.py podar-reads.sam p1.fastq.gz > sam-seq-1 \  
	./extract-sam-seqs-to-fq.py podar-reads.sam p2.fastq.gz > sam-seq-2 \
	 cat sam-seq-1 sam-seq-2 >sam-seq \
	gzip -c sam-seq >podar-mapped.fq.gz

podar-reads.sam.pos: podar-reads.sam podar-ref.fa
	./sam-scan.py podar-ref.fa podar-reads.sam > podar-reads.sam.pos

podar-dn-report.txt: podar-mapped.fq.gz 
	normalize-by-median.py -x 4e8 -N 4 -k 20 -C 20 -s podar.dn.kh podar-mapped.fq.gz -R podar-dn-report.txt

podar-mapped.fq.gz.abundtrim: podar-mapped.fq.gz 
	/mnt/khmer/sandbox/trim-low-abund.py -V -k 20 -Z 20 -C 3 -x 4e8 -N 4 podar-mapped.fq.gz

podar_compare5_pre.txt: podar-mapped.fq.gz
	./summarize-pos-file.py podar-reads.sam.pos podar-mapped.fq.gz > podar_compare5_pre.txt

podar-abundtrim.sam: podar-mapped.fq.gz.abundtrim
	bowtie2 -p 4 -x podar -U podar-mapped.fq.gz.abundtrim -S podar-abundtrim.sam

podar-abundtrim.sam.pos: podar-abundtrim.sam
	./sam-scan.py podar-ref.fa podar-abundtrim.sam > podar-abundtrim.sam.pos 
        
podar_compare5_post.txt: podar-abundtrim.sam.pos podar-mapped.fq.gz.abundtrim
	./summarize-pos-file.py podar-abundtrim.sam.pos podar-mapped.fq.gz.abundtrim > podar_compare5_post.txt 

#---------------------------------------Mouse  Work--------------
mouse: mouse.fastq.gz mouse-ref.fa
	bowtie2-build mouse-ref.fa mouse \
	samtools faidx mouse-ref.fa 

mouse-reads.sam: m.fastq.gz
	./trim-at-N.py mouse.fastq.gz | bowtie2 -p 4 -x mouse -U - -S mouse-reads.sam

mouse-mapped.fq.gz: mouse-reads.sam
	./extract-sam-seqs-to-fq.py mouse-reads.sam m.fastq.gz > sam-seq \  
	gzip -c sam-seq >mouse-mapped.fq.gz

mouse-reads.sam.pos: mouse-reads.sam mouse-ref.fa
	./sam-scan.py mouse-ref.fa mouse-reads.sam > mouse-reads.sam.pos

mouse-dn-report.txt: mouse-mapped.fq.gz
	normalize-by-median.py -x 4e8 -N 4 -k 20 -C 20 -s mouse.dn.kh mouse-mapped.fq.gz -R mouse-dn-report.txt

mouse-mapped.fq.gz.abundtrim: mouse-mapped.fq.gz
	/mnt/khmer/sandbox/trim-low-abund.py -V -k 20 -Z 20 -C 3 -x 4e8 -N 4 mouse-mapped.fq.gz

mouse_compare5_pre.txt: mouse-mapped.fq.gz
	./summarize-pos-file.py mouse-reads.sam.pos mouse-mapped.fq.gz > mouse_compare5_pre.txt

mouse-abundtrim.sam: mouse-mapped.fq.gz.abundtrim
	bowtie2 -p 4 -x mouse -U mouse-mapped.fq.gz.abundtrim -S mouse-abundtrim.sam

mouse-abundtrim.sam.pos: mouse-abundtrim.sam
	./sam-scan.py mouse-ref.fa mouse-abundtrim.sam > mouse-abundtrim.sam.pos 
        
mouse_compare5_post.txt: mouse-abundtrim.sam.pos mouse-mapped.fq.gz.abundtrim
	./summarize-pos-file.py mouse-abundtrim.sam.pos mouse-mapped.fq.gz.abundtrim > mouse_compare5_post.txt 

#--------------------------------------------------


