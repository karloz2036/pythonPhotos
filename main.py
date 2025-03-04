from flask import Flask, render_template, request
import Script as sc
import base64
import cv2
import numpy as np
import logger as lg

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed', methods=['POST'], endpoint='video_feed')
def TomarFoto():

    try:
        print("creando imagen")
        lg.escribirLog("creando imagen")
        data = request.json['image']
        # Decode the base64 image data
        image_data = base64.b64decode(data.split(',')[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # Call your function to process the image
        sc.ImagenCorreo(img)
        return "Respuesta", 200
    except Exception as e:
        print("error:" + e)
        lg.escribirLogError("error:" + e)

if __name__ == '__main__':
    app.run(debug=True)