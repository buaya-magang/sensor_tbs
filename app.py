from flask import Flask, render_template, request, redirect, send_from_directory
from dotenv import load_dotenv
import os
import numpy as np
import gdown
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# === Konfigurasi model ===
model_filename = '3_TA_80_2050V2AdamXAugmentasi.h5'
drive_file_id = '1fHFnj8takqOYY8O73WaCKDujCLvMWpyq'
model_path = os.path.join(".", model_filename)

# === Download model dari Google Drive jika belum ada ===
if not os.path.exists(model_path):
    print("Model tidak ditemukan. Mengunduh dari Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={drive_file_id}", model_path, quiet=False)
else:
    print("Model ditemukan.")

# === Load model ===
model = load_model(model_path)
print("Model berhasil load.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/classification')
def classification():
    return render_template('classification.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hasil', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    prediction = load_model_and_predict(file_path)
    return render_template('result.html', image_url=file_path, prediction=prediction)

def load_model_and_predict(image_path):
    img = load_img(image_path, target_size=(224, 224)) 
    img_array = img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = (predictions > 0.5).astype("int32")
    class_labels = ['MATANG', 'MENTAH']
    predicted_label = class_labels[predicted_class[0][0]]
    return predicted_label

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
