from flask import Flask, request, render_template, redirect
from gtts import gTTS
from pydub import AudioSegment
from functools import reduce
import os
import subprocess
import uuid
import time
import math
import configparser
import serial

config = configparser.ConfigParser()
config['default'] = {
        'SEGMENT_LENGTH': 25, 
        'SMOOTHING': 10,
        'MINIMUM_FLAP': 80,
        'SLOW': 0
}
config.read('config.ini')

SEGMENT_LENGTH = int(config['default']['SEGMENT_LENGTH'])
SMOOTHING = int(config['default']['SMOOTHING'])
MINIMUM_FLAP = int(config['default']['MINIMUM_FLAP'])
SLOW = bool(int(config['default']['SLOW']))
print(MINIMUM_FLAP)

ser = serial.Serial('/dev/ttyUSB0', 9600)

app = Flask(__name__)


def ascending(ls):
    result = True
    for i in range(len(ls) - 1):
        result = result and ls[i] < ls[i + 1]
    return result

def descending(ls):
    result = True
    for i in range(len(ls) - 1):
        result = result and ls[i] > ls[i + 1]
    return result

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        text = request.form['text']
        commands = request.form['commands']
        accent = request.form['Type of food']
        if text:
            speak(text, accent)
        if commands:
            issue_commands(commands)
    return render_template('main.html')

def speak(text, accent):
    basename = str(uuid.uuid4()) + '.mp3'
    filename = 'generated/' + basename
    tts = gTTS(text=text, lang=accent, slow=SLOW)
    tts.save(filename)

    sound = AudioSegment.from_mp3(filename)
    times = []
    prev_dBFS = [0] * (SMOOTHING + 2)
    for i in range(len(sound) // SEGMENT_LENGTH):
        segment = sound[i * SEGMENT_LENGTH : (i + 1) * SEGMENT_LENGTH]
        dBFS = segment.dBFS
        prev_dBFS.append(dBFS)
        first = sum(prev_dBFS[:-2]) / SMOOTHING
        middle = sum(prev_dBFS[1:-1]) / SMOOTHING
        last = sum(prev_dBFS[2:]) / SMOOTHING
        if ((first < middle and middle > last)
            or (first > middle and middle < last)):
            times.append((i - int(SMOOTHING / 2)) * SEGMENT_LENGTH)
        prev_dBFS.pop(0)

    if len(times) / 2 != len(times) // 2:
        times.append(SEGMENT_LENGTH * (len(sound) // SEGMENT_LENGTH + 1))
    print(times)
    print('syllables', len(times) / 2)

    durations = [times[0]]
    for i in range(len(times) - 1):
        durations.append(times[i + 1] - times[i])

    print('durations before', *durations)
    while True:
        for i, d in enumerate(durations):
            j = i // 2
            if d < MINIMUM_FLAP:
                if j != 0:
                    durations[2 * (j - 1)] += durations[2 * j] + durations[2 * j + 1]
                else:
                    durations[2] += durations[0] + durations[1]
                durations.pop(2 * j)
                durations.pop(2 * j)
                break
        else:
            break
    
    durations = list(map(str, durations))
    print('durations', *durations)
    p = subprocess.Popen(['python3', 'test-servo2.py'] + durations)
    subprocess.run(['ffplay', '-nodisp', '-autoexit', filename])
    os.remove(filename)

def issue_commands(commands):
    pass

if __name__ == '__main__':
  app.run(host='0.0.0.0')
