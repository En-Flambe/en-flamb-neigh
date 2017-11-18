from flask import Flask, request, render_template
from gtts import gTTS
from pydub import AudioSegment
from functools import reduce
import os
import subprocess
import uuid
import time
import math

SEGMENT_LENGTH = 25
SMOOTHING = 10
MINIMUM_FLAP = 100
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
        if text:
            speak(text)
    return render_template('main.html')

def speak(text):
    basename = str(uuid.uuid4()) + '.mp3'
    filename = 'generated/' + basename
    tts = gTTS(text=text, lang='en', slow=False)
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
        times.append(len(sound))
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

if __name__ == '__main__':
  app.run(host='0.0.0.0')
