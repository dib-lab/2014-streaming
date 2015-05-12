#! /usr/bin/env python
import screed
import argparse
import sys

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
    parser.add_argument('readfile')
    args = parser.parse_args()

    for record in screed.open(args.readfile):
        loc = record.sequence.find('N')
        if loc > -1:
            record.sequence = record.sequence[:loc]
            record.quality = record.quality[:loc]

            if len(record.sequence) < 32:
                continue

        sys.stdout.write(output_single(record))
         

if __name__ == '__main__':
    main()
    
