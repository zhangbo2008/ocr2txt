# 安装:  pip install  flask flask_cors tencentcloud-sdk-python -i https://pypi.tuna.tsinghua.edu.cn/simple
# 
# 
# pip install opencv-python matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple

# sql语句:SELECT * FROM "med" where data like '%CTR20211512%'

# 大模型方案: 1. kimi+pdf  2. ocr之后txt+豆包大模型


# 2024-07-08,15点17d   算法最终的服务: nohup ~/miniconda3/bin/python  backend最强.py  &

import sqlite3
# import cv2
import os
import io
import json
# import fitz  
from io import BytesIO  
import os
print(os.cpu_count(), 'cpushuliaing')


from PIL import Image
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # 解决跨域问题

from ocr_tools2 import ocr_my2

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException


basedir = os.path.abspath(os.path.dirname(__file__))  # 定义一个根目录 用于保存图片用
UPLOAD_ROOT_PATH = 'pic_data'
# http://172.27.118.204:5050


# ==============初始化数据.

# con = sqlite3.connect("Test.db", check_same_thread=False)
# cur = con.cursor()


# meddata = [eval(i[1]) for i in cur.execute("select * from med").fetchall()]

# userdata = [eval(i[1]) for i in cur.execute("select * from user").fetchall()]
# print("请分析下面的医药信息和患者信息是否匹配, 给出分析结果和原因")
# print('========================医药===========================')
# print(meddata[0])
# print('========================用户===========================')
# print(userdata[0])
# pass














import multiprocessing
import time

def worker(a,b):
    png_data=a
    metainfo=b
    ttt = ocr_my2(BytesIO(png_data),metainfo)
    # print('===================================',ttt)
    
    if isinstance(ttt,TencentCloudSDKException):
        return jsonify(ttt.message)
    return ttt













@app.route('/ocr4', methods=['GET', 'POST'])
def ocrFile1234324212():
    files = request.files.getlist('files')
    import cv2
    files[0].save('tmp.png')
    aaaaa=cv2.imread('tmp.png')
    with open('tmp.png', 'rb') as file:  
                png_data = file.read()
    if 1: # 2024-09-23,20点46 改成并发.
            
        all_jieguo=worker(png_data,aaaaa.shape[:2])

    #===========#===========step0:进行页面融合 2024-09-10,23点00 进行强融合策略.最终所有页变成一页.
    #是否进行网页融合.
    all_jieguo
    #=每一页的头尾删除空白.

    print("==============打印ocr排版之后结果")
    for i in all_jieguo:
        [print(ii) for ii in i]
        print('==========分页')
        
        
        
        
  
    return jsonify(all_jieguo)


if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=5001)


# 前端设计: 左边一个框, 里面可以打开上传一堆图片, 传完之后是缩略图, 打开每一个可以放大缩回, 然后点ocr解析, 右边框就会出现所有信息的结构化, 然后可以修改这些信息,之后点击上传服务器, 出现确认框之后我们数据会上传. 如果服务器已经有这个数据, 那么提示是否进行覆盖. 如果重名了提示后面加一个数
# 字,(加的数字是重复率加1) 或者不加数字就会覆盖之前数据.
