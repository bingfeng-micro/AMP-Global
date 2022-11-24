import os
import sys
from Bio import SeqIO


indir = sys.argv[1]
outfile = sys.argv[2]

w = open(outfile,'w+')
for file in os.listdir(indir):
	infile = os.path.join(indir,file)
	sample = file.split('.')[0]
	for rec in SeqIO.parse(infile,'fasta'):
		descs = rec.description.split('#')
		name = descs[0].strip()
		contig_id = '_'.join(name.split('_')[:-1])
		start = descs[1].strip()
		end = descs[2].strip()
		w.write(contig_id+'\t'+name+'\t'+start+'\t'+end+'\t'+sample+'\n')
w.close()