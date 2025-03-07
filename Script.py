import numpy as np
import cv2, time
import os
from datetime import datetime
import logger as lg

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText  
import shutil


def ImagenCorreo(foto, ip):
    print("ejecutando...")
    now = datetime.now()
    current_time = now.strftime("%H%M")

    VideoArray=[]
    VideoArray.append(foto)    

    if len(VideoArray) > 0:
        # Reshape the array to 2D if necessary
        array_reshaped = VideoArray[0].reshape(-1, VideoArray[0].shape[-1])

        #IF THE FILE EXISTS, IT IS DELETED
        file_path = 'arrayFile.txt'
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Archivo eliminado")
            lg.escribirLog("Archivo eliminado:" + current_time)

        # Save the array to a text file
        np.savetxt(file_path, array_reshaped, fmt='%d')
        print("Archivo creado")
        lg.escribirLog("Archivo creado:" + current_time)

        # Load the array back from the text file (optional)
        #loaded_array = np.loadtxt('arrayFile.txt', dtype=np.uint8).reshape(VideoArray[0].shape)
    else:
        print("Array Vacio")
        lg.escribirLogError("Array Vacio:"+ current_time)


    #CREATE THE IMAGE FROM ARRAY FILE
    #print("Numero de imagenes:",len(VideoArray))
    rutaNvaImg = os.path.join(os.getcwd(), "imgs\\nuevaImg.jpg")
    #print(len(VideoArray))
    for i, fr in enumerate(VideoArray):
        #print(f"Frame {i} type: {type(fr)}")
        #cv2.imshow("img", fr)#esta imagen es solo para mostrarla, pero cuando de despliega en un servidor no es necesaria ya que marca error
        cv2.imwrite(rutaNvaImg, fr)#solo es necesario guardarla para despues mostrarla
        #key=cv2.waitKey(2000)#no aplica en el servidor
    #cv2.destroyAllWindows()#no aplica en el servidor

    try:
        # Email details
        sender_email = 'karloz2036cursos@gmail.com'
        receiver_email = 'karloz2036@gmail.com'
        subject = 'Correo Python ' + ip + " " + current_time
        body = "FYI"
        password = 'plbw wdeq bspj kpqg'

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        listFilesAttach = ["imgs\\nuevaImg.jpg", 'arrayFile.txt', "txtFiles/JsonLocation.txt"]
        for item in listFilesAttach:
            #Attach the zip file
            filename = item
            attachment = open(filename, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)

        # Send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()

        print("correo enviado")
        lg.escribirLog("correo enviado:"+ current_time)
    
        return "ok"

    except Exception as e:
        print("error al enviar correo: ", e)

        import traceback
        traceback_details = traceback.format_exc()

        error_message = str(e)

        #return "error correo: " + traceback_details
        return "error correo: " + error_message
    

