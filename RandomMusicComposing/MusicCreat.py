# -*- coding = utf-8 -*-

import os
import json
import random

from midiutil.MidiFile import MIDIFile

def main():
    filename = input("请输入输出文件名：")
    subfolder = "output"
    if not os.path.isdir(subfolder):    # 如果文件夹不存在则建立
        os.mkdir(subfolder)
    name = subfolder + "/" + filename + ".mid"
    music = Music()
    music.create_file(filename=name,
                      piano=True,
                      perc=False,
                      chord=False)

class Music():
    def __init__(self, rules_path="rules.json", length=4, tempo=90):
        rulesPath = open(rules_path, "r")
        rules = json.load(rulesPath)
        rulesPath.close()

        self.length = length
        self.tempo = tempo

        self.rhythm = rules["rhythm"]  # 读取节奏规则 16拍4小节
        self.seq_chord = rules["seq_chord"]  # 读取和弦规则
        self.seq_perc = rules["seq_perc"]  # 读取击打乐规则
        self.velocity = rules["velocity"]  # 读取速率

        self.notes = rules["notes"]
        self.interval_upper = rules["interval_upper"]
        self.interval_lower = rules["interval_lower"]

        self.MyMIDI = MIDIFile(3)   # 创建三轨道
        self.piano_trackNumber = 0
        self.perc_trackNumber = 1
        self.chord_trackNumber = 2

    # 随机音调
    def random_note(self):
        last_played = 0
        while True:
            note = random.choice(range(1, len(self.notes) + 1))
            if not last_played:
                break
            else:
                # 音程限制
                if random.choice(self.interval_upper) >= abs(note - last_played) >= random.choice(self.interval_lower):
                    break
                else:
                    continue
        last_played = note
        return self.notes[last_played - 1]

    # 创建打击乐
    def create_perc_track(self):
        self.MyMIDI.addTrackName(
            track=self.perc_trackNumber,
            time=0, trackName="perc")
        self.MyMIDI.addTempo(
            track=self.perc_trackNumber,
            time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(
            tracknum=self.perc_trackNumber,
            channel=9, time=0, program=0)

        pos = 0
        while pos < self.length * 16:
            if pos != 0:
                self.MyMIDI.addNote(
                    track=self.perc_trackNumber,
                    channel=9, pitch=49, time=pos, duration=0.5, volume=102)
            for pitch, duration in self.seq_perc:
                relative_pos = pos - int(pos / 4) * 4
                if 0 <= relative_pos < 1:
                    vol = 102
                elif 2 <= relative_pos < 3:
                    vol = 96
                else:
                    vol = 92
                self.MyMIDI.addNote(
                    track=self.perc_trackNumber,
                    channel=9, pitch=pitch, time=pos, duration=duration, volume=vol)
                pos += duration

    # 创建钢琴乐
    def create_piano_track(self):
        seq_melody = []  # 创建序列
        for i in range(self.length):  # 读取长度
            for phrase in self.rhythm:  # 读取节奏
                for duration in phrase:
                    seq_melody.append((self.random_note(), duration))  # 随机音调

        self.MyMIDI.addTrackName(
            track=self.piano_trackNumber,
            time=0, trackName="piano")
        self.MyMIDI.addTempo(
            track=self.piano_trackNumber,
            time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(
            tracknum=self.piano_trackNumber,
            channel=0, time=0, program=0)

        pos = 0
        for pitch, duration in seq_melody:
            relative_pos = pos - int(pos / 4) * 4
            if 0 <= relative_pos < 1:
                vol = self.velocity["strong"]
            elif 2 <= relative_pos < 3:
                vol = self.velocity["intermediate"]
            else:
                vol = self.velocity["weak"]
            self.MyMIDI.addNote(
                track=self.piano_trackNumber,
                channel=0, pitch=pitch, time=pos, duration=duration, volume=vol)
            if relative_pos in [0, 2]:
                self.MyMIDI.addControllerEvent(
                    track=self.piano_trackNumber,
                    channel=0, time=pos, controller_number=64, parameter=127)
                self.MyMIDI.addControllerEvent(
                    track=self.piano_trackNumber,
                    channel=0, time=pos + 1.96875, controller_number=64, parameter=0)
            pos += duration

    # 创建和弦
    def create_chord_track(self):
        self.MyMIDI.addTrackName(
            track=self.chord_trackNumber,
            time=0, trackName="chords")
        self.MyMIDI.addTempo(
            track=self.chord_trackNumber,
            time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(
            tracknum=self.chord_trackNumber,
            channel=0, time=0, program=0)

        # C  D  E  F  G  A  B  | C  D  E  F  G  A  B  | C
        # 48 50 52 53 55 57 59 | 60 62 64 65 67 69 71 | 72

        pos = 0
        while pos < self.length * 16:
            for item in self.seq_chord:
                for pitch in item:
                    self.MyMIDI.addControllerEvent(
                        track=self.chord_trackNumber,
                        channel=0, time=pos, controller_number=64, parameter=127)
                    self.MyMIDI.addControllerEvent(
                        track=self.chord_trackNumber,
                        channel=0, time=pos + 1.96875, controller_number=64, parameter=0)

                    self.MyMIDI.addNote(
                        track=self.chord_trackNumber,
                        channel=0, pitch=pitch, time=pos, duration=2, volume=76)

                    self.MyMIDI.addControllerEvent(
                        track=self.chord_trackNumber,
                        channel=0, time=pos + 2, controller_number=64, parameter=127)
                    self.MyMIDI.addControllerEvent(
                        track=self.chord_trackNumber,
                        channel=0, time=pos + 3.96875, controller_number=64, parameter=0)

                    self.MyMIDI.addNote(
                        track=self.chord_trackNumber,
                        channel=0, pitch=pitch, time=pos + 2, duration=2, volume=68)
                pos += 4

    # 创建文件（单一版本）
    def create_file(self, filename, piano=True, chord=True, perc=True):
        if piano:
            self.create_piano_track()
        if chord:
            self.create_chord_track()
        if perc:
            self.create_perc_track()
        with open(filename, "wb") as midi_file:
            self.MyMIDI.writeFile(midi_file)

if __name__ == "__main__":
    main()
