# -*- coding = utf-8 -*-
from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido
import json



def main():
    # loadFile("Music/憧憬と屍の道-进击的巨人第三季OP2 .mid")
    # saveJson(loadMidi("Music/Astronomia-黑人抬棺.mid"), "黑人抬棺")
    creatMidi("rules/黑人抬棺.json", "15_黑人抬棺")

def firstLearn():
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # program_change表示乐器音色
    # 音色表: https://blog.csdn.net/ruyulin/article/details/84103186
    track.append(Message('program_change', program=0, time=0))
    # note_on:音符开始
    # note_off:音符结束
    # velocity:音量
    # time:持续时间（）
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))

    mid.save('test_song_0.mid')

def loadMidi(FilePath):
    mid = MidiFile(FilePath)    # 打开文件
    music = {}                  # 保存音乐信息
    for i, track in enumerate(mid.tracks):  # 获取音乐轨道
        print("Track{}:{}".format(i, track.name))
        music["Track{}".format(i)] = {  # 每个轨道主要内容
            "time_signature": [],       # 音乐主要元数据
            "set_tempo": [],            # 节拍分辨率：默认500000微秒一拍，即120拍每分钟
            "program_change": [],       # 音符结束信号
            "key_signature": [],        # 音调信号
            "note": [],                 # 音符信号
        }
        for msg in track:
            print(msg)
            if msg.type == "time_signature":    # 音乐主要元数据
                time_signature = {}
                time_signature["numerator"] = msg.numerator         # 每小节节拍数
                time_signature["denominator"] = msg.denominator     # 小节数
                time_signature["clocks_per_click"] = msg.clocks_per_click
                time_signature["notated_32nd_notes_per_beat"] = msg.notated_32nd_notes_per_beat
                time_signature["time"] = msg.time
                music["Track{}".format(i)]["time_signature"].append(time_signature)     # 添加信号保存
            elif msg.type == "set_tempo":   # 音调信号
                set_tempo = {}
                set_tempo["tempo"] = msg.tempo      # 音调信号
                set_tempo["time"] = msg.time
                music["Track{}".format(i)]["set_tempo"].append(set_tempo)   # 添加信号保存
            elif msg.type == "key_signature":   # 音调信号
                key_signature = {}
                key_signature["key"] = msg.key      # 音调信号
                key_signature["time"] = msg.time
                music["Track{}".format(i)]["key_signature"].append(key_signature)   # 添加信号保存
            elif msg.type == "program_change":   # 音调信号
                program_change = {}
                program_change["program"] = msg.program     # 乐器
                program_change["channel"] = msg.channel     # 通道
                program_change["time"] = msg.time  # 时间
                music["Track{}".format(i)]["program_change"].append(program_change)   # 添加信号保存
            elif msg.type == "note_on" or msg.type == "note_off":     # 音符开始信号
                note = {}
                note["type"] = msg.type             # 音符
                note["note"] = msg.note             # 音符
                note["channel"] = msg.channel       # 通道
                note["velocity"] = msg.velocity     # 音量
                note["time"] = msg.time             # 时间
                music["Track{}".format(i)]["note"].append(note)   # 添加信号保存
    return music

def saveJson(music,filename):
    savepath = "rules/"+filename+".json"
    with open(savepath, "w") as f:
        rule = json.dump(music, f, indent=4)
        print(music)

def creatMidi(jsonPath, fileName):
    j = open(jsonPath, "r")
    rule = json.load(j)
    j.close()

    mid = MidiFile()
    n = 0
    for count in rule:
        if n == 0:
            pass
            # track = MidiTrack()
            # mid.tracks.append(track)
            # track.append(MetaMessage('time_signature',
            #                      numerator=rule["Track{}".format(n)]["time_signature"][0]["numerator"],
            #                      denominator=rule["Track{}".format(n)]["time_signature"][0]["denominator"],
            #                      clocks_per_click=rule["Track{}".format(n)]["time_signature"][0]["clocks_per_click"],
            #                      notated_32nd_notes_per_beat=rule["Track{}".format(n)]["time_signature"][0]["notated_32nd_notes_per_beat"],
            #                      time=rule["Track{}".format(n)]["time_signature"][0]["time"]))
            # track.append(MetaMessage('key_signature',
            #                          key=rule["Track{}".format(1)]["key_signature"][0]["key"],
            #                          time=rule["Track{}".format(1)]["key_signature"][0]["time"]))

        else:
            track = MidiTrack()
            mid.tracks.append(track)
            track.append(MetaMessage('time_signature',
                                     numerator=rule["Track{}".format(0)]["time_signature"][0]["numerator"],
                                     denominator=rule["Track{}".format(0)]["time_signature"][0]["denominator"],
                                     clocks_per_click=rule["Track{}".format(0)]["time_signature"][0]["clocks_per_click"],
                                     notated_32nd_notes_per_beat=rule["Track{}".format(0)]["time_signature"][0][
                                         "notated_32nd_notes_per_beat"],
                                     time=rule["Track{}".format(0)]["time_signature"][0]["time"]))
            track.append(MetaMessage('set_tempo',
                                 tempo=rule["Track{}".format(0)]["set_tempo"][0]["tempo"],
                                 time=rule["Track{}".format(0)]["set_tempo"][0]["time"]))
            track.append(Message('program_change',
                                 program=15,
                                 channel=rule["Track{}".format(n)]["program_change"][0]["channel"],
                                 time=rule["Track{}".format(n)]["program_change"][0]["time"]))
            track.append(MetaMessage('key_signature',
                                 key=rule["Track{}".format(n)]["key_signature"][0]["key"],
                                 time=rule["Track{}".format(n)]["key_signature"][0]["time"]))
            for i in rule["Track{}".format(n)]["note"]:
                track.append(Message(i["type"],
                                     note=i["note"],
                                     channel=i["channel"],
                                     velocity=i["velocity"],
                                     time=i["time"]))
        n += 1
    mid.save("output/"+fileName+".mid")

class FirstMusic():
    def __init__(self, bpm=90, numerator=4, denominator=4):
        self.tempo = mido.bpm2tempo(bpm)
        # time_signature表示曲风
        # numerator表示节拍，denominator表示小节
        # numerator/denominator = 4/4
        self.meta_time = MetaMessage('time_signature', numerator=numerator, denominator=denominator)

        self.meta_tempo = MetaMessage('set_tempo', tempo=self.tempo, time=0)

        self.meta_tone = MetaMessage('key_signature', key='C')

if __name__ == "__main__":
    main()