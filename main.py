import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json

json_open = open('key.json', 'r')
json_load = json.load(json_open)

subscription_key = json_load['section1']['key']
assert subscription_key
face_api_url = json_load['section1']['endpoint']


st.title('顔認識アプリ')

st.image('https://github.com/OHMORIYUSUKE/sinnkeisuizyaku/blob/main/sample.jpeg?raw=true',width=700)

"""
## 機能
- 顔を緑に囲います。
- 年齢・性別を判定します。
### 注意事項
- JPEGのみ対応です。(撮影方法によっては判定できない場合があります。)
- 人間以外(キャラクターなど)は判定できません。
- 次の写真をアップロードする際は一度画像をBrowse filesボタンの下の×をクリックし画像を削除してから行ってください。
"""

uploaded_file = st.file_uploader("画像をアップロードしてください。")

if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output,format="JPEG")
        binary_img = output.getvalue()
    
    headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    results = res.json()

    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill = None,outline='green',width=5)
        
        attribute = result['faceAttributes']
        age = attribute['age']
        gender = attribute['gender']
        
        age = int(age)
        age = str(age)
        
        fontsize = rect['width']/4
        fontsize = int(fontsize)

        font = ImageFont.truetype("arial.ttf", fontsize)
        draw.text((rect['left'],rect['top']-fontsize),age+' , '+gender,fill="green",font=font)
        
    st.image(img , caption='判定結果', use_column_width=True)

