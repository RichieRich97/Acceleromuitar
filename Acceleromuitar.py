from microbit import *
import math

def midiNoteOn(chan, n, vel):
    MIDI_NOTE_ON = 0x90
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_ON | chan, n, vel])
    uart.write(msg)

def midiNoteOff(chan, n, vel):
    MIDI_NOTE_OFF = 0x80
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_OFF | chan, n, vel])
    uart.write(msg)

def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15:
        return
    if n > 127:
        return
    if value > 127:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)

def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

Start()
lastA = False
lastB = False
lastC = False
cval = 0
last_tilt = 0
while True:
    a = button_a.is_pressed()
    b = button_b.is_pressed()
    c = pin2.is_touched()
    if a is True and lastA is False:
        midiNoteOn(0, 0, 127)
        display.show("1")
    elif a is False and lastA is True:
        midiNoteOff(0, 0, 127)
    if b is True and lastB is False:
        midiNoteOn(1, 0, 127)
        display.show("2")
    elif b is False and lastB is True:
        midiNoteOff(1, 0, 127)
    if c is True and lastC is False:
        if cval == 0:
            cval = 1
            midiNoteOn(2, 1, 127)
            pin1.write_digital(1)
            display.on()

        elif cval == 1:
            cval = 0
            midiNoteOn(2, 0, 127)
            pin1.write_digital(0)
            display.off()

    lastA = a
    lastB = b
    lastC = c
    current_tilt = accelerometer.get_y()
    if current_tilt != last_tilt:
        mod_y = math.floor(math.fabs((((current_tilt + 1024) / 2048) * 127)))
        midiControlChange(0, 22, mod_y)
        last_tilt = current_tilt
    sleep(50)
