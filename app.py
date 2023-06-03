from flask import Flask, render_template, request, flash, redirect, jsonify
from werkzeug.utils import secure_filename
import os
import glob
import os
import joblib
import librosa
import numpy as np
import pandas as pd
import scipy
import scipy.signal
import uuid
from difflib import SequenceMatcher

import speech_recognition as sr



def latest_wav():
    # * means all if need specific format then *.csv
    list_of_files = glob.glob('./wav_files/*.wav')
    path_latest_wav = max(list_of_files, key=os.path.getctime)

    return path_latest_wav

# Initialize recognizer class                                       
r = sr.Recognizer()



def generate_dataset(audio, sr=22050):
    # generate Mel spectrogram
    spec = librosa.feature.melspectrogram(audio, sr=sr)

    # generate DataFrame from spectrogram (columns: frequencies, rows: analysis frames)
    X = pd.DataFrame(np.transpose(spec))
    return X


def remove_silence(signal):
    # extract non-silent intervals from the voice signal
    voice_intervals = librosa.effects.split(
        signal, frame_length=2048, top_db=35, hop_length=512)
    voice_no_silence = np.array([])
    slices = [signal[interval[0]:interval[1]] for interval in voice_intervals]
    voice_no_silence = np.concatenate(slices)
    return voice_no_silence


def pass_band_filter(sound, sr_sound=22050):
    # design a filter to remove the background noise using scipy.signal.iirfilter
    b, a = scipy.signal.iirfilter(
        1, [128, 2048], btype="bandpass", fs=sr_sound)

    # apply the filter using scipy.signal.lfilter
    y_sound_filt = scipy.signal.filtfilt(b, a, sound)
    return y_sound_filt


def pretraitment(sound):
    sound_filtered = pass_band_filter(sound)
    sound_no_silence = remove_silence(sound_filtered)
    return sound_no_silence


UPLOAD_FOLDER = './wav_files'

app = Flask(__name__, template_folder='template')
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def webpage():
    return render_template('index.html')


modele = joblib.load("rf_model.joblib")


@app.route('/predict', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        audio, _ = librosa.load(latest_wav())
        
        srAudio = sr.AudioFile(latest_wav())
       
        #read audio object and transcribe
        with srAudio as source:
            srAudio = r.record(source)                 
            result = r.recognize_google(srAudio, language="fr-FR")
        print(result)
        
        if (SequenceMatcher(None, 'sésame ouvre-toi', result).ratio() >= 0.7):
            X_eval = generate_dataset(pretraitment(audio), 22050)

            predictions = modele.predict(X_eval)
            eval_unique_labels, eval_unique_counts = np.unique(
                predictions, return_counts=True)
            pred_finale = eval_unique_labels[np.argmax(eval_unique_counts)]
            print(f"Labels : {eval_unique_labels}")
            print(f"Predictions : {eval_unique_counts}")
            print(f"Prédiction : {pred_finale}")

            if str(pred_finale) == "aissa":
                return render_template('aissa.html')
            elif str(pred_finale) == "marouan":
                return render_template('marouan.html')
            else:
                return render_template('another.html')
        else:
            return render_template('wrong_pass.html')

        # # generate the "nutcracker" input data (ignore label series)
        # X_eval = generate_dataset(pretraitment(audio), 22050)
        # # generate dataset from the audio signal, the samplerate and the label

        # predictions = modele.predict(X_eval)
        # eval_unique_labels, eval_unique_counts = np.unique(
        #     predictions, return_counts=True)
        # pred_finale = eval_unique_labels[np.argmax(eval_unique_counts)]
        # if str(pred_finale) == "aissa":
        #     return render_template('aissa.html')
        # if str(pred_finale) == "marouan":
        #     return render_template('marouan.html')
        # else:
        #     return render_template('another.html')


# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     pred_finale = ""
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         file_name = str(uuid.uuid4()) + ".wav"
#         full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
#         file.save(full_file_name)

#         print(f"Filename : {full_file_name}")

#         audio, _ = librosa.load(full_file_name)
        
#         # Initialize recognizer class                                       
#         r = sr.Recognizer()
       
#         srAudio = sr.AudioFile(full_file_name)
#         print(type(srAudio))
#         #read audio object and transcribe
#         with srAudio as source:
#             print("before record")
#             srAudio = r.record(source) 
#             print("after record")                 
#             result = r.recognize_google(srAudio, language="fr-FR")
#             print("after recognized")
       
#         if (result in ["sésame ouvre-toi", "sésame ouvre toi", "sezame ouvre-toi"]):
#             X_eval = generate_dataset(pretraitment(audio), 22050)

#             predictions = modele.predict(X_eval)
#             eval_unique_labels, eval_unique_counts = np.unique(
#                 predictions, return_counts=True)
#             pred_finale = eval_unique_labels[np.argmax(eval_unique_counts)]
#             print(f"Labels : {eval_unique_labels}")
#             print(f"Predictions : {eval_unique_counts}")
#             print(f"Prédiction : {pred_finale}")

#             if str(pred_finale) == "aissa":
#                 return render_template('aissa.html')
#             elif str(pred_finale) == "marouan":
#                 return render_template('marouan.html')
#             else:
#                 return render_template('another.html')
#         else:
#             return render_template('wrong_pass.html')


if __name__ == '__main__':
    app.run()
