from flask import Flask, render_template, request, send_from_directory
import Script as sc
import base64
import cv2
import numpy as np
import logger as lg
from datetime import datetime 
import socket
#from browser_history import get_history
import os



app = Flask(__name__)

########################################
#variables globales
#obtiene el nombre del host
hostname = socket.gethostname()
rutaArchivoTxt = ""
########################################

@app.route('/')
def index():
    try:
        now = datetime.now()
        current_time = now.strftime("%H%M%S")

        global rutaArchivoTxt
        rutaArchivoTxt = f"txtFiles/history_{current_time}_{hostname}.txt"

        print("-------inicio index--------", current_time)
        lg.escribirLog("-------inicio index--------")

        #se comenta codigo para obtener historial de navegador
        # outputs = get_history()
        # histories = outputs.histories

        # rutaTxtFiles = os.path.join(os.getcwd(), "txtFiles/")
        # if not os.path.exists(rutaTxtFiles):
        #     os.mkdir(rutaTxtFiles)
        #     print("carpeta creada correctamente")
        # else:
        #     print("la carpeta ya existe")
    
        # print("creando txt")
        # lg.escribirLog("creando txt")
        # with open(rutaArchivoTxt, 'w') as file:
        #     file.write(' probando')
        #     for historie in histories:
        #         file.write(str(historie[0]) + ' --- ' + historie[1] + '\n')
        # print("txt creado")
        # lg.escribirLog("txt creado")

        # print("rutaArchivoTxt1:", rutaArchivoTxt)
        print("-------fin index--------", current_time)

        return render_template('index.html', hostname=hostname)
    except Exception as e:
        print("***error catch index***")
        lg.escribirLogError("error catch index()")
        
        error_message = str(e)
        error_type = type(e).__name__
        import traceback
        traceback_details = traceback.format_exc()
        
        # print(f"Error Type: {error_type}")
        print(f"Error Message: {error_message}")#solo muestra el mensaje de error
        # print(f"Traceback: {traceback_details}")#este mensaje muestra la ruta donde se genero el error y el mensaje de error
        print("-------fin error catch--------")

        return "error catch", 500
    

@app.route('/video_feed', methods=['POST'], endpoint='video_feed')
def TomarFoto():
    global rutaArchivoTxt
    now = datetime.now()
    current_time = now.strftime("%H%M%S")

    try:
        print("-------inicio TomarFoto--------", current_time)
        print("creando imagen")
        lg.escribirLog("creando imagen")
        
        #aqui viene todo el objeto json que se mandas desde el html
        #print("request: ",request.json);
        
        data = request.json['sendImage']
        # Decode the base64 image data
        image_data = base64.b64decode(data.split(',')[1])

        #print("image_data:",image_data);
        print("image_data len:",len(image_data));
        
        np_arr = np.frombuffer(image_data, np.uint8)
        #print("np_arr:",len(np_arr));
        if len(np_arr) == 0:
            raise ValueError("Empty buffer")
        

        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # Call your function to process the image
        print("rutaArchivoTxt2:", rutaArchivoTxt)
        response = sc.ImagenCorreo(img, rutaArchivoTxt)
        print("-------fin TomarFoto--------", current_time)
        return response, 200 
    except Exception as e:
        print("***error catch tomar foto***")
        lg.escribirLogError("error catch tomar foto")
        
        error_message = str(e)
        error_type = type(e).__name__
        import traceback
        traceback_details = traceback.format_exc()
        
        # print(f"Error Type: {error_type}")
        #print(f"Error Message: {error_message}")#solo muestra el mensaje de error
        # print(f"Traceback: {traceback_details}")#este mensaje muestra la ruta donde se genero el error y el mensaje de error
        #print("-------fin error catch tomar foto--------")

        #return "error catch tomar foto: " + traceback_details, 500
        return "error catch tomar foto: " + error_message, 500


'''
The purpose of the serve_image function is to create a route in your Flask application that serves files from the imgs directory. This allows you to access images stored in that directory via a URL.
Here's how it works:
Route Definition: The route /imgs/<path:filename> is defined to handle requests for any file within the imgs directory. The <path:filename> part is a placeholder for the actual file name you want to serve.
Serving the File: The send_from_directory function is used to serve the requested file from the imgs directory.
Using the Route in HTML: You use this route in your HTML file to display the image.
'''
@app.route('/imgs/<path:filename>')
def serve_image(filename):
    return send_from_directory('imgs', filename)

if __name__ == '__main__':
    app.run(debug=True)