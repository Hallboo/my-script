#encoding:utf-8
import wave
import os
import argparse

corpusecond = 0.0
corpusmin   = 0.0
corpushour  = 0.0
parser = argparse.ArgumentParser(description = "Calculate the duration of the corpus.")
parser.add_argument("wav_dir",help="audio file dir (wav_dir/*.wav)")
args = parser.parse_args()
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory,args.wav_dir)
file_list = os.listdir(file_path)
count = 0
#print("find file number:%d"%len(file_list))
for onefile in file_list:
    try:
        onefile_dir = os.path.join(file_path,onefile)
        onewave = wave.open(onefile_dir,"rb")
        oneparams = onewave.getparams()[:4]
        nchannels, sampwidth, framerate, nframes = oneparams[:4]
        second = nframes/(framerate*1.0)
        corpusecond += second
        channels,width,framerate,frames  = oneparams[:4]
        print(onefile + "\tchannels:%d width:%2d framerate:%6d frames:%8d duration:%.03f"%(channels,width,framerate,frames,second))
        count+=1
    except:
        pass
corpusmin  = corpusecond/60
corpushour = corpusmin/60
print("\n*************************************************\n")
ind="  "
print(ind+"文件个数 : %d"%count)
if corpusmin < 1:
    print(ind+"语料时长 : %.3f（秒）"%corpusecond)
if corpusmin >= 1 and corpushour < 1:
    print(ind+"语料时长 : %.3f（分钟）"%corpusmin)
if corpushour >= 1:
    print(ind+"语料时长 : %.3f（小时）"%corpushour)
print("\n*************************************************\n")
