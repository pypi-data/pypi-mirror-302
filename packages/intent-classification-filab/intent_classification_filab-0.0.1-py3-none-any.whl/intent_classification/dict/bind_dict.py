import argparse
import sys
import pandas as pd

def bind_dict(input_files, output_file):
#    filelist = input_files.split(',')

    dup = []

    for i in input_files:
        f = open(i.strip(), 'r')

        lines = f.readlines()

#        dup = []

        for line in lines:
            l = line.split('\t')
            if line not in dup and not line.isspace() and len(l[0]) >= 2:
                dup.append(line)
        f.close()

    f2 = open(output_file, 'w')

    for d in dup:
        i = d.split('\t')
        if i[2].strip() != '0':
           f2.write(i[0].strip())
           f2.write('\t')
           f2.write(i[2].strip())
           f2.write('\n')
    f2.close()

#    f3 = open(output_file2, 'w')

#    for d in dup:
#        f3.write(d.strip())
#        f3.write('\n')
#    f3.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bind_dict')

    parser.add_argument('-i', '--inputfile', nargs='+')
    parser.add_argument('-o', '--outputfile')
#    parser.add_argument('-o2', '--outputfile2')
    args = parser.parse_args()
    
#    input_files = sys.argv[1]
#    output_file = sys.argv[2]

    bind_dict(args.inputfile, args.outputfile)
