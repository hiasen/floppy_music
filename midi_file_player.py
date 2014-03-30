from midi.MidiOutStream import MidiOutStream
from midi.MidiToText import MidiToText
from midi.MidiInFile import MidiInFile
from floppy_controller import FloppyManager, FloppyThread
import time
import threading


FLOPPY_LIST = [(3,5),(7,8),(10,12),(18,16),(19,15),(13,11)]

ON = True
OFF = False
channels = {}
class MidiToFloppy(MidiToText):
    def note_on(self, channel=0, note=0x40, velocity=0x40):
#        fm.update_time(0)
#        fm.play_midi_note(note=note)
#        print 'note_on  - ch:%02X,  note:%02X,  vel:%02X time:%s' % (channel, note, velocity, self.rel_time())
        channel_list = channels.setdefault(channel, [])
        channel_list.append((ON, note, self.abs_time() ))



    def note_off(self, channel=0, note=0x40, velocity=0x40):
#        print 'note_off - ch:%02X,  note:%02X,  vel:%02X time:%s' % (channel, note, velocity, self.rel_time())
#        fm.stop_midi_note(note=note)
        channel_list = channels.setdefault(channel, [])
        channel_list.append( (OFF, note, self.abs_time()))
       # self.note_list.append((OFF, channel, note, self.abs_time()))

midi_file_dir = '/home/pi/midi_files'
kirby = 'KirbysTheme.mid'
imperial_march = 'imperial_march.mid'
test_file = 'outer.mid'
test_file= r'Star_Wars_Imperial_March_2.mid'
test_file = 'James_Bond_Theme_1.mid'
test_file = 'Mario.mid'

import os
f = open(os.path.join(midi_file_dir,test_file), 'rb')
midiIn = MidiInFile(MidiToFloppy(), f)
midiIn.read()
channel_numbers = channels.keys()
one_channel = channels[channel_numbers[1]]
time_scaling = 0.005



def play_channel(one_channel, name, pins):
    ft = FloppyThread(name=name, dir_pin=pins[0], step_pin=pins[1])
    ft.reset_drive()
    ft.start()
    for i in xrange(len(one_channel)):
        on, note, abs_time = one_channel[i]
        duration = one_channel[i+1][2] - one_channel[i][2]
        if on:
            ft.play_midi_note(note)
            time.sleep(time_scaling*duration)
            ft.stop_playing()
        else:
            time.sleep(time_scaling*duration)
    ft.kill_thread()

the_threads = []
for i,key in enumerate(channels.keys()):
    current_thread = threading.Thread(target=play_channel, args=(channels[key], i, FLOPPY_LIST[i]))
    current_thread.start()
    the_threads.append(current_thread)

