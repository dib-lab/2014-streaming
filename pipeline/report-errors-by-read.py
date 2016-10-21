#! /usr/bin/env python
import sys
import screed
import khmer
import argparse

# NOT USED
def find_spectral_error_positions(kh, sequence, cutoff):
    K = kh.ksize()

    start = 0
    end = len(sequence) - K + 1
    posns = []

    # skip over errors at beginning
    while start < end:
        if kh.get(sequence[start:start+K]) >= cutoff:
            break
        start += 1

    if start > 0:
        if start >= K:
            # multiple errors => unresolvable
            return [-1]
        else:          # error in first K
            posns.append(start - 1)

    # ok, now find next k-mer overlapping an error, if any.
    while start < end:
        kmer = sequence[start:start + K]

        c = kh.get(kmer)
        if c < cutoff:
            pos = start + K - 1
            posns.append(pos)
            
            while start < end:
                if kh.get(sequence[start:start+K]) >= cutoff:
                    break
                start += 1
        else:
            start += 1

    if not posns:
        return None
        
    return posns


def add_n_posns(posns, sequence):
    loc = sequence.find('N')
    p = set(posns)

    while loc > -1:
        p.add(loc)
        loc = sequence.find('N', loc + 1)
            
    return list(sorted(p))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('table')
    parser.add_argument('sequences')
    parser.add_argument('-C', '--cutoff', default=3, type=int)
    parser.add_argument('--coverage', default=20, type=int)
    parser.add_argument('-V', '--variable', default=False, action='store_true')
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
                        default=sys.stdout)

    args = parser.parse_args()

    kh = khmer.load_countgraph(args.table)
    n_skipped_variable = 0
    n_total = 0

    print >>sys.stderr, "K:", kh.ksize()
    print >>sys.stderr, "CUTOFF:", args.cutoff
    if args.variable:
        print >>sys.stderr, "variable coverage flag set;"
        print >>sys.stderr, "NORMALIZE_LIMIT:", args.coverage
    else:
        print >>sys.stderr, "assuming even coverage - no -V"

    for n, record in enumerate(screed.open(args.sequences)):
        if n % 100000 == 0:
            print >>sys.stderr, '...', n
        seq = record.sequence.replace('N', 'A')

        n_total += 1

        varskip = False
        if args.variable:
            med, _, _ = kh.get_median_count(seq)
            if med < args.coverage:
                varskip = True
                n_skipped_variable += 1
            
        name = record.name.split()[0]
        if varskip:
            print >>args.outfile, name, 'V'
        else:
            #posns = find_spectral_error_positions(kh, seq, args.cutoff)
            posns = kh.find_spectral_error_positions(seq, args.cutoff)
            posns = add_n_posns(posns, record.sequence)
            print >>args.outfile, name, ",".join(map(str, posns))


    if args.variable:
        sys.stderr.write('Skipped %d reads of %d total due to -V\n' % \
                         (n_skipped_variable, n_total))

if __name__ == '__main__':
   main()
   
