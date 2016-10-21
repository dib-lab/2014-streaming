#! /usr/bin/env python
"""
Compare two lists of error positions ('pos files').

first file is assumed to be prediction, second file is assumed to be "truth."
"""
import argparse
import sys
import screed

def do_counting(first, second, ignore_set):
    n = 0                               # reads w/errors in first
    o = 0                               # reads w/errors in second
    
    matches = 0                         # exact matches
    mismatches = 0                      # 
    n_ignored = 0                       # intentionally ignored

    for k, va in first.iteritems():
        if k in ignore_set:             # ignoreme
            n_ignored += 1
            continue

        vb = second.get(k)
        if not va and not vb:           # no errors! TN.
            continue

        # these conditions are handled elsewhere
        if va and not vb: # part of fp; see incorr_in_a intersect corr_in_b
            continue
        if vb and not va: # fn; see corr_in_a intersect incorr in b
            continue
        
        n += 1
        if va == vb:                    # exact match!
            matches += 1
        else:
            mismatches += 1             # no match :(

    for k, vb in second.iteritems():
        if k in ignore_set:             # ignoreme
            continue
        
        if len(vb):
            o += 1

    return n, o, matches, mismatches, n_ignored


# read in list of error positions per read
def read_pos_file(filename, ignore_set):
    for line in open(filename):
        line = line.strip()
        try:
            read, posns = line.split(' ', 2)
        except ValueError:
            read = line
            posns = []

        if read in ignore_set:
            posns = []
        elif posns:
            if posns is 'V':            # ignore variable coverage foo
                ignore_set.add(read)
                posns = []
            else:
                posns = list(sorted(map(int, posns.split(','))))

        yield read, posns


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--variable', default=False, action='store_true')
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    parser.add_argument('pos_a')
    parser.add_argument('pos_b')
    parser.add_argument('reads')
    args = parser.parse_args()

    ignore_set = set() # reads to ignore because of low coverage

    # read in two lists of positions & errors
    print >>sys.stderr, 'loading posfiles'
    a = dict(read_pos_file(args.pos_a, ignore_set))
    b = dict(read_pos_file(args.pos_b, ignore_set))

    if not args.variable:               # eliminate ignore_set
        ignore_set = set()

    # get list of all reads
    print >>sys.stderr, 'loading reads from', args.reads
    all_names = set()

    total_reads = 0
    for record in screed.open(args.reads):
        total_reads += 1
        if record.name not in ignore_set:
            all_names.add(record.name.split()[0])

    print >>sys.stderr, 'done!'
    
    # reads we pay attention to
    tracked_reads = len(all_names)
    n_ignored = total_reads - tracked_reads

    n, o, matches, mismatches, n_ignoredXX = do_counting(a, b, ignore_set)

    print 'total # of reads: %d' % (total_reads,)
    print 'IGNORED due to -V: %d (%d, %.2f%%)' % (n_ignored,
                                                  tracked_reads,
               tracked_reads / float(total_reads) * 100.)
    print 'total # of tracked reads:', tracked_reads
    
    print '%d erroneous reads in %s' % (n, args.pos_a)
    print '%d erroneous reads in %s' % (o, args.pos_b)
    print '%d reads in common => all error positions AGREE' % (matches,)
    print '%d DISAGREE' % (mismatches,)

    # assume a is prediction, b is correct
    
    incorrect_in_a = set([ k for k in a if a[k] ])
    incorrect_in_b = set([ k for k in b if b[k] ])
    correct_in_a = all_names - set([ k for k in a if a[k] ])
    correct_in_b = all_names - set([ k for k in b if b[k] ])
    
    if args.debug:
        print 'DDD incorrect in a:', len(incorrect_in_a)
        print 'DDD incorrect in b:', len(incorrect_in_b)
        print 'DDD correct in a:', len(correct_in_a)
        print 'DDD correct in b:', len(correct_in_b)
    
    # m is reads thought to be erroneous by a, agree exactly with b
    tp = matches

    # fp: reads thought to be erroneous by a, but actually correct (in b)
    #     + places where a called errors that were incorrect
    fp = mismatches + len(incorrect_in_a.intersection(correct_in_b))

    if args.debug:
        print 'DDD incorrect in a, correct in b:', \
              incorrect_in_a.intersection(correct_in_b)

    # fn: reads thought to be correct by a, but actually erroneous (in b)
    fn = len(correct_in_a.intersection(incorrect_in_b))

    # tn: reads thought to be correct in both a and b
    tn = len(correct_in_a.intersection(correct_in_b))

    print 'TP:', tp
    print 'TN:', tn
    print 'FP: %d (%d + %d)' % (fp,
                                mismatches,
                                len(incorrect_in_a.intersection(correct_in_b)))
    print 'FN:', fn

    print 'sensitivity:', tp / float(tp + fn)
    print 'specificity:', tn / float(tn + fp)

    assert n <= total_reads
    assert o <= total_reads
# assert n_ignored == n_ignoredXX
    
    assert len(all_names) == tp + tn + fp + fn, (
           len(all_names) - (tp+tn+fp+fn),
           len(all_names),
           tp,
           tn,
           fp,
           fn)
    
if __name__ == '__main__':
    main()
