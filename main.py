from flask import Flask, request, render_template
from gtts import gTTS
from playsound import playsound
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        text = request.form['text']
        speak(text)
    return render_template('main.html')

def speak(text):
    filename = os.path.join('generated', str(uuid.uuid4()) + '.mp3')
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)
    playsound(filename)
    os.remove(filename)
    print('yo')

if __name__ == '__main__':
  app.run()
