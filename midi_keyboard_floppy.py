import pygame.midi as midi
from floppy_controller import FloppyManager




import time

midi.init()

MIDI_DEVICE_ID = 3

midi_input = midi.Input(MIDI_DEVICE_ID)

def polling():
    fm = FloppyManager()
    while(True):
        evs = midi_input.read(10)
        for ev, timestamp in evs:
            print ev,timestamp
            up = ev[0] == 128
            down = ev[0] == 144
            midi_note = ev[1]
            if down:
                print('DOWN:{}'.format(midi_note))
                fm.play_midi_note(midi_note)
            elif up:
                print('UP:{}'.format(midi_note))
                fm.stop_midi_note(midi_note)
            else:
                print('UNKNOWN:')
            
                
        time.sleep(0.001)



def clean_up():
    print('Cleaning up')
    midi_input.close()
    midi.quit()

try:
    polling()
except KeyboardInterrupt:
    clean_up()
    raise

clean_up()
