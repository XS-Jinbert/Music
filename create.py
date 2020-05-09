# -*- coding = utf-8 -*-
from mido import Message, MidiFile, MidiTrack, MetaMessage
import json

def main():
    creatMidi("rules/下山.json", "15_下山")

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