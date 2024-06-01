import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import cv2
import time
import requests
from threading import Thread
app = Flask(__name__)

# @app.route('/upload')
# # def home():
# #    return 'This is Home!'
# def upload_file():
#    return render_template('upload.html')

# @app.route('/uploader',methods=['GET','POST'])
# def uploader_file():
#    if request.method=='POST':
#       f=request.files['file']
#       f.save(secure_filename(f.filename)) #저장
#       return '파일 업로드 성공'

# if __name__ == '__main__':  
#    app.run(debug=True)


# def capture_and_upload_image():
#     while True:
#         # 웹캠 시작
#         cam = cv2.VideoCapture(0)
#         ret, frame = cam.read()

#         if not ret:
#             print("웹캠에서 이미지를 캡처하는데 실패했습니다.")
#         else:
#             # 이미지 파일로 저장
#             img_name = "capture_{}.png".format(time.strftime("%Y%m%d-%H%M%S"))
#             cv2.imwrite(img_name, frame)
#             print("{} 저장 완료".format(img_name))
#             cam.release()

#             # 이미지 업로드
#             upload_image(img_name)
#         time.sleep(3)

# def upload_image(img_name):
#     url = 'http://localhost:5000/uploader'
#     files = {'file': open(img_name, 'rb')}
#     response = requests.post(url, files=files)
#     if response.status_code == 200:
#         print("파일 업로드 성공")
#     else:
#         print("파일 업로드 실패: ", response.status_code)

# @app.route('/')
# def home():
#     return 'Flask App Running!'

# if __name__ == "__main__":
#     t = Thread(target=capture_and_upload_image)
#     t.start()
#     app.run(debug=True)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 해당 디렉토리가 없다면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def capture_and_upload_image():
    while True:
        # 웹캠 시작
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()

        if not ret:
            print("웹캠에서 이미지를 캡처하는데 실패했습니다.")
        else:
            # 이미지 파일로 저장
            img_name = "capture_{}.png".format(time.strftime("%Y%m%d-%H%M%S"))
            cv2.imwrite(img_name, frame)
            print("{} 저장 완료".format(img_name))
            cam.release()

            # 이미지 업로드
            upload_image(img_name)
        time.sleep(3)

def upload_image(img_name):
    url = 'http://localhost:5000/uploader'
    files = {'file': open(img_name, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print("파일 업로드 성공")
    else:
        print("파일 업로드 실패: ", response.status_code)

@app.route('/')
def home():
    return 'Flask App Running!'

@app.route('/uploader', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File successfully uploaded'}), 200

if __name__ == "__main__":
    t = Thread(target=capture_and_upload_image)
    t.start()
    app.run(debug=True)