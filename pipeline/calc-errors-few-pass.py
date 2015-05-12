#! /usr/bin/env python2
"""
Streaming error finding.

% python calc-errors-few-pass [ <data1> [ <data2> [ ... ] ] ]

Use -h for parameter help.
"""
import sys
import screed
import os
import khmer
import argparse
import tempfile
import shutil

DEFAULT_NORMALIZE_LIMIT = 20
DEFAULT_CUTOFF = 3

DEFAULT_K = 20
DEFAULT_N_HT = 4
DEFAULT_MIN_HASHSIZE = 1e6

# see Zhang et al., http://arxiv.org/abs/1309.2975
MAX_FALSE_POSITIVE_RATE = 0.8

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


def add_n_posns(posns, sequence):
    loc = sequence.find('N')
    p = set(posns)

    while loc > -1:
        p.add(loc)
        loc = sequence.find('N', loc + 1)
            
    return list(sorted(p))


def main():
    parser = argparse.ArgumentParser(description='XXX')

    env_ksize = os.environ.get('KHMER_KSIZE', DEFAULT_K)
    env_n_hashes = os.environ.get('KHMER_N_HASHES', DEFAULT_N_HT)
    env_hashsize = os.environ.get('KHMER_MIN_HASHSIZE', DEFAULT_MIN_HASHSIZE)

    parser.add_argument('--ksize', '-k', type=int, dest='ksize',
                        default=env_ksize,
                        help='k-mer size to use')
    parser.add_argument('--n_hashes', '-N', type=int, dest='n_hashes',
                        default=env_n_hashes,
                        help='number of hash tables to use')
    parser.add_argument('--hashsize', '-x', type=float, dest='min_hashsize',
                        default=env_hashsize,
                        help='lower bound on hashsize to use')

    parser.add_argument('--cutoff', '-C', type=int, dest='abund_cutoff',
                        help='remove k-mers below this abundance',
                        default=DEFAULT_CUTOFF)

    parser.add_argument('--normalize-to', '-Z', type=int, dest='normalize_to',
                        help='base cutoff on median k-mer abundance of this',
                        default=DEFAULT_NORMALIZE_LIMIT)

    parser.add_argument('--variable-coverage', '-V', action='store_true',
                        dest='variable_coverage', default=False,
                        help='Only trim low-abundance k-mers from sequences '
                        'that have high coverage.')
    parser.add_argument('--tempdir', '-T', type=str, dest='tempdir',
                        default='./')

    parser.add_argument('input_filenames', nargs='+')
    args = parser.parse_args()

    K = args.ksize
    HT_SIZE = args.min_hashsize
    N_HT = args.n_hashes

    CUTOFF = args.abund_cutoff
    NORMALIZE_LIMIT = args.normalize_to

    print >>sys.stderr, "K:", K
    print >>sys.stderr, "HT SIZE:", HT_SIZE
    print >>sys.stderr, "N HT:", N_HT
    print >>sys.stderr, "CUTOFF:", CUTOFF
    print >>sys.stderr, "NORMALIZE_LIMIT:", NORMALIZE_LIMIT

    print >>sys.stderr, 'making hashtable'
    ht = khmer.new_counting_hash(K, HT_SIZE, N_HT)

    tempdir = tempfile.mkdtemp('khmer', 'tmp', args.tempdir)
    print >>sys.stderr, 'created temporary directory %s; ' % tempdir + \
          'use -T to change location'

    ###

    save_pass2 = 0

    read_bp = 0
    read_reads = 0

    pass2list = []
    for filename in args.input_filenames:
        pass2filename = os.path.basename(filename) + '.pass2'
        pass2filename = os.path.join(tempdir, pass2filename)

        pass2list.append((filename, pass2filename))

        pass2fp = open(pass2filename, 'w')

        for n, read in enumerate(screed.open(filename)):
            if n % 100000 == 0:
                print >>sys.stderr, '...', n, filename, save_pass2, \
                      read_reads, read_bp
                
            read_reads += 1
            read_bp += len(read.sequence)

            seq = read.sequence.replace('N', 'A')
            med, _, _ = ht.get_median_count(seq)

            # has this portion of the graph saturated? if not,
            # consume & save => pass2.
            if med < NORMALIZE_LIMIT:
                ht.consume(seq)
                pass2fp.write(output_single(read))
                save_pass2 += 1
            else:
                posns = ht.find_spectral_error_positions(seq, CUTOFF)
                posns = add_n_posns(posns, read.sequence)
                print read.name, ",".join(map(str, posns))
                
        pass2fp.close()

        print >>sys.stderr, '%s: kept aside %d of %d from first pass, in %s' %\
              (filename, save_pass2, n + 1, filename)

    n_omitted = 0
    for orig_filename, pass2filename in pass2list:
        print >>sys.stderr,'second pass: looking at ' + \
              'sequences kept aside in %s' % pass2filename
        for n, read in enumerate(screed.open(pass2filename)):
            if n % 100000 == 0:
                print >>sys.stderr, '... x 2', n, pass2filename, read_reads, \
                      read_bp

            seq = read.sequence.replace('N', 'A')
            med, _, _ = ht.get_median_count(seq)

            if med >= NORMALIZE_LIMIT or not args.variable_coverage:
                posns = ht.find_spectral_error_positions(seq, CUTOFF)
                posns = add_n_posns(posns, read.sequence)
                print read.name, ",".join(map(str, posns))

            if args.variable_coverage and med < NORMALIZE_LIMIT:
                print read.name, 'V'
                n_omitted += 1

        print >>sys.stderr, 'removing %s' % pass2filename
        os.unlink(pass2filename)

    print >>sys.stderr, 'removing temp directory & contents (%s)' % tempdir
    shutil.rmtree(tempdir)

    print >>sys.stderr, 'read %d reads, %d bp' % (read_reads, read_bp,)
    if args.variable_coverage:
        print >>sys.stderr, 'omitted %d reads for -V' % (n_omitted)

    fp_rate = khmer.calc_expected_collisions(ht)
    print >>sys.stderr, \
          'fp rate estimated to be {fpr:1.3f}'.format(fpr=fp_rate)

    if fp_rate > MAX_FALSE_POSITIVE_RATE:
        print >> sys.stderr, "**"
        print >> sys.stderr, ("** ERROR: the k-mer counting table is too small"
                              " for this data set. Increase tablesize/# "
                              "tables.")
        print >> sys.stderr, "**"
        print >> sys.stderr, "** Do not use these results!!"
        sys.exit(1)

if __name__ == '__main__':
    main()
