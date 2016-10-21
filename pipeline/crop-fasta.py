#! /usr/bin/env python
import os

def read_FASTA(filename):
    genome = ""
    f = open(filename, "r")
    while 1:
        temp = f.readline().replace("\n","")
        if not temp:
            break
        if temp[0] == '>':
            continue
        genome += temp
    print("File read.")
    return genome.upper()


def crop_FASTA(sequence, filename, cropSize):
    header = ">" + os.path.splitext(filename)[0]
    index = open(filename, "w")
    index.write(header+"\n")
    counter = 0
    counter_w = 0
    while (counter_w < cropSize):
        if sequence[counter] != "N":
            counter_w += 1
            index.write(sequence[counter])
            if counter_w % 70 == 0:
                index.write("\n")
#            if counter_w % 10000 == 0:
#                print(str(counter_w))
        counter += 1
    print("Cropped file created.")
    index.close()


def init(file, cropSize):
    ref = read_FASTA(file)
    filename = os.path.splitext(file)[0] + "-crop.fa"
    crop_FASTA(ref, filename, cropSize)

               
def start():
    print "Enter name of your FASTA file:"
    file = raw_input()
    print "Enter desired size for cropping:"
    cropSize = int(raw_input())
    init(file,cropSize)

init("chr21.fa",5000000)
#start()
