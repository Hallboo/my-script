#encoding:utf-8
import wave
import os
import argparse

corpus_second = 0.0
corpus_min   = 0.0
corpus_hour  = 0.0
audio_file_count = 0
max_length = 0
max_length_file = "unknow"
min_length = 0
min_length_file = "unknow"
sample_rate = 0
parser = argparse.ArgumentParser(description = "Calculate the duration of the corpus.")
parser.add_argument("wav_dir",help="audio file dir (wav_dir/.../.wav)")
args = parser.parse_args()
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory,args.wav_dir)

def traverse(file_path):
    global corpus_second,audio_file_count,max_length,max_length_file,min_length,min_length_file
    file_list = os.listdir(file_path)
    for onefile in file_list:
        file_or_dir = os.path.join(file_path,onefile)
        if os.path.isfile(file_or_dir) and file_or_dir.split(".")[-1]=="wav":
            try:
                onewave = wave.open(file_or_dir,"rb")
                channels, width, framerate, frames = onewave.getparams()[:4]
                onewave.close()
                if max_length < frames:
                    max_length = frames
                    max_length_file = file_or_dir
                if min_length > frames or min_length == 0:
                    min_length = frames
                    min_length_file = file_or_dir
                second = frames/(framerate*1.0)
                corpus_second += second
                print(file_or_dir + "\n\t" + "channels:%d width:%2d framerate:%6d frames:%8d duration:%.03f"
                      %(channels,width,framerate,frames,second))
                audio_file_count+=1
            except:
                print("error: "+ file_or_dir) 
        elif os.path.isdir(file_or_dir):
            traverse(file_or_dir)

traverse(file_path)
corpus_min  = corpus_second/60
corpus_hour = corpus_min/60
ti="-"*100
print("\n"+ti+"\n")
ind=" "
print(ind+"文件个数 : %d"%audio_file_count)
if corpus_min < 1:
    print(ind+"语料时长 : %f（秒）"%corpus_second)
if corpus_min >= 1 and corpus_hour < 1:
    print(ind+"语料时长 : %.3f（分钟）"%corpus_min)
if corpus_hour >= 1:
    print(ind+"语料时长 : %.3f（小时）"%corpus_hour)
print(ind+"最长语音 : " + str(max_length) + "\n " + max_length_file)
print(ind+"最短语音 ：" + str(min_length) + "\n " + min_length_file)
print('\n')
