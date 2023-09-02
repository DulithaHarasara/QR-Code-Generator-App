from flask import Flask,render_template,request
from io import BytesIO
from base64 import b64encode
import qrcode

app = Flask(__name__)

@app.route('/')
def index():
    memory = BytesIO()
    return render_template('index.html')

@app.route('/QR')
def qr(data):
     return render_template('QR.html')

@app.route('/',methods = ['POST'])
def QR():
            data = request.form.get('data')
            bgcolor = request.form.get('bgcolor')
            color = request.form.get('color')
            fillcolor = request.form.get('fillcolor')
            version = request.form.get('version')
            border = request.form.get('border')

            if border is None or border == "":
                border = 1 
            else:
                try:
                    border = int(border)
                except ValueError:
                    border = 1 

            memory = BytesIO()

            qr = qrcode.QRCode(
                    version= version,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border= border,
                )
            
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color= fillcolor, back_color= bgcolor)
            img.save(memory)
            memory.seek(0)

            base64_image = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')

            return render_template('index.html',data = base64_image,fileName = data)


if __name__ == '__main__':
    app.run(debug=True)