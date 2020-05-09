# -*- coding = utf-8 -*-

import mido

midi_file_path = 'D:\projects\Python\Music\Music\下山-要想练就绝世武功就要忍受常人难忍受的痛-抖音热歌.mid'

bpm = 82  # BPM 是必须的，这一个音频人员知道是什么

tap_value = 10  # 定义点击的值
wipe_value = 11  # 定义滑动的值
hold_value = 12  # 定义按住的值

# 这一个是为了适应人的听感，而加的偏移值，midi 文件的时间是准的
# 但是人耳朵听起来可能不是很准，最终是以人耳听起来准为目标
# 这个值不固定，根据自己游戏的音乐类型不同，以及做音频的人的听感不同，而设定，可以是正的，可以是负的
time_offset = 0.25

def get_base_notes_data(_midi_file_path, _bpm):
    mid = mido.midifiles.MidiFile(_midi_file_path, debug=True)
    tempo = mido.bpm2tempo(_bpm)

    _note_list = []
    i = 0

    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        passed_time = 0
        for msg in track:
            ab_time = mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
            real_time = ab_time + passed_time
            passed_time += ab_time
            # print(msg, " passed time=" + str(ab_time), " read time=" + str(round(real_time, 3)))
            if msg.type == "note_on":
                note_value = msg.note
                if note_value == tap_value:
                    note_name = "tap"
                elif note_value == wipe_value:
                    note_name = "wipe"
                elif note_value == hold_value:
                    note_name = "hold"
                else:
                    note_name = ""
                if note_name != "":
                    note_data = {"note_name": note_name, "time": round(real_time + time_offset, 3)}
                    _note_list.append(note_data)
                    print(note_data)

    return _note_list

get_base_notes_data(midi_file_path, bpm)