import os
import sys
from Bio import SeqIO
from concurrent.futures import ThreadPoolExecutor
import subprocess
import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--diamond_result","-i",help="蛋白质数据库diamond比对结果文件表格")
    parser.add_argument("--outdir","-o",help="输出目录")
    parser.add_argument("--mag_file","-f",help="MAG核酸序列文件")
    parser.add_argument("--cds_file","-s",help="MAG核酸序列对应的CDS的位置文件")
    parser.add_argument("--identity","-d",help="比对一致性阈值")
    parser.add_argument("--coverage","-c",help="比对覆盖度阈值")
    parser.add_argument("--up_length",help="要提取MAG上游序列长度",default=5000)
    parser.add_argument("--down_length",help="要提取MAG下游序列长度",default=5000)
    parser.add_argument("--min_length",help="上下游序列最小长度",default=50)

    args = parser.parse_args()
    return args

def main():
    outdir = os.path.abspath(args.outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    final_table = os.path.join(outdir,"diamond.hits.tsv")
    up_down_file = os.path.join(outdir,"up_down.fasta")
    diamond_result = args.diamond_result
    mag_file = args.mag_file
    identity = float(args.identity)
    coverage = float(args.coverage)
    up_length = int(args.up_length)
    down_length = int(args.down_length)
    cds_file = args.cds_file
    min_length = int(args.min_length)
    cds_positons = {}
    f = open(cds_file)
    #contig_id,protein_id,start,end,sample
    for lines in f:
        if lines.strip():
            data = lines.strip().split('\t')
            contig_id = data[0]
            cds_id = data[1]
            start = int(data[2])
            end = int(data[3])
            sample = data[4]
            if contig_id not in cds_positons:
                cds_positons[contig_id] = {}
            cds_positons[contig_id][cds_id] = [start,end,sample]
    f.close()
    seq_dict = {}
    for rec in SeqIO.parse(mag_file,'fasta'):
        seq_dict[rec.id] = str(rec.seq)
    w1 = open(final_table,'w+')
    w2 = open(up_down_file,'w+')
    w1.write('sample\tcontig_id\tprotein_id\thit_name\tidentity\tcoverage\n')
    f = open(diamond_result)
    for lines in f:
        if lines.strip():
            data = lines.strip().split('\t')
            qid = data[0]
            sid = data[1]
            contig_id = '_'.join(qid.split('_')[:-1])
            ident = float(data[2])
            q_start = int(data[6])
            q_end = int(data[7])
            if q_start > q_end:
                q_start,q_end = q_end,q_start
            s_start = int(data[8])
            s_end = int(data[9])
            s_len = int(data[-1])
            cov = abs(s_end-s_start+1)*100/s_len
            if ident >= identity and cov >= coverage:
                contig_seq = seq_dict[contig_id]
                cds_pos = cds_positons[contig_id][qid]
                sample = cds_pos[2]
                w1.write(sample+'\t'+contig_id+'\t'+qid+'\t'+sid+'\t'+str(ident)+'\t'+str(round(cov,2))+'\n')
                s1 = (q_start-1)*3+1
                e1 = q_end*3
                s2 = cds_pos[0] + s1 -1
                e2 = cds_pos[0] + e1 -1
                if s2-1-up_length >= 0:
                    up_seq = contig_seq[s2-1-up_length:s2-1]
                else:
                    up_seq = contig_seq[:s2-1]
                down_seq = contig_seq[e2:e2+down_length]
                if len(up_seq) >= min_length:
                    w2.write('>'+sample+'~'+qid+'~'+sid+'~up'+str(up_length)+'\n'+up_seq+'\n')
                if len(down_seq) >= min_length:
                    w2.write('>'+sample+'~'+qid+'~'+sid+'~down'+str(down_length)+'\n'+down_seq+'\n')

    f.close()
    w1.close()
    w2.close()




if __name__ == '__main__':
    args = arg_parse()
    main()