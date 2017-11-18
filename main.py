from flask import Flask, request, render_template
from gtts import gTTS
import os
import subprocess
import uuid
import time

app = Flask(__name__)

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
    #filename = os.path.join('generated', basename)
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)

    subprocess.Popen('bash -c \'mpg123 {f}; rm {f}\''.format(f=filename))

if __name__ == '__main__':
  app.run()
