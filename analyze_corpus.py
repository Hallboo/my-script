# encoding = 'utf-8'
# Zhang Haobo
# 20190308
# 统计语料脚本

import os
import wave
import argparse

class Wave(object):
    def __init__(self, name = 'Unknow', channels = 1, 
                    width = 2, framerate = 16000, frames = 0):
        self.name = name
        self.channels = channels
        self.width = width
        self.framerate = framerate
        self.frames = frames
        self.second = frames/framerate

class statistic(object):
    def __init__(self):
        self.count = 0
        self.corpus_dur = 0.0
        self.max_head = Wave('Unknow_max',frames = 0)
        self.min_head = Wave('Unknow_min',frames = 0xffffffff)
        self.same = True
        self.framerate = 16000
        self.width = 2
        self.channels = 1
    
    def scan(self, wave_head):
        self.count += 1
        self.corpus_dur += wave_head.second
        self.averag_dur = self.corpus_dur / self.count
        if wave_head.second > self.max_head.second:
            self.max_head = wave_head
        if wave_head.second < self.min_head.second:
            self.min_head = wave_head
        
        # 判断语音的参数不一致，这里没有考虑channel的不一样
        diff_flag = wave_head.framerate != self.framerate or wave_head.width != self.width
        # diff_flag = diff_flag or wave_head.channels
        if diff_flag and self.count>1:
            self.same = False
        elif self.count == 1:
            self.framerate = wave_head.framerate
            self.width = wave_head.width
            self.channels = wave_head.channels
        if wave_head.channels == 2:
            print(wave_head.name + '\n' + str(wave_head.channels))

    
    def report(self):
        self.bps = self.framerate * self.width * 8
        corpus_min  = self.corpus_dur/60
        corpus_hour = corpus_min/60
        ti="-"*80
        ind=" "
        print("\n" + ti + "\n")
        print(ind + "文件个数 : %d"%self.count)
        if corpus_min < 1:
            print(ind + "语料时长 : %f 秒"%corpus_second)
        if corpus_min >= 1 and corpus_hour < 1:
            print(ind + "语料时长 : %.3f 分钟"%corpus_min)
        if corpus_hour >= 1:
            print(ind + "语料时长 : %.3f 小时"%corpus_hour)
        print(ind + "最长语音 : %0.3f 秒\n %s"%(self.max_head.second,self.max_head.name))
        print(ind + "最短语音 ：%0.3f 秒\n %s"%(self.min_head.second,self.min_head.name))
        print(ind + "平均时长 ：%0.3f 秒"%self.averag_dur)
        
        if self.same:
            print(ind + "音频参数 ：一致")
            print(ind + "数据宽度 ：%d bit"%(self.width*8))
            print(ind + "采样率 ：%.1fk Hz"%(self.framerate / 1000))
            print(ind + "波特率 ：%.1fk bps"%(self.bps / 1000))
        else:
            print(ind + "音频参数 ：不一致")
        print('\n')

def traverse(file_path,st):
    file_list = os.listdir(file_path)
    for one_file in file_list:
        
        file_or_dir = os.path.join(file_path, one_file)
        # wave file
        if os.path.isfile(file_or_dir) and file_or_dir.split(".")[-1]=="wav":
            wave_file = file_or_dir
            one_wave_file = wave.open(wave_file, 'rb')
            channels, width, framerate, frames = one_wave_file.getparams()[:4]
            # print(wave_file + "\n\t" + "channels:%d width:%2d framerate:%6d frames:%8d"
                    #   %(channels,width,framerate,frames))
            one_wave_head = Wave(wave_file, channels, width, framerate, frames)
            st.scan(one_wave_head)
        # dir
        elif os.path.isdir(file_or_dir):
            traverse(file_or_dir,st)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Calculate the duration of the corpus.")
    parser.add_argument("wav_dir",help="audio file dir (wav_dir/.../.wav)")
    args = parser.parse_args()
    st = statistic()
    traverse(args.wav_dir,st)
    st.report()