# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 23:23:14 2023

@author: Abhiroop
"""

import easyocr
import translators.server as tss
from flask import Flask, render_template, Response, request

tnl=['en','en']
app = Flask(__name__)
data=None

def resu(file):
    global data
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file)
    if len(result)<1:
        result= ["No data found"]
    data = [i[1] for i in result]
    return data

@app.route('/trans/', methods=['POST'])
def trans():
    if request.method == "POST":
        value = request.form.get("value")
        if value!=tnl[1]:
            tnl[1]=value
            for i in range(len(data)):
                data[i]=tss.google(data[i], tnl[0], tnl[1])
    return render_template('result.html',data=data)

@app.route('/')
def home():
    return render_template('image.html')

@app.route('/drop-image/', methods=['POST'])
def drop_image():
    if request.method == 'POST':
        file = request.files['file']
        path = file.filename
        file.save(path)
        data=resu(path)
        return render_template('result.html',data=data)
    
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/val/',methods=['POST','GET'])
def val():    
    if request.method == "POST":
        dropdown_value = request.form.get("dropdown_value")
        tln[0]=dropdown_value
        return render_template('image.html')
    
@app.route('/image_upload/',methods=['POST','GET'])
def img_():
    global data
    if request.method == 'POST':
        f = request.files['image']
        path = f.filename
        f.save(path)
        data=resu(path)
        return render_template('result.html',data=data)


if __name__ == '__main__':
   app.run()
