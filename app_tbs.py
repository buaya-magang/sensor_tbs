from flask import Flask, render_template, request, redirect
from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model yang telah disimpan
model_path = '3_TA 80_2050V2AdamXAugmentasi.h5'
model = load_model(model_path)



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/classification')
def classification():
    return render_template('classification.html')

# Route untuk upload gambar dan prediksi
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
    # Load dan preprocess gambar
    img = load_img(image_path, target_size=(224, 224)) 
    img_array = img_to_array(img)  
    img_array = img_array / 255.0  
    img_array = np.expand_dims(img_array, axis=0)
    # Lakukan prediksi
    predictions = model.predict(img_array)
    predicted_class = (predictions > 0.5).astype("int32") 
    class_labels = ['MATANG', 'MENTAH']  
    predicted_label = class_labels[predicted_class[0][0]]

    return predicted_label

if __name__ == '__main__':
    app.run(debug=True)