from flask import Flask, render_template, Response
import Script as sc


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


#@app.route('/video_feed', endpoint='video_feed')
# def TomarFoto():
#     return Response(sc.ImagenCorreo(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed', methods=['POST'], endpoint='video_feed')
def TomarFoto():
    sc.ImagenCorreo()  # Call your function to take a photo and send an email
    return "Respuesta", 200


if __name__ == '__main__':
    app.run(debug=True)



