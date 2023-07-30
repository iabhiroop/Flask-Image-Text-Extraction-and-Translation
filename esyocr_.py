# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 23:23:14 2023

@author: Abhiroop
"""

import easyocr
import translators.server as tss
from flask import Flask, render_template, Response, request
import os
import cv2

tnl=['en','en']
app = Flask(__name__)
path = os.getcwd()
image = None

lng = {'Afrikaans': 'af', 'Albanian': 'sq', 'Arabic': 'ar', 'Armenian': 'hy', 'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Chinese': 'zh-cn', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hebrew': 'he', 'Hindi': 'hi', 'Hungarian': 'hu', 'Icelandic': 'is', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Kannada': 'kn', 'Kazakh': 'kz', 'Khmer': 'km', 'Korean': 'ko', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Macedonian': 'mk', 'Malay': 'ms', 'Maltese': 'mt', 'Marathi': 'mr', 'Mongolian': 'mn', 'Nepali': 'ne', 'Norwegian': 'no', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Romanian': 'ro', 'Russian': 'ru', 'Serbian': 'sr', 'Slovak': 'sk', 'Slovenian': 'sl', 'Spanish': 'es', 'Swahili': 'sw', 'Swedish': 'sv', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Yiddish': 'yi'}

# def resu(file):
#     global data
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(file)
#     if len(result)<1:
#         result= ["No data found"]
#     data = [i[1] for i in result]
#     return data

def ocr(val):
    # print(image)
    print(tnl)
    reader = easyocr.Reader([tnl[0]])
    result = reader.readtext(image)

    # if len(result)<1:
    #     result= ["No data found"]
    # data = [i[1] for i in result]

    txt=[]
    for bbox, text, prob in result:
        # Get the coordinates of the bounding box
        xmin, ymin = [int(coord) for coord in bbox[0]]
        xmax, ymax = [int(coord) for coord in bbox[2]]
        # print(text)
        # Draw the bounding box and the text on the image
        if val==0:
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
            cv2.putText(image, text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            txt.append(text)
        else:
            text = tss.google(text, tnl[0],tnl[1])
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
            cv2.putText(image, text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (2, 255, 100), 1)
            txt.append(text)
    return txt

def image_process(image):
    ret, jpeg = cv2.imencode('.jpg', image)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/image_filters/img_share')
def img_share():
    global image
    # image=cv2.resize(image, (480, 480))
    return Response(image_process(image), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/trans/', methods=['POST'])
# def trans():
#     if request.method == "POST":
#         value = request.form.get("value")
#         if value!=tnl[1]:
#             tnl[1]=value
#             for i in range(len(data)):
#                 data[i]=tss.google(data[i], tnl[0], tnl[1])
#     return render_template('result.html',data=data)


@app.route('/')
def home():
    return render_template('image.html',lng=lng.keys())

# @app.route('/upload', methods=['POST'])
# def drop_image():
#     if request.method == 'POST':
#         file = request.files['image']
#         path = file.filename
#         # print(1)
#         file.save(path)
#         data = ocr(0)
#         return render_template('result.html',data=data)
    
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

    
@app.route('/image_upload/',methods=['POST','GET'])
def img_():
    global image
    if request.method == 'POST':
        dropdown_value1 = request.form.get("from")
        dropdown_value2 = request.form.get("to")

        tnl[0]=lng[dropdown_value1]
        tnl[1]=lng[dropdown_value2]
        
        if tnl[1] != tnl[0]:
            flag = 1

        f = request.files['image']
        path = f.filename
        f.save(path)
        image = cv2.imread(path)
        data=ocr(flag)
        return render_template('result.html',data=data)


if __name__ == '__main__':
   app.run(debug=True)
