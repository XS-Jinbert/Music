# -*- coding = utf-8 -*-
from mido import Message, MidiFile, MidiTrack, MetaMessage
import json

def main():
    # loadFile("Music/憧憬と屍の道-进击的巨人第三季OP2 .mid")
    # saveJson(loadMidi("Music/Astronomia-黑人抬棺.mid"), "黑人抬棺")
    creatMidi("rules/黑人抬棺.json", "15_黑人抬棺")

def loadMidi(FilePath):
    mid = MidiFile(FilePath)    # 打开文件
    music = {}                  # 保存音乐信息
    for i, track in enumerate(mid.tracks):  # 获取音乐轨道
        print("Track{}:{}".format(i, track.name))
        music["Track{}".format(i)] = {  # 每个轨道主要内容
            "time_signature": [],       # 音乐主要元数据
            "set_tempo": [],
            "program_change": [],             # 音符结束信号
            "key_signature": [],        # 音调信号
            "note": [],              # 音符信号
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

if __name__ == "__main__":
    main()