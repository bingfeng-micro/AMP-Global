import os
import sys
import json
import re


outfile = sys.argv[2]
w = open(outfile,'w+')
indir = os.path.join(os.path.abspath(sys.argv[1]),"result")
for file in os.listdir(indir):
    if "json" in file:
        json_file = os.path.join(indir,file)
        f=open(json_file)
        data = json.load(f)
        cmd = data['command']
        fq1=""
        fq2=""
        if "-o " in cmd:
            fq1 = re.split('-o ',cmd)[1].split(' ')[0]
        if "-O " in cmd:
            fq2 = re.split('-O ',cmd)[1].split(' ')[0]
        reads_count = data['filtering_result']['passed_filter_reads']
        if fq2:
            w.write(fq1+' '+fq2+' '+str(reads_count)+'\n')
        else:
            w.write(fq1+' '+str(reads_count)+'\n')
        f.close()
w.close()
