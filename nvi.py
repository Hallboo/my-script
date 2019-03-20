import os
import sys
import commands
nvioutput=commands.getoutput("nvidia-smi | grep '|[^|]*[0-9][^|]*C[^|]*MiB[^|]*|' | awk '{print $2\"|\"$3\"|\"$5\"|\"$6}'")
nvilist=nvioutput.split("\n")
#print(nvilist)
split_line='-'*60
print("\n" + split_line)
if len(nvilist[0]) == 0:
    print('\tNone')
    print(split_line + "\n")
    sys.exit()
for x in nvilist:
    one_line = x.split("|")
    user = commands.getoutput("ps -aux | grep " + one_line[1] + " | grep -v grep | awk '{print $1}'")
    #print(one_line[1])
    user = user.split('\n')[0]
    #print(user)
    print("\t%s\t%s\t%s\t%-14s\t%s"%(one_line[0],user,one_line[1],one_line[2],one_line[3]))
print(split_line + "\n")
