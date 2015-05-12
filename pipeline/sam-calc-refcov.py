#! /usr/bin/env python
import sys
import argparse
import screed
import math

def ignore_at(iter):
    for item in iter:
        if item.startswith('@'):
            continue
        yield item

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genome')
    parser.add_argument('samfile')

    args = parser.parse_args()

    genome_dict = {}
    for record in screed.open(args.genome):
        genome_dict[record.name] = [0] * len(record.sequence)

    n = 0
    n_skipped = 0
    n_rev = n_fwd = 0

    for samline in ignore_at(open(args.samfile)):
        n += 1
        if n % 100000 == 0:
            print >>sys.stderr, '...', n

        readname, flags, refname, refpos, _, _, _, _, _, seq = \
                  samline.split('\t')[:10]
        if refname == '*' or refpos == '*':
            # (don't count these as skipped)
            continue
        
        refpos = int(refpos)
        try:
            ref = genome_dict[refname]
        except KeyError:
            print >>sys.stderr, "unknown refname: %s; ignoring (read %s)" % (refname, readname)
            n_skipped += 1
            continue

        for i in range(refpos - 1, refpos + len(seq) - 1):
            #print len(ref), i, refpos, len(seq)
            #print samline
            if i < len(ref):
                ref[i] = 1

    if n_skipped / float(n) > .01:
        raise Exception, "Error: too many reads ignored! %d of %d" % \
              (n_skipped, n)

    total = 0.
    cov = 0.

    for name in genome_dict:
        total += len(genome_dict[name])
        cov += sum(genome_dict[name])

    print float(cov) / float(total)

if __name__ == '__main__':
    main()
