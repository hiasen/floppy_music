import threading
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

FORWARD = 1
BACKWARD = -1
END_POSITION = 80

A_NOTE = 440.
FLOPPY_LIST = [(18,16),(10,12),(13,11),(3,5),(7,8),(19,15)]

def direction_to_boolean(direction):
    return direction==FORWARD

def midi_note_to_frequency(midi_note_number):
    return A_NOTE*2.**((midi_note_number-69)/12.)

class FloppyThread(threading.Thread):
    frequency = None
    _direction = FORWARD
    position = 0
    _half_period = None
    _killed = False

    def __init__(self, name, dir_pin, step_pin):
        self._play_event = threading.Event()
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)

        threading.Thread.__init__(self, name=name)


    def run(self):
        while(True):
            self._play_event.wait()
            if self._killed:
                self._play_event.clear()
                return
            self.one_period()

    def reset_drive(self):
        print('Reset drive', self.name)
        self.set_direction(BACKWARD)
        for i in range(100):
            GPIO.output(self.step_pin, True)
            time.sleep(0.001)
            GPIO.output(self.step_pin, False)
            time.sleep(0.001)
        self.position = 0
        self.set_direction(FORWARD)
        print('Finished resetting drive ', self.name)
        
        

    def set_direction(self, direction):
        print('{}: Change direction {}'.format(self.name, direction))
        self._direction = direction
        GPIO.output(self.dir_pin, direction_to_boolean(direction))

    def one_period(self):
#        print('{}: Move from position {}'.format(self.name, self.position))
        if self.position >= END_POSITION:
            self.set_direction(BACKWARD)
        elif self.position <= 0:
            self.set_direction(FORWARD)

        self.position += self._direction
#        print('{}: Move to position {}'.format(self.name, self.position))
        GPIO.output(self.step_pin, True)
        time.sleep(self._half_period)
        GPIO.output(self.step_pin, False)
        time.sleep(self._half_period)

    def stop_playing(self):
        print('{}: stop playing'.format(self.name))
        self._play_event.clear()

    def play_frequency(self, frequency):
        print('{}: Play frequency: {}'.format(self.name, frequency))
        self.frequency = frequency
        self._half_period = 0.5/frequency
        self._play_event.set()

    def play_midi_note(self, note):
        freq = midi_note_to_frequency(note)
        self.play_frequency(freq)

    def kill_thread(self):
        print('Kill thread: {}'.format(self.name))
        self.stop_playing()
        self._killed = True
        self._play_event.set()


class FloppyManager(object):

    def __init__(self, floppy_list=FLOPPY_LIST):
        self.all_floppys = []
        for i,pins in enumerate(floppy_list):
            dir_pin, step_pin = pins

            ft = FloppyThread(name='floppy{}'.format(i), dir_pin=dir_pin, step_pin=step_pin )
            ft.start()
            ft.reset_drive()
            self.all_floppys.append(ft)

        self.all_floppys.reverse()
        self.free_floppys = self.all_floppys[:]
        self.playing = {}

    def play_midi_note(self, note):
        try:
            floppy = self.free_floppys.pop()
        except IndexError:
            print('All floppys are used!')
            return
        self.playing[note] = floppy
        floppy.play_midi_note(note)

    def stop_midi_note(self, note):
        if note not in self.playing:
            return
        floppy = self.playing.pop(note)
        floppy.stop_playing()
        self.free_floppys.append(floppy)

    def kill_all_threads(self):
        for floppy in self.all_floppys:
            floppy.kill_thread()


def test1():
    dir_pin = 0
    step_pin = 1
    ft = FloppyThread(name='thread1', dir_pin=dir_pin, step_pin=step_pin)
    ft.reset_drive()
    ft.start()
    scala = [0,2,4,5,7,9,11,12]
    melody1 = [0, 0, 0, 4, None, 2,2,2,5,None, 4,4,2,2,0,None]
    ground_note = 29
    play_time = 0.5 
    note_time = 0.9*play_time 
    pause_time = 0.1*play_time
    play_array = [(ground_note + offset) if (offset is not None) else None for offset in melody1 ]
    try:
        while(True):
            for note in play_array:
                if note is None :
                    time.sleep(play_time)
                else:
                    ft.play_midi_note(note)
                    time.sleep(note_time)
                    ft.stop_playing()
                    time.sleep(pause_time)
    except KeyboardInterrupt:
        ft.kill_thread()
        GPIO.cleanup()

def test2():
    try:
        floppy_list = [(3,5),(8,7)]
        fm = FloppyManager(floppy_list = floppy_list)
        fm.play_midi_note(40)
        fm.play_midi_note(42)
        fm.play_midi_note(53)
        while(True): 
           time.sleep(1)
    except KeyboardInterrupt:
        fm.kill_all_threads()
        GPIO.cleanup()



if __name__ == '__main__':
    test2()
