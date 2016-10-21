#! /usr/bin/env python
import sys
import screed
import argparse


def ignore_at(iter):
    for item in iter:
        if item.startswith('@'):
            continue
        yield item


def output_single(read):
    name = read.name
    sequence = read.sequence

    quality = None
    if hasattr(read, 'quality'):
        quality = read.quality

    if quality:
        return "@%s\n%s\n+\n%s\n" % (name, sequence, quality)
    else:
        return ">%s\n%s\n" % (name, sequence)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('samfile')
    parser.add_argument('readsfile')
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
                        default=sys.stdout)

    args = parser.parse_args()

    all_readnames = set()
    for n, samline in enumerate(ignore_at(open(args.samfile))):
        n += 1
        if n % 100000 == 0:
            print >>sys.stderr, '... samfile', n

        readname, _, refname, refpos = samline.split('\t')[:4]
        if refname == '*' or refpos == '*':
            # (don't count these as skipped)
            continue
        all_readnames.add(readname)

    m = 0
    for n, record in enumerate(screed.open(args.readsfile)):
        if n % 100000 == 0:
            print >>sys.stderr, '... readsfile', n
            
        if record.name.split()[0] in all_readnames:
            args.outfile.write(output_single(record))
            m += 1

    print >>sys.stderr, "output %d reads of %d mapped" % (m,
                                                          len(all_readnames))
    print >>sys.stderr, "(missing %d)" % (len(all_readnames) - m,)
    print >>sys.stderr, "dropped %d reads as unmapped" % (n - m,)


if __name__ == '__main__':
    main()
