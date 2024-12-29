# =============矫正图片:还是腾讯的ocr效果好.记得阿里好像也不错.
# 2024-05-22,17点48 暴力方法找表格的分界线.
# -- coding: utf-8 --
import json
import types
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import sys
import cv2
# from txocrtest import aaa2
# from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import math
import re
import numpy as np
import json
maohaodaquan = [':', '：', '∶']

sys.path.append("..")  # 模块父目录下的model文件中

sys.path.append("../..")
sys.path.append(".")
sys.path.append("./")

sys.path.append("..")  # 模块父目录下的model文件中

sys.path.append("../..")
sys.path.append(".")
sys.path.append("./")
# 扫描王矫正过的结果.
# aaaa = cv2.imdecode(np.fromfile('ocr结构化输出/10000.png', dtype=np.uint8), -1)
# 调用腾讯的网页demo返回, 免费试用的.估计每天有次数限制.
# with open('ocr结构化输出/10000.json', encoding='utf-8') as f:  # 调用的高精度腾旭ocr
#     tmp = f.read()
#     tengxunjieguo = json.loads(tmp)
#    #  tengxunjieguo=json.load(f)

def ocr_my(dizhi):
    if 1:
        # 加载新图片的腾讯接口结果.
        # bbb=aaa2('ocr结构化输出/100007.png')  #===========这个图片的信息就是不带冒号的.全凭排版.
        # bbb = aaa2('ocr结构化输出/1000005.png')  # ===========这个图片的信息就是不带冒号的.全凭排版.
        
        
        try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(
                "AKIDVwCKF4kHckgQxY243LZcKrBKNCoIQRGu", "Z1Ibo380fIpDOdmlY7SaWRJ0Um4A3xRr")
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GeneralAccurateOCRRequest()

            import base64
            tmp2=dizhi.read()
            # tmp=bytearray(tmp2)
            if 1:
                # img=cv2.imdecode(np.frombuffer(tmp, dtype=np.uint8),flags=cv2.IMREAD_COLOR)
                encoded_string = base64.b64encode(
                    tmp2).decode("utf-8")

            params = {
                "ImageBase64": encoded_string,

            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个GeneralAccurateOCRResponse的实例，与请求对象对应
            resp = client.GeneralAccurateOCR(req)
            # 输出json格式的字符串回包
            # print(resp.to_json_string())
            bbb= resp.to_json_string()

        except TencentCloudSDKException as err:

            print(err)
            return {}
        
        
        
        
        
        
        
        
        
        # bbb = aaa2(dizhi)  # ===========这个图片的信息就是不带冒号的.全凭排版.

        tengxunjieguo = json.loads(bbb)
        # 把识别的结果可视化,看目标检测的效果.
        # print('原始的腾讯返回结果',bbb)
        # print('==========================================')

    zuobiao = []
    for i in tengxunjieguo['TextDetections']:
        tmp = i['Polygon']
        # print(i['DetectedText'])
        tmp = [
            [tmp[0]['X'], tmp[0]['Y']],
            [tmp[1]['X'], tmp[1]['Y']],
            [tmp[2]['X'], tmp[2]['Y']],
            [tmp[3]['X'], tmp[3]['Y']],


        ]
        zuobiao.append(tmp)

        pass


        # zuobiao = np.array(zuobiao)
        # pass

        # keshihua = aaaa.copy()
        # cv2.polylines(keshihua, zuobiao, isClosed=True,
        #             color=(255, 125, 125), thickness=1)
        # cv2.imwrite('debug4.png', keshihua)


        # # ============识别表格的线. 我们先用传统方法来做.


        # kernel = np.ones((1, 3), np.uint8)

        # img = aaaa.copy()
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # # cv2.imwrite("13里面二值化的图片.png", binary)
        # # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=2)  # 二值化.
        # cv2.imwrite('debug1.png', binary)

    # 可以看到处理后基本的文字方向.
    # 进行直线检测.


    # =========改成用大量的逻辑判断来结构化文档


    ocr_jieguo = tengxunjieguo['TextDetections']

    pass
    # =======字高

    tmp = []
    for i in ocr_jieguo:
        tmp.append(i['ItemPolygon']['Height'])
    tmp.sort()
    tmp = np.array(tmp)
    tmp = np.median(tmp)
    zigao = tmp
    pass


    jieguo1 = {}
    # ====================第一种抽取 xxx:yyy类型.

    import re
    def pandinghefakey(a):
        return not re.fullmatch('[0-9|\s|-]*', a)


    pandinghefakey('2023-04-23 8')
    for fenge in [':', '：', '∶']:
        for i in ocr_jieguo:
            zifu = i['DetectedText']
            if fenge in zifu and zifu.split(fenge) and zifu.split(fenge)[0] and zifu.split(fenge)[1] and pandinghefakey(zifu.split(fenge)[0]):
                if zifu.split(fenge)[1] in jieguo1.values():
                    continue  # 不要value重复录入.

                if zifu.split(fenge)[0] in jieguo1:
                    # 如果之前已经存在了. 那么我们取信息最详细的那个
                    if len(zifu.split(fenge)[1]) > len(jieguo1[zifu.split(fenge)[0]]):
                        jieguo1[zifu.split(fenge)[0]] = zifu.split(fenge)[1]
                    else:
                        pass
                else:

                    jieguo1[zifu.split(fenge)[0]] = zifu.split(fenge)[1]
                pass

    # print('jieguo1', jieguo1)
    pass


    # ==========数据进行行融合!!!!!!
    ocr_jieguo
    # 每一个数据的中心坐标:
    # from tools_for_geo import *
    ocr_jieguo2 = []
    for dex in range(len(ocr_jieguo)):
        i = ocr_jieguo[dex]

        line1 = i['Polygon'][0]['X'], i['Polygon'][0]['Y'], i['Polygon'][2]['X'], i['Polygon'][2]['Y']
        line1with_x_axis = math.atan(
            (-line1[3]+line1[1])/(line1[2]-line1[0]))/math.pi*180 if line1[2] != line1[0] else 90
        # print(line1with_x_axis)
        #  if abs(line1with_x_axis)   >25: # 对于10度都扔了.
        # continue

        i['center_point'] = (i['Polygon'][0]['X']+i['Polygon'][2]
                            ['X'])/2, (i['Polygon'][0]['Y']+i['Polygon'][2]['Y'])/2
        ocr_jieguo2.append(i)
    # 一定还要先按照列排序!!!!!!!!!!否则逻辑不对.
    ocr_jieguo2.sort(key=lambda x: (x['center_point'][1], x['center_point'][0]))
    pass

    alltext = []
    # print('打印腾通ocr原始返回值.')
    for i in ocr_jieguo2:
        # print(i['DetectedText'], i['center_point'][0], i['center_point'][1])
        print()
        print()
        alltext.append(i['DetectedText'])


    # 生成一个包含30个随机整数的数组(1~100)
    data = np.random.randint(1, 101, size=30)
    data = np.array([i['center_point'][1] for i in ocr_jieguo2])

    zigao
    # 应用DBSCAN算法, 进行行分割. 设置好eps:类内最大距离, 和min_sample=1即可.
    # db = DBSCAN(eps=zigao/2+2, min_samples=1)
    # # db = DBSCAN(eps=3, min_samples=1)
    # db.fit(data.reshape(-1,1))
    # # 获取聚类标签
    # labels = db.labels_
    # pass

    # ======dbscan还不是我们想要的行分割函数.
    pass


    # =========对data进行分类,让所有分类的mean互相都大于 11: zigao/2+2
    # =======这个算法,目前有点慢, 可以再改吧以后.
    d = [[i] for i in range(len(data))]
    pass


    def hebing():  # 对d的子数组进行合并.
        nonlocal d
        hebingma = False
        for dex, i in enumerate(d):
            for dex2, j in enumerate(d):
                if j != i and abs(np.mean(data[j])-np.mean(data[i])) < zigao/2+2:
                    hebingma = True

                    d[dex] = i+j
                    # 把j添加到i的后面即可.
                    d.pop(dex2)
                    return hebingma  # 每一次合并,d内元素都修改了.所以每一次函数只合并一次更稳妥.
        return hebingma


    aaa = hebing()
    # print(aaa)
    while hebing():
        pass
    pass


    # ========debug
    print('下面进行文本分行结果的debug')

    # 行拆分的结果. 结果是一个数组, 数组里面每一个元素是一个数组,小数组表示一行的全部识别结果. #先进行排序!!!!!!!!!!!!!!!!!!!!!!
    ocr_hangchaifen = []
    for i in d:
        tmp = []
        for i1 in i:
            tmp.append(ocr_jieguo2[i1])
        ocr_hangchaifen.append(sorted(tmp, key=lambda x: (x['center_point'][0])))
    ocr_hangchaifen.sort(key=lambda x: np.mean([y['center_point'][1] for y in x]))
    pass


    ocr_hangronghe = []
    for i in ocr_hangchaifen:
        tmp = '  '.join([j['DetectedText'] for j in i])
        ocr_hangronghe.append(tmp)

    pass

    print('解析后打印每行')
    print('===============================')
    for i in ocr_hangronghe:
        # print(i)
        print('===============================')


    # yolo 做一个语义分割的模型. 把整个图片切割几个部分. 比如第一个部分标记为 文本的框, 第二个为表格啥的.........做这个目标检测.如果做好这个,那么文本的框里面找第一个:前面的文字就是key, 后面的文字就是value, 表格按照第一行的列名分割下面的数据即可.

    # 版面分析: https://blog.csdn.net/weixin_43424450/article/details/135596393
    # https://blog.csdn.net/mddCSDN/article/details/132459685


    # 使用nlp的方法.数据全部拉成一个字符串, 然后nlp方法语义分类抽出里面的key, key中间夹着的部分就是value了.


    # 如果我们的key value都是一个确定的集合. 比如一个几万字符串的数组来存. 那么每次进行key value匹配即可了. 比如血液化验的这些xxx酶,啥的.做一个表.然后我们找到这个字之后直接返回他右边的数字即可.

    # ========安装上腾讯接口:
    # pip install  tencentcloud-sdk-python


    # ==============
    # 下面写的是一行信息的处理逻辑.############################################################################################
    print('step 1:抽取不会换行的基本信息')


    keys_candidate = [
        '姓名',
        '性别',
        '科室',
        '科别',
        '年龄',
        # '诊断',
        '体重',
        '就诊状态',
        '就诊科室',
        '就诊日期',
        '电话',
        '出生地',
        '籍贯',
        '民族',
        '电话',
        '证件号',
        '现住地',
        '户口地址',
        '身份证件类别',
        '国籍',
        '职业',
        '入院记录',
        '出院记录',
    ]
    # =去重
    keys_candidate2 = []
    [keys_candidate2.append(i) for i in keys_candidate if i not in keys_candidate2]
    keys_candidate = keys_candidate2
    # ==========直接字符串,跟上面的行信息强匹配即可.
    out = {}
    for mubiaokey in keys_candidate:
        for i in ocr_hangronghe:
            # print(i)
            tmp = i.split('\t')  # 单独的.
            for dex, j in enumerate(tmp):
                # ======删除冒号:
                j = j.replace(':', '').replace('：', '').replace('∶', '')

                if mubiaokey in j and j[:len(mubiaokey)] == mubiaokey:  # 在ocr小块里面
                    qita = j[j.index(mubiaokey)+len(mubiaokey):]  # 找到后面其他部分.
                    # 其他部分是不是数字.
                    if re.fullmatch('\d', qita):  # 后面只带一个数字
                        if dex+1 < len(tmp):
                            xijie = tmp[dex+1]
                            xijie2 = xijie.replace('1', '**1').replace('2', '**2').replace('3', '**3').replace('4', '**4').replace(
                                '5', '**5').replace('6', '**6').replace('7', '**7').replace('8', '**8').replace('9', '**9').split('**')
                            if xijie2:
                                xijie2 = [i for i in xijie2 if qita in i]
                                if xijie2:
                                    out[mubiaokey] = re.sub('\d\.', '', xijie2[0])

                            pass  #
                        else:
                            out[mubiaokey] = qita
                        continue
                    elif qita:
                        out[mubiaokey] = qita
                    else:
                        if dex+1 < len(tmp):
                            out[mubiaokey] = tmp[dex+1]

                        pass
    print('抽取的基本信息', out)

    pass


    # 一行信息的处理逻辑. over############################################################################################
    # =====我期望: key 严格匹配的. 不用现在的包含关系. key写的很全, 比如: 血小板, *血小板 . 都看做两个.


    # ===================
    print('下面进行多行信息的抽取')

    # ============

    # 2024-05-27,13点42
    # 业务员:  1. 先看病例.  2. 看化验单
    # 三大模块: 1.ocr 2. 药物 3. 匹配:
    # 1.ocr: 多行:
    #       1.cv方法: 目标检测. 标记:整个key value box, 然后第一个冒号之前的部分我们作为key,其他作为value
    # yolo: 2000个一类
    #       2. nlp 方法: 整个当一个字符串, 让nlp做分隔.(大模型)
    #       3. 正则


    # 3.匹配:
    #                                      字符串包含:  六个月  !=  半年.
    #                                      bert:句向量.(小模型)
    #                                      大量nlp算法.(太过复杂, 推荐是使用大模型或者医疗垂直领域大模型)


    # 前后端. 人工校验之后,再入数据库.


    # =========解析段落.
    ocr_hangchaifen
    # 求每一行的长度.
    hangchangdu = []
    for i in ocr_hangchaifen:
        if len(i) == 1:
            chang = i[0]['ItemPolygon']['Width']
            pass
        else:
            chang = i[-1]['ItemPolygon']['X'] - \
                i[0]['ItemPolygon']['X']+i[-1]['ItemPolygon']['Width']
        hangchangdu.append(chang)
    pass

    changdu2 = sorted(hangchangdu)


    zifuchangdu = []
    for i in ocr_hangchaifen:
        chang = sum([j['ItemPolygon']['Width'] for j in i])
        zifuchangdu.append(chang)
    pass

    zifumidu = []
    for i in range(len(zifuchangdu)):
        zifumidu.append(hangchangdu[i]/zifuchangdu[i])

    # 大于0.8的最长那个最为最长的行.
    hangchangdu = np.array(hangchangdu)
    zifumidu = np.array(zifumidu)
    zifuchangdu = np.array(zifuchangdu)


    if len(hangchangdu[zifumidu > 0.8]) > 0:
        zuichanghang = sorted(hangchangdu[zifumidu > 0.8])[-1]
    else:
        zuichanghang = sorted(hangchangdu)[-1]
    pass


    juzizuihoudexzuobiao = []

    for i in ocr_hangchaifen:
        zuihoux = i[-1]['ItemPolygon']['X']+i[-1]['ItemPolygon']['Width']
        juzizuihoudexzuobiao.append(zuihoux)
    pass

    juzizuihoudexzuobiao = np.array(juzizuihoudexzuobiao)
    if len(juzizuihoudexzuobiao[zifumidu > 0.8]) > 0:
        zuiyouduan = sorted(juzizuihoudexzuobiao[zifumidu > 0.8])[-1]
    else:
        zuiyouduan = sorted(juzizuihoudexzuobiao)[-1]
    pass


    # 大于zuiyouduan*0.85的行我们才认为是一个整行.

    #============开始抽取!!!!!!!!!!!!!!!
    # 多行, 必须作为开头的写这里.
    duohangkaitou = [
        '主诉',
        '现病史',
        '既往史',
        '个人史',
        '婚育史',
        '主要诊断',
        '其他诊断',
        '出院医嘱',
        '入院诊断',
        '出院诊断',
        '治疗经过简介',
        '出院时情况',
        '体格检查',
        '处方',
        '药物过敏史',
        '诊断',
        '辅助检验',
        '医嘱、处置',
        '医嘱',
        '治疗经过',
        '西医诊断',
        '病理诊断'









    ]
    
    duohangkaitou=[i+':' for i in duohangkaitou]
    
    

    #==============多行包含就算的写这里.
    duohangzhongjian=['查房记录',
                      '病程记录',
                      '病房记录',
                      '疾病记录'


    ]



    duohangkaitou2 = []
    for i in duohangkaitou:
        if i not in duohangkaitou2:
            duohangkaitou2.append(i)
    duohangkaitou = duohangkaitou2


    def pandinghangshifuohangkaitou(a): # 2024-06-25,13点03 添加多行判断. 返回找到key的长度.
        for i in duohangkaitou:
            if a[:len(i)] == i:
                return len(i)
        for i in duohangzhongjian:
            if i in a:
                return a.index(i)+len(i)


        return False


    def pandingshiyigechangju(i):
        return True
        return i[-1]['ItemPolygon']['X']+i[-1]['ItemPolygon']['Width'] > zuiyouduan*0.85


    ocrhangtext = ocr_hangronghe
    # ======直接抽取多行.
    tmp = ''

    changjuduanju = []
    for i in ocr_hangchaifen:
        changjuduanju.append(pandingshiyigechangju(i))

    # =====2024-05-28,13点18 如果一个句子只有我们的duohangkaitou , 那么他也是判定为长句, 可以链接下面的句子.


    for dex, i in enumerate(ocrhangtext):
        panding = pandinghangshifuohangkaitou(i)
        if panding and len(i[panding:]) < 2:  # 后面的垃圾字符小于2 就算无效字符,所以看做长句.
            changjuduanju[dex] = True


    shifoushikaitou = []
    for i in ocrhangtext:
        shifoushikaitou.append(pandinghangshifuohangkaitou(i))


    for dex, i in enumerate(ocrhangtext):

        if shifoushikaitou[dex] and changjuduanju[dex]:
            if tmp:  # 记录旧的
                suoyin = pandinghangshifuohangkaitou(tmp)
                out[tmp[:suoyin]] = tmp[suoyin:]
            tmp = i
        if not shifoushikaitou[dex]:
            if dex == 0:
                continue
            if dex != 0:
                shangyihang = changjuduanju[dex-1]
                if shangyihang:  # 上一行如果是长句子.
                    tmp += i  # 非开头句子只有上一句是长句子时候才能加入段落.
        if shifoushikaitou[dex] and not changjuduanju[dex]:
            if tmp:  # 记录旧的
                suoyin = pandinghangshifuohangkaitou(tmp)
                out[tmp[:suoyin]] = tmp[suoyin:]
            tmp = i
            if tmp:  # 记录当前的
                suoyin = pandinghangshifuohangkaitou(tmp)
                out[tmp[:suoyin]] = tmp[suoyin:]
            tmp = ''
        if dex == len(ocrhangtext)-1:
            # 最后一个:
            if tmp:  # 记录旧的
                suoyin = pandinghangshifuohangkaitou(tmp)
                out[tmp[:suoyin]] = tmp[suoyin:]

        # #判定头部:
        # panding=pandinghangshifuohangkaitou(i)
        # if panding:
        #    if tmp:
        #       suoyin=pandinghangshifuohangkaitou(tmp)
        #       out[tmp[:suoyin]]=tmp[suoyin:]
        #    tmp=i #记录下开头
        # if not(panding)
    # 总结多行的抽取思路: 我们先计算那些行是长的, 长的标准是字的密度大于0.85. 字的密度是ocrbox长度和/收尾box长度
    #                  只有长的我们才允许他拼接到下面一行作为段落.如果不是长的,那么进行抽取即可. 抽取按照句子前几个字属于我们keyword里面即可.

    pass
    out2={}
    for i in out:
        if i:
            out2[i]=out[i]
    out=out2
    print('抽取完多行完毕!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', )
    for i in out:
        print(i+'=============================='+out[i])
        
# 2024-07-16,10点05 ocr添加检测结果识别.
    jiancexiangmu=[
        '谷丙转氨酶',

    '谷草转氨酶',

'谷草/谷丙',  
'谷氨酰转肽酶',
    '碱性磷酸酶',
    '总蛋白'  ,
    '白蛋白',  

    '球蛋白' , 

    '白球比'  ,

    '总胆汁酸',

    '前白蛋白',

    '核苷酸酶',

    '总胆红素',

    '直接胆红素',

    '间接胆红素',

    '甘油三脂',
    '总胆固醇',

       

'低密度脂蛋白',

'载脂蛋白A1',

 '载脂蛋白B' ,
    '脂蛋白(a)',
    '葡萄糖'  ,
    '尿酸'    ,

        
        '尿素',
        '肌酐',
        '肌酐/尿素',
        '微球蛋白',
        '羟丁酸脱氢酶',
        '乳酸脱氢酶',
        '肌酸激酶',
        '肌酸酶同功酶',
        '钾',
        '钠',
        '氯',
        '二氧化碳',
        '阴离子间隙',
        '钙',
        '磷',
        '镁',
        '铁',
        '高密度脂蛋白',
        '转铁蛋白',
        
    ]
    ocrhangtext
    yuanshishuju=[i.split() for i in ocrhangtext]
    #原始数据后处理:
    for i in yuanshishuju:
        for dex in range(len(i)):
            for muban in jiancexiangmu:
                
                if muban in i[dex] and dex<len(i)-1:
                    zifu=i[dex] 
                    shuzi=i[dex+1]
                    if shuzi=='↓' or shuzi=='↑' and dex+2<len(i):
                        i[dex+1]=i[dex+1]+i[dex+2]
                        
    
    
    
    
    
    
    
    for i in yuanshishuju:
        for dex in range(len(i)):
            for muban in jiancexiangmu:
                
                if muban in i[dex] and dex<len(i)-1:
                    zifu=i[dex] 
                    shuzi=i[dex+1]
                    def  pandingshuzi(s):
                        for i in s:
                            if i not  in ['0','1','2','3','4','5','6','7','8','9','0','.','↑','↓']:
                                return False
                        for jjj in out.values():
                            if zifu in jjj:
                                return False
                        return True
                    if pandingshuzi(shuzi):
                        

                        out[zifu]=shuzi
    print('检测')
        
        
    print('抽取检测结果!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    for i in out:
        print(i+'======'+out[i])
        
    import re
    for i in out:
        out[i]=re.sub('CS.*扫描全能王','',out[i])
        out[i]=re.sub('Cs.*扫描全能王','',out[i])
        out[i]=re.sub('cs.*扫描全能王','',out[i])
        out[i]=re.sub('Os.*扫描全能王','',out[i])
        out[i]=re.sub('os.*扫描全能王','',out[i])
        out[i]=re.sub('扫描全能王','',out[i])
        out[i]=re.sub('第\d页','',out[i])
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    return out
        
        
        
        
        
    return out










def ocr_my2(dizhi):
    if 1:
        # 加载新图片的腾讯接口结果.
        # bbb=aaa2('ocr结构化输出/100007.png')  #===========这个图片的信息就是不带冒号的.全凭排版.
        # bbb = aaa2('ocr结构化输出/1000005.png')  # ===========这个图片的信息就是不带冒号的.全凭排版.
        
        
        try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(
                "AKIDgBTXPhlffzUsHj4OXecSBh0VAlO1Wpy0", "2tbBd1EE8sbDi8LB7DFPURTYVN937Pkv")
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GeneralAccurateOCRRequest()

            import base64
            tmp2=dizhi.read()
            # tmp=bytearray(tmp2)
            if 1:
                # img=cv2.imdecode(np.frombuffer(tmp, dtype=np.uint8),flags=cv2.IMREAD_COLOR)
                encoded_string = base64.b64encode(
                    tmp2).decode("utf-8")

            params = {
                "ImageBase64": encoded_string,

            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个GeneralAccurateOCRResponse的实例，与请求对象对应
            resp = client.GeneralAccurateOCR(req)
            # 输出json格式的字符串回包
            # print(resp.to_json_string())
            bbb= resp.to_json_string()

        except TencentCloudSDKException as err:

            print(err)
            return {}
        
        
        
        
        
        
        
        
        
        # bbb = aaa2(dizhi)  # ===========这个图片的信息就是不带冒号的.全凭排版.

        tengxunjieguo = json.loads(bbb)
        # 把识别的结果可视化,看目标检测的效果.
        print('原始的腾讯返回结果',bbb)
        print('==========================================')
        return bbb











def ocr_my2(dizhi):
    if 1:
        # 加载新图片的腾讯接口结果.
        # bbb=aaa2('ocr结构化输出/100007.png')  #===========这个图片的信息就是不带冒号的.全凭排版.
        # bbb = aaa2('ocr结构化输出/1000005.png')  # ===========这个图片的信息就是不带冒号的.全凭排版.
        
        
        try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(
                "AKIDgBTXPhlffzUsHj4OXecSBh0VAlO1Wpy0", "2tbBd1EE8sbDi8LB7DFPURTYVN937Pkv")
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GeneralAccurateOCRRequest()

            import base64
            tmp2=dizhi.read()
            # tmp=bytearray(tmp2)
            if 1:
                # img=cv2.imdecode(np.frombuffer(tmp, dtype=np.uint8),flags=cv2.IMREAD_COLOR)
                encoded_string = base64.b64encode(
                    tmp2).decode("utf-8")

            params = {
                "ImageBase64": encoded_string,

            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个GeneralAccurateOCRResponse的实例，与请求对象对应
            resp = client.GeneralAccurateOCR(req)
            # 输出json格式的字符串回包
            # print(resp.to_json_string())
            bbb= resp.to_json_string()

        except TencentCloudSDKException as err:

            print(err)
            return {}
        
        
        
        
        
        
        
        
        
        # bbb = aaa2(dizhi)  # ===========这个图片的信息就是不带冒号的.全凭排版.

        tengxunjieguo = json.loads(bbb)
        # 把识别的结果可视化,看目标检测的效果.
        print('原始的腾讯返回结果',bbb)
        print('==========================================')

    zuobiao = []
    for i in tengxunjieguo['TextDetections']:
        tmp = i['Polygon']
        # print(i['DetectedText'])
        tmp = [
            [tmp[0]['X'], tmp[0]['Y']],
            [tmp[1]['X'], tmp[1]['Y']],
            [tmp[2]['X'], tmp[2]['Y']],
            [tmp[3]['X'], tmp[3]['Y']],


        ]
        zuobiao.append(tmp)

        pass


        # zuobiao = np.array(zuobiao)
        # pass

        # keshihua = aaaa.copy()
        # cv2.polylines(keshihua, zuobiao, isClosed=True,
        #             color=(255, 125, 125), thickness=1)
        # cv2.imwrite('debug4.png', keshihua)


        # # ============识别表格的线. 我们先用传统方法来做.


        # kernel = np.ones((1, 3), np.uint8)

        # img = aaaa.copy()
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # # cv2.imwrite("13里面二值化的图片.png", binary)
        # # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=2)  # 二值化.
        # cv2.imwrite('debug1.png', binary)

    # 可以看到处理后基本的文字方向.
    # 进行直线检测.


    # =========改成用大量的逻辑判断来结构化文档


    ocr_jieguo = tengxunjieguo['TextDetections']

    pass
    # =======字高

    tmp = []
    for i in ocr_jieguo:
        tmp.append(i['ItemPolygon']['Height'])
    tmp.sort()
    tmp = np.array(tmp)
    tmp = np.median(tmp)
    zigao = tmp
    pass


    jieguo1 = {}
    # ====================第一种抽取 xxx:yyy类型.


    def pandinghefakey(a):
        return not re.fullmatch('[0-9|\s|-]*', a)


    pandinghefakey('2023-04-23 8')
    for fenge in [':', '：', '∶']:
        for i in ocr_jieguo:
            zifu = i['DetectedText']
            if fenge in zifu and zifu.split(fenge) and zifu.split(fenge)[0] and zifu.split(fenge)[1] and pandinghefakey(zifu.split(fenge)[0]):
                if zifu.split(fenge)[1] in jieguo1.values():
                    continue  # 不要value重复录入.

                if zifu.split(fenge)[0] in jieguo1:
                    # 如果之前已经存在了. 那么我们取信息最详细的那个
                    if len(zifu.split(fenge)[1]) > jieguo1[zifu.split(fenge)[0]]:
                        jieguo1[zifu.split(fenge)[0]] = zifu.split(fenge)[1]
                    else:
                        pass
                else:

                    jieguo1[zifu.split(fenge)[0]] = zifu.split(fenge)[1]
                pass

    print('jieguo1', jieguo1)
    pass


    # ==========数据进行行融合!!!!!!
    ocr_jieguo
    # 每一个数据的中心坐标:
    # from tools_for_geo import *
    ocr_jieguo2 = []
    for dex in range(len(ocr_jieguo)):
        i = ocr_jieguo[dex]

        line1 = i['Polygon'][0]['X'], i['Polygon'][0]['Y'], i['Polygon'][2]['X'], i['Polygon'][2]['Y']
        line1with_x_axis = math.atan(
            (-line1[3]+line1[1])/(line1[2]-line1[0]))/math.pi*180 if line1[2] != line1[0] else 90
        print(line1with_x_axis)
        #  if abs(line1with_x_axis)   >25: # 对于10度都扔了.
        # continue

        i['center_point'] = (i['Polygon'][0]['X']+i['Polygon'][2]
                            ['X'])/2, (i['Polygon'][0]['Y']+i['Polygon'][2]['Y'])/2
        ocr_jieguo2.append(i)
    # 一定还要先按照列排序!!!!!!!!!!否则逻辑不对.
    ocr_jieguo2.sort(key=lambda x: (x['center_point'][1], x['center_point'][0]))
    pass

    alltext = []
    print('打印腾通ocr原始返回值.')
    for i in ocr_jieguo2:
        print(i['DetectedText'], i['center_point'][0], i['center_point'][1])
        print()
        print()
        alltext.append(i['DetectedText'])


    # 生成一个包含30个随机整数的数组(1~100)
    data = np.random.randint(1, 101, size=30)
    data = np.array([i['center_point'][1] for i in ocr_jieguo2])

    zigao
    # 应用DBSCAN算法, 进行行分割. 设置好eps:类内最大距离, 和min_sample=1即可.
    # db = DBSCAN(eps=zigao/2+2, min_samples=1)
    # # db = DBSCAN(eps=3, min_samples=1)
    # db.fit(data.reshape(-1,1))
    # # 获取聚类标签
    # labels = db.labels_
    # pass

    # ======dbscan还不是我们想要的行分割函数.
    pass


    # =========对data进行分类,让所有分类的mean互相都大于 11: zigao/2+2
    # =======这个算法,目前有点慢, 可以再改吧以后.
    d = [[i] for i in range(len(data))]
    pass


    def hebing():  # 对d的子数组进行合并.
        nonlocal d
        hebingma = False
        for dex, i in enumerate(d):
            for dex2, j in enumerate(d):
                if j != i and abs(np.mean(data[j])-np.mean(data[i])) < zigao/2+2:
                    hebingma = True

                    d[dex] = i+j
                    # 把j添加到i的后面即可.
                    d.pop(dex2)
                    return hebingma  # 每一次合并,d内元素都修改了.所以每一次函数只合并一次更稳妥.
        return hebingma


    aaa = hebing()
    print(aaa)
    while hebing():
        pass
    pass


    # ========debug
    print('下面进行文本分行结果的debug')

    # 行拆分的结果. 结果是一个数组, 数组里面每一个元素是一个数组,小数组表示一行的全部识别结果. #先进行排序!!!!!!!!!!!!!!!!!!!!!!
    ocr_hangchaifen = []
    for i in d:
        tmp = []
        for i1 in i:
            tmp.append(ocr_jieguo2[i1])
        ocr_hangchaifen.append(sorted(tmp, key=lambda x: (x['center_point'][0])))
    ocr_hangchaifen.sort(key=lambda x: np.mean([y['center_point'][1] for y in x]))
    pass


    ocr_hangronghe = []
    for i in ocr_hangchaifen:
        tmp = '\t'.join([j['DetectedText'] for j in i])
        ocr_hangronghe.append(tmp)

    pass

    print('解析后打印每行')
    print('===============================')
    return ocr_hangronghe





def convert_pdf_to_pics(pdf_data, zoom, png_path, pdf_filename_base):  
    if not os.path.exists(png_path):  
        os.mkdir(png_path)  
  
    # 使用BytesIO将字节流转换为文件对象  
    pdf_file = BytesIO(pdf_data)  
  
    # 使用fitz打开这个“文件”  
    doc = fitz.open(stream=pdf_file)  
  
    total = doc.page_count  
    png_paths = []  # 创建一个空列表来存储PNG文件路径  
  
    for pg in range(total):  
        page = doc[pg]  
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).prerotate(0)  
        pm = page.get_pixmap(matrix=trans, alpha=False)  
        # 使用PDF文件名（去除扩展名）和页码来命名PNG图片  
        save_path = os.path.join(png_path, f'{pdf_filename_base}_page_{pg+1}.png')  
        pm.save(save_path)  
        png_paths.append(save_path)  # 将每个PNG文件的路径添加到列表中  
  
    doc.close()  
    return png_paths  # 返回包含所有PNG文件路径的列表 
import os
import sqlite3
# import cv2
import os
import io
import json
# import fitz  
from PIL import Image
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from io import BytesIO  
def ocr_my3(files): #用于多页的pdf识别.
    
    outdic={}
    for dex,file_data in enumerate(files):
        pdf_data = file_data.read()  
        pdf_filename_base = os.path.splitext(file_data.filename)[0]         
        png_paths = convert_pdf_to_pics(pdf_data,200,"./imgs",pdf_filename_base)
        for dex,png_path in enumerate(png_paths):
            print("png path is" + png_path)
            import  cv2
            aaaaa=cv2.imread(png_path,1)
            zuichangde =max(aaaaa.shape[0],aaaaa.shape[1])
            bili=zuichangde/1000
            
            bbb=cv2.resize(aaaaa,(int(aaaaa.shape[1]/bili),int(aaaaa.shape[0]/bili)))
            cv2.imwrite(png_path,bbb)
            with open(png_path, 'rb') as file:  
                png_data = file.read()

            # print(png_data)
            ttt = BytesIO(png_data)
            if 1:
                # 加载新图片的腾讯接口结果.
                # bbb=aaa2('ocr结构化输出/100007.png')  #===========这个图片的信息就是不带冒号的.全凭排版.
                # bbb = aaa2('ocr结构化输出/1000005.png')  # ===========这个图片的信息就是不带冒号的.全凭排版.
                
                
                try:
                # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
                # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
                # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
                    cred = credential.Credential(
                        "AKIDgBTXPhlffzUsHj4OXecSBh0VAlO1Wpy0", "2tbBd1EE8sbDi8LB7DFPURTYVN937Pkv")
                    # 实例化一个http选项，可选的，没有特殊需求可以跳过
                    httpProfile = HttpProfile()
                    httpProfile.endpoint = "ocr.tencentcloudapi.com"

                    # 实例化一个client选项，可选的，没有特殊需求可以跳过
                    clientProfile = ClientProfile()
                    clientProfile.httpProfile = httpProfile
                    # 实例化要请求产品的client对象,clientProfile是可选的
                    client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

                    # 实例化一个请求对象,每个接口都会对应一个request对象
                    req = models.GeneralAccurateOCRRequest()

                    import base64
                    tmp2=ttt.read()
                    # tmp=bytearray(tmp2)
                    if 1:
                        # img=cv2.imdecode(np.frombuffer(tmp, dtype=np.uint8),flags=cv2.IMREAD_COLOR)
                        encoded_string = base64.b64encode(
                            tmp2).decode("utf-8")

                    params = {
                        "ImageBase64": encoded_string,

                    }
                    req.from_json_string(json.dumps(params))

                    # 返回的resp是一个GeneralAccurateOCRResponse的实例，与请求对象对应
                    resp = client.GeneralAccurateOCR(req)
                    # 输出json格式的字符串回包
                    # print(resp.to_json_string())
                    bbb= resp.to_json_string()
                    print("腾讯返回json",bbb)

                except TencentCloudSDKException as err:

                    print(err)
                    return {}
                
                
                
                
                
                
                
                
                
                # bbb = aaa2(dizhi)  # ===========这个图片的信息就是不带冒号的.全凭排版.

                tengxunjieguo = json.loads(bbb)
                # 把识别的结果可视化,看目标检测的效果.
                # print('原始的腾讯返回结果',bbb)
                # print('==========================================')

            zuobiao = []
            for i in tengxunjieguo['TextDetections']:
                tmp = i['Polygon']
                # print(i['DetectedText'])
                tmp = [
                    [tmp[0]['X'], tmp[0]['Y']],
                    [tmp[1]['X'], tmp[1]['Y']],
                    [tmp[2]['X'], tmp[2]['Y']],
                    [tmp[3]['X'], tmp[3]['Y']],


                ]
                zuobiao.append(tmp)

                pass


                # zuobiao = np.array(zuobiao)
                # pass

                # keshihua = aaaa.copy()
                # cv2.polylines(keshihua, zuobiao, isClosed=True,
                #             color=(255, 125, 125), thickness=1)
                # cv2.imwrite('debug4.png', keshihua)


                # # ============识别表格的线. 我们先用传统方法来做.


                # kernel = np.ones((1, 3), np.uint8)

                # img = aaaa.copy()
                # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # # cv2.imwrite("13里面二值化的图片.png", binary)
                # # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=2)  # 二值化.
                # cv2.imwrite('debug1.png', binary)

            # 可以看到处理后基本的文字方向.
            # 进行直线检测.


            # =========改成用大量的逻辑判断来结构化文档


            ocr_jieguo = tengxunjieguo['TextDetections']

            pass
            # =======字高

            tmp = []
            for i in ocr_jieguo:
                tmp.append(i['ItemPolygon']['Height'])
            tmp.sort()
            tmp = np.array(tmp)
            tmp = np.median(tmp)
            zigao = tmp
            pass


            jieguo1 = {}
            # ====================第一种抽取 xxx:yyy类型.

            import re
            def pandinghefakey(a):
                return not re.fullmatch('[0-9|\s|-]*', a)


            pandinghefakey('2023-04-23 8')
            for fenge in [':', '：', '∶']:
                for i in ocr_jieguo:
                    zifu = i['DetectedText']
                    if fenge in zifu and zifu.split(fenge) and zifu.split(fenge)[0] and zifu.split(fenge)[1] and pandinghefakey(zifu.split(fenge)[0]):
                        if zifu.split(fenge)[1] in jieguo1.values():
                            continue  # 不要value重复录入.

                        if zifu.split(fenge)[0] in jieguo1:
                            # 如果之前已经存在了. 那么我们取信息最详细的那个
                            if len(zifu.split(fenge)[1]) > len(jieguo1[zifu.split(fenge)[0]]):
                                jieguo1[zifu.split(fenge)[0]] = zifu.split(fenge)[1]
                            else:
                                pass
                        else:

                            jieguo1[zifu.split(fenge)[0]] = zifu.split(fenge)[1]
                        pass

            # print('jieguo1', jieguo1)
            pass


            # ==========数据进行行融合!!!!!!
            ocr_jieguo
            # 每一个数据的中心坐标:
            # from tools_for_geo import *
            ocr_jieguo2 = []
            for dex in range(len(ocr_jieguo)):
                i = ocr_jieguo[dex]

                line1 = i['Polygon'][0]['X'], i['Polygon'][0]['Y'], i['Polygon'][2]['X'], i['Polygon'][2]['Y']
                line1with_x_axis = math.atan(
                    (-line1[3]+line1[1])/(line1[2]-line1[0]))/math.pi*180 if line1[2] != line1[0] else 90
                # print(line1with_x_axis)
                #  if abs(line1with_x_axis)   >25: # 对于10度都扔了.
                # continue

                i['center_point'] = (i['Polygon'][0]['X']+i['Polygon'][2]
                                    ['X'])/2, (i['Polygon'][0]['Y']+i['Polygon'][2]['Y'])/2
                ocr_jieguo2.append(i)
            # 一定还要先按照列排序!!!!!!!!!!否则逻辑不对.
            ocr_jieguo2.sort(key=lambda x: (x['center_point'][1], x['center_point'][0]))
            pass

            alltext = []
            # print('打印腾通ocr原始返回值.')
            for i in ocr_jieguo2:
                # print(i['DetectedText'], i['center_point'][0], i['center_point'][1])
                print()
                print()
                alltext.append(i['DetectedText'])


            # 生成一个包含30个随机整数的数组(1~100)
            data = np.random.randint(1, 101, size=30)
            data = np.array([i['center_point'][1] for i in ocr_jieguo2])

            zigao
            # 应用DBSCAN算法, 进行行分割. 设置好eps:类内最大距离, 和min_sample=1即可.
            # db = DBSCAN(eps=zigao/2+2, min_samples=1)
            # # db = DBSCAN(eps=3, min_samples=1)
            # db.fit(data.reshape(-1,1))
            # # 获取聚类标签
            # labels = db.labels_
            # pass

            # ======dbscan还不是我们想要的行分割函数.
            pass


            # =========对data进行分类,让所有分类的mean互相都大于 11: zigao/2+2
            # =======这个算法,目前有点慢, 可以再改吧以后.
            d = [[i] for i in range(len(data))]
            pass


            def hebing():  # 对d的子数组进行合并.
                nonlocal d
                hebingma = False
                for dex, i in enumerate(d):
                    for dex2, j in enumerate(d):
                        if j != i and abs(np.mean(data[j])-np.mean(data[i])) < zigao/2+2:
                            hebingma = True

                            d[dex] = i+j
                            # 把j添加到i的后面即可.
                            d.pop(dex2)
                            return hebingma  # 每一次合并,d内元素都修改了.所以每一次函数只合并一次更稳妥.
                return hebingma


            aaa = hebing()
            # print(aaa)
            while hebing():
                pass
            pass


            # ========debug
            print('下面进行文本分行结果的debug')

            # 行拆分的结果. 结果是一个数组, 数组里面每一个元素是一个数组,小数组表示一行的全部识别结果. #先进行排序!!!!!!!!!!!!!!!!!!!!!!
            ocr_hangchaifen = []
            for i in d:
                tmp = []
                for i1 in i:
                    tmp.append(ocr_jieguo2[i1])
                ocr_hangchaifen.append(sorted(tmp, key=lambda x: (x['center_point'][0])))
            ocr_hangchaifen.sort(key=lambda x: np.mean([y['center_point'][1] for y in x]))
            pass


            ocr_hangronghe = []
            for i in ocr_hangchaifen:
                tmp = '  '.join([j['DetectedText'] for j in i])
                ocr_hangronghe.append(tmp)

            pass

            print('解析后打印每行')
            print('===============================')
            for i in ocr_hangronghe:
                # print(i)
                print('===============================')


            # yolo 做一个语义分割的模型. 把整个图片切割几个部分. 比如第一个部分标记为 文本的框, 第二个为表格啥的.........做这个目标检测.如果做好这个,那么文本的框里面找第一个:前面的文字就是key, 后面的文字就是value, 表格按照第一行的列名分割下面的数据即可.

            # 版面分析: https://blog.csdn.net/weixin_43424450/article/details/135596393
            # https://blog.csdn.net/mddCSDN/article/details/132459685


            # 使用nlp的方法.数据全部拉成一个字符串, 然后nlp方法语义分类抽出里面的key, key中间夹着的部分就是value了.


            # 如果我们的key value都是一个确定的集合. 比如一个几万字符串的数组来存. 那么每次进行key value匹配即可了. 比如血液化验的这些xxx酶,啥的.做一个表.然后我们找到这个字之后直接返回他右边的数字即可.

            # ========安装上腾讯接口:
            # pip install  tencentcloud-sdk-python


            # ==============
            # 下面写的是一行信息的处理逻辑.############################################################################################
            print('抽取不会换行的基本信息')


            keys_candidate = [
                '姓名',
                '性别',
                '科室',
                '科别',
                '年龄',
                # '诊断',
                '体重',
                '就诊状态',
                '就诊科室',
                '就诊日期',
                '电话',
                '出生地',
                '籍贯',
                '民族',
                '电话',
                '证件号',
                '现住地',
                '户口地址',
                '身份证件类别',
                '国籍',
                '职业',
                '入院记录',
                '出院记录',
            ]
            # =去重
            keys_candidate2 = []
            [keys_candidate2.append(i) for i in keys_candidate if i not in keys_candidate2]
            keys_candidate = keys_candidate2
            # ==========直接字符串,跟上面的行信息强匹配即可.
            out = {}
            for mubiaokey in keys_candidate:
                for i in ocr_hangronghe:
                    # print(i)
                    tmp = i.split('\t')  # 单独的.
                    for dex, j in enumerate(tmp):
                        # ======删除冒号:
                        j = j.replace(':', '').replace('：', '').replace('∶', '')

                        if mubiaokey in j and j[:len(mubiaokey)] == mubiaokey:  # 在ocr小块里面
                            qita = j[j.index(mubiaokey)+len(mubiaokey):]  # 找到后面其他部分.
                            # 其他部分是不是数字.
                            if re.fullmatch('\d', qita):  # 后面只带一个数字
                                if dex+1 < len(tmp):
                                    xijie = tmp[dex+1]
                                    xijie2 = xijie.replace('1', '**1').replace('2', '**2').replace('3', '**3').replace('4', '**4').replace(
                                        '5', '**5').replace('6', '**6').replace('7', '**7').replace('8', '**8').replace('9', '**9').split('**')
                                    if xijie2:
                                        xijie2 = [i for i in xijie2 if qita in i]
                                        if xijie2:
                                            out[mubiaokey] = re.sub('\d\.', '', xijie2[0])

                                    pass  #
                                else:
                                    out[mubiaokey] = qita
                                continue
                            elif qita:
                                out[mubiaokey] = qita
                            else:
                                if dex+1 < len(tmp):
                                    out[mubiaokey] = tmp[dex+1]

                                pass
            print('抽取的基本信息', out)

            pass


            # 一行信息的处理逻辑. over############################################################################################
            # =====我期望: key 严格匹配的. 不用现在的包含关系. key写的很全, 比如: 血小板, *血小板 . 都看做两个.


            # ===================
            print('下面进行多行信息的抽取')

            # ============

            # 2024-05-27,13点42
            # 业务员:  1. 先看病例.  2. 看化验单
            # 三大模块: 1.ocr 2. 药物 3. 匹配:
            # 1.ocr: 多行:
            #       1.cv方法: 目标检测. 标记:整个key value box, 然后第一个冒号之前的部分我们作为key,其他作为value
            # yolo: 2000个一类
            #       2. nlp 方法: 整个当一个字符串, 让nlp做分隔.(大模型)
            #       3. 正则


            # 3.匹配:
            #                                      字符串包含:  六个月  !=  半年.
            #                                      bert:句向量.(小模型)
            #                                      大量nlp算法.(太过复杂, 推荐是使用大模型或者医疗垂直领域大模型)


            # 前后端. 人工校验之后,再入数据库.


            # =========解析段落.
            if 0:
                ocr_hangchaifen
                # 求每一行的长度.
                hangchangdu = []
                for i in ocr_hangchaifen:
                    if len(i) == 1:
                        chang = i[0]['ItemPolygon']['Width']
                        pass
                    else:
                        chang = i[-1]['ItemPolygon']['X'] - \
                            i[0]['ItemPolygon']['X']+i[-1]['ItemPolygon']['Width']
                    hangchangdu.append(chang)
                pass

                changdu2 = sorted(hangchangdu)


                zifuchangdu = []
                for i in ocr_hangchaifen:
                    chang = sum([j['ItemPolygon']['Width'] for j in i])
                    zifuchangdu.append(chang)
                pass

                zifumidu = []
                for i in range(len(zifuchangdu)):
                    zifumidu.append(hangchangdu[i]/zifuchangdu[i])

                # 大于0.8的最长那个最为最长的行.
                hangchangdu = np.array(hangchangdu)
                zifumidu = np.array(zifumidu)
                zifuchangdu = np.array(zifuchangdu)


                if len(hangchangdu[zifumidu > 0.8]) > 0:
                    zuichanghang = sorted(hangchangdu[zifumidu > 0.8])[-1]
                else:
                    zuichanghang = sorted(hangchangdu)[-1]
                pass


                juzizuihoudexzuobiao = []

                for i in ocr_hangchaifen:
                    zuihoux = i[-1]['ItemPolygon']['X']+i[-1]['ItemPolygon']['Width']
                    juzizuihoudexzuobiao.append(zuihoux)
                pass

                juzizuihoudexzuobiao = np.array(juzizuihoudexzuobiao)
                if len(juzizuihoudexzuobiao[zifumidu > 0.8]) > 0:
                    zuiyouduan = sorted(juzizuihoudexzuobiao[zifumidu > 0.8])[-1]
                else:
                    zuiyouduan = sorted(juzizuihoudexzuobiao)[-1]
                pass


            # 大于zuiyouduan*0.85的行我们才认为是一个整行.


            # 多行, 必须作为开头的写这里.
            duohangkaitou = [
                '主诉',
                '现病史',
                '既往史',
                '个人史',
                '婚育史',
                '主要诊断',
                '其他诊断',
                '出院医嘱',
                '入院诊断',
                '出院诊断',
                '治疗经过简介',
                '出院时情况',
                '体格检查',
                '处方',
                '药物过敏史',
                '诊断',
                '辅助检验',
                '医嘱、处置',
                '医嘱',
                '治疗经过',
                '西医诊断',
                '病理诊断'









            ]
            
            duohangkaitou=[i+':' for i in duohangkaitou]
            
            

            #==============多行包含就算的写这里.
            duohangzhongjian=['查房记录',
                            '病程记录',
                            '病房记录',
                            '疾病记录'


            ]



            duohangkaitou2 = []
            for i in duohangkaitou:
                if i not in duohangkaitou2:
                    duohangkaitou2.append(i)
            duohangkaitou = duohangkaitou2


            def pandinghangshifuohangkaitou(a): # 2024-06-25,13点03 添加多行判断. 返回找到key的长度.
                for i in duohangkaitou:
                    if a[:len(i)] == i:
                        return len(i)
                for i in duohangzhongjian:
                    if i in a:
                        return a.index(i)+len(i)


                return False


            def pandingshiyigechangju(i):
                return True
                return i[-1]['ItemPolygon']['X']+i[-1]['ItemPolygon']['Width'] > zuiyouduan*0.85


            ocrhangtext = ocr_hangronghe
            # ======直接抽取多行.
            tmp = ''

            changjuduanju = []
            for i in ocr_hangchaifen:
                changjuduanju.append(pandingshiyigechangju(i))

            # =====2024-05-28,13点18 如果一个句子只有我们的duohangkaitou , 那么他也是判定为长句, 可以链接下面的句子.


            for dex, i in enumerate(ocrhangtext):
                panding = pandinghangshifuohangkaitou(i)
                if panding and len(i[panding:]) < 2:  # 后面的垃圾字符小于2 就算无效字符,所以看做长句.
                    changjuduanju[dex] = True


            shifoushikaitou = []
            for i in ocrhangtext:
                shifoushikaitou.append(pandinghangshifuohangkaitou(i))


            for dex, i in enumerate(ocrhangtext):

                if shifoushikaitou[dex] and changjuduanju[dex]:
                    if tmp:  # 记录旧的
                        suoyin = pandinghangshifuohangkaitou(tmp)
                        out[tmp[:suoyin]] = tmp[suoyin:]
                    tmp = i
                if not shifoushikaitou[dex]:
                    if dex == 0:
                        continue
                    if dex != 0:
                        shangyihang = changjuduanju[dex-1]
                        if shangyihang:  # 上一行如果是长句子.
                            tmp += i  # 非开头句子只有上一句是长句子时候才能加入段落.
                if shifoushikaitou[dex] and not changjuduanju[dex]:
                    if tmp:  # 记录旧的
                        suoyin = pandinghangshifuohangkaitou(tmp)
                        out[tmp[:suoyin]] = tmp[suoyin:]
                    tmp = i
                    if tmp:  # 记录当前的
                        suoyin = pandinghangshifuohangkaitou(tmp)
                        out[tmp[:suoyin]] = tmp[suoyin:]
                    tmp = ''
                if dex == len(ocrhangtext)-1:
                    # 最后一个:
                    if tmp:  # 记录旧的
                        suoyin = pandinghangshifuohangkaitou(tmp)
                        out[tmp[:suoyin]] = tmp[suoyin:]

                # #判定头部:
                # panding=pandinghangshifuohangkaitou(i)
                # if panding:
                #    if tmp:
                #       suoyin=pandinghangshifuohangkaitou(tmp)
                #       out[tmp[:suoyin]]=tmp[suoyin:]
                #    tmp=i #记录下开头
                # if not(panding)
            # 总结多行的抽取思路: 我们先计算那些行是长的, 长的标准是字的密度大于0.85. 字的密度是ocrbox长度和/收尾box长度
            #                  只有长的我们才允许他拼接到下面一行作为段落.如果不是长的,那么进行抽取即可. 抽取按照句子前几个字属于我们keyword里面即可.

            pass
            out2={}
            for i in out:
                if i:
                    out2[i]=out[i]
            out=out2
            # print('抽取完多行完毕!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', )
            # for i in out:
            #     print(i+'=============================='+out[i])
                
        # 2024-07-16,10点05 ocr添加检测结果识别.
            jiancexiangmu=[
                '谷丙转氨酶',

            '谷草转氨酶',

        '谷草/谷丙',  
        '谷氨酰转肽酶',
            '碱性磷酸酶',
            '总蛋白'  ,
            '白蛋白',  

            '球蛋白' , 

            '白球比'  ,

            '总胆汁酸',

            '前白蛋白',

            '核苷酸酶',

            '总胆红素',

            '直接胆红素',

            '间接胆红素',

            '甘油三脂',
            '总胆固醇',

            

        '低密度脂蛋白',

        '载脂蛋白A1',

        '载脂蛋白B' ,
            '脂蛋白(a)',
            '葡萄糖'  ,
            '尿酸'    ,

                
                '尿素',
                '肌酐',
                '肌酐/尿素',
                '微球蛋白',
                '羟丁酸脱氢酶',
                '乳酸脱氢酶',
                '肌酸激酶',
                '肌酸酶同功酶',
                '钾',
                '钠',
                '氯',
                '二氧化碳',
                '阴离子间隙',
                '钙',
                '磷',
                '镁',
                '铁',
                '高密度脂蛋白',
                '转铁蛋白',
                
            ]
            ocrhangtext
            yuanshishuju=[i.split() for i in ocrhangtext]
            #原始数据后处理:
            for i in yuanshishuju:
                for dex in range(len(i)):
                    for muban in jiancexiangmu:
                        
                        if muban in i[dex] and dex<len(i)-1:
                            zifu=i[dex] 
                            shuzi=i[dex+1]
                            if shuzi=='↓' or shuzi=='↑' and dex+2<len(i):
                                i[dex+1]=i[dex+1]+i[dex+2]
                                
            
            
            
            
            
            
            
            for i in yuanshishuju:
                for dex in range(len(i)):
                    for muban in jiancexiangmu:
                        
                        if muban in i[dex] and dex<len(i)-1:
                            zifu=i[dex] 
                            shuzi=i[dex+1]
                            def  pandingshuzi(s):
                                for i in s:
                                    if i not  in ['0','1','2','3','4','5','6','7','8','9','0','.','↑','↓']:
                                        return False
                                for jjj in out.values():
                                    if zifu in jjj:
                                        return False
                                return True
                            if pandingshuzi(shuzi):
                                

                                out[zifu]=shuzi
            # print('检测')
                
                
            # print('抽取检测结果!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # for i in out:
            #     print(i+'======'+out[i])
                
            import re
            for i in out:
                out[i]=re.sub('CS.*扫描全能王','',out[i])
                out[i]=re.sub('Cs.*扫描全能王','',out[i])
                out[i]=re.sub('cs.*扫描全能王','',out[i])
                out[i]=re.sub('第\d页','',out[i])
            
            
            
            
            
            
            
            
            
            
            os.remove(png_path)
            if isinstance(ttt,TencentCloudSDKException):
                return jsonify(ttt.message)
            outdic=outdic|ttt  
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    return out
        
        
        
        
        
    return out








import  asyncio,time

def ocr_my2(dizhi,metainfo):
    if 1:
        # 加载新图片的腾讯接口结果.
        # bbb=aaa2('ocr结构化输出/100007.png')  #===========这个图片的信息就是不带冒号的.全凭排版.
        # bbb = aaa2('ocr结构化输出/1000005.png')  # ===========这个图片的信息就是不带冒号的.全凭排版.
        
        
        try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(
                "AKIDVwCKF4kHckgQxY243LZcKrBKNCoIQRGu", "Z1Ibo380fIpDOdmlY7SaWRJ0Um4A3xRr")
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GeneralAccurateOCRRequest()

            import base64
            tmp2=dizhi.read()
            # tmp=bytearray(tmp2)
            if 1:
                # img=cv2.imdecode(np.frombuffer(tmp, dtype=np.uint8),flags=cv2.IMREAD_COLOR)
                encoded_string = base64.b64encode(
                    tmp2).decode("utf-8")

            params = {
                "ImageBase64": encoded_string,

            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个GeneralAccurateOCRResponse的实例，与请求对象对应
            print('运行腾讯')
            resp = client.GeneralAccurateOCR(req)
            # 输出json格式的字符串回包
            # print(resp.to_json_string())
            bbb= resp.to_json_string()

        except TencentCloudSDKException as err:
            print('Faile tengxun jiekou')
            print(err)
            return {}
        
        
        
        
        
        
        
        
        
        # bbb = aaa2(dizhi)  # ===========这个图片的信息就是不带冒号的.全凭排版.

        # tengxunjieguo = json.loads(bbb)
        # 把识别的结果可视化,看目标检测的效果.
        # print('原始的腾讯返回结果',bbb)
        # print('==========================================')
        
        
        tengxunjieguo = json.loads(bbb)
        # 把识别的结果可视化,看目标检测的效果.
        # print('原始的腾讯返回结果',bbb)
        # print('==========================================')

        zuobiao = []
        print(metainfo)
        print('当前页的识别角度',tengxunjieguo['Angel'])
        
        
        #========切割掉全能王:
        # gaodu2=int(aaaaa.shape[0]*(552-29)/552)
        # aaaaa=aaaaa[:gaodu2,:]
        if 0<=tengxunjieguo['Angel']<=30 or 330<=tengxunjieguo['Angel']<=360:
            qudiaoindex=[]
            bianjie=int(metainfo[0]*(552-29)/552)
            tmp2=[]
            for i in range(len(tengxunjieguo['TextDetections'])):
                if tengxunjieguo['TextDetections'][i]['Polygon'][0]['Y']<=bianjie:
                    tmp2.append(tengxunjieguo['TextDetections'][i])
            tengxunjieguo['TextDetections']=tmp2
        if 240<tengxunjieguo['Angel']<300:
            qudiaoindex=[]
            bianjie=int(metainfo[1]*(1181-100)/1181)
            tmp2=[]
            for i in range(len(tengxunjieguo['TextDetections'])):
                if tengxunjieguo['TextDetections'][i]['Polygon'][0]['X']<=bianjie:
                    tmp2.append(tengxunjieguo['TextDetections'][i])
            tengxunjieguo['TextDetections']=tmp2
            
        #=======其他角度的切割和旋转还需要写.
        if 80<tengxunjieguo['Angel']<110:
            qudiaoindex=[]
            bianjie=int(metainfo[0]*(552-29)/552)
            tmp2=[]
            for i in range(len(tengxunjieguo['TextDetections'])):
                if tengxunjieguo['TextDetections'][i]['Polygon'][0]['Y']<=bianjie:
                    tmp2.append(tengxunjieguo['TextDetections'][i])
            tengxunjieguo['TextDetections']=tmp2
        
        
        
        
        
        
        
        # 旋转矫正:
        
        
        
        if 80<tengxunjieguo['Angel']<110:
            #竖直图片:
            #===坐标转回去:
            for i in range(len(tengxunjieguo['TextDetections'])):
                #修改polygon即可.
                tmp=tengxunjieguo['TextDetections'][i]
                for j in range(len(tmp['Polygon'])):
                    
                    
                    tmp2=metainfo[1]-tmp['Polygon'][j]['X']
                    tmp3=tmp['Polygon'][j]['Y']
                    tmp['Polygon'][j]['X']=tmp3
                    tmp['Polygon'][j]['Y']=tmp2
                tengxunjieguo['TextDetections'][i]=tmp
        
        
        
        
        
        
        
        
        
        
        if 240<tengxunjieguo['Angel']<300:
            #竖直图片:
            #===坐标转回去:
            for i in range(len(tengxunjieguo['TextDetections'])):
                #修改polygon即可.
                tmp=tengxunjieguo['TextDetections'][i]
                for j in range(len(tmp['Polygon'])):
                    
                    
                    tmp2=metainfo[0]-tmp['Polygon'][j]['Y']
                    tmp3=tmp['Polygon'][j]['X']
                    tmp['Polygon'][j]['X']=tmp2
                    tmp['Polygon'][j]['Y']=tmp3
                tengxunjieguo['TextDetections'][i]=tmp
            
            pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        for i in tengxunjieguo['TextDetections']:
            tmp = i['Polygon']
            # print(i['DetectedText'])
            tmp = [
                [tmp[0]['X'], tmp[0]['Y']],
                [tmp[1]['X'], tmp[1]['Y']],
                [tmp[2]['X'], tmp[2]['Y']],
                [tmp[3]['X'], tmp[3]['Y']],


            ]
            zuobiao.append(tmp)

            pass


            # zuobiao = np.array(zuobiao)
            # pass

            # keshihua = aaaa.copy()
            # cv2.polylines(keshihua, zuobiao, isClosed=True,
            #             color=(255, 125, 125), thickness=1)
            # cv2.imwrite('debug4.png', keshihua)


            # # ============识别表格的线. 我们先用传统方法来做.


            # kernel = np.ones((1, 3), np.uint8)

            # img = aaaa.copy()
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # # cv2.imwrite("13里面二值化的图片.png", binary)
            # # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=2)  # 二值化.
            # cv2.imwrite('debug1.png', binary)

        # 可以看到处理后基本的文字方向.
        # 进行直线检测.


        # =========改成用大量的逻辑判断来结构化文档


        ocr_jieguo = tengxunjieguo['TextDetections']

        pass
        # =======字高

        tmp = []
        for i in ocr_jieguo:
            tmp.append(i['ItemPolygon']['Height'])
        tmp.sort()
        tmp = np.array(tmp)
        tmp = np.median(tmp)
        zigao = tmp
        
        # ========去掉过小的字
        ocr_jieguo=[i for i in ocr_jieguo if i['ItemPolygon']['Height']>zigao*0.66]
        
        
        
        
        pass


        jieguo1 = {}
        # ====================第一种抽取 xxx:yyy类型.

        import re
        def pandinghefakey(a):
            return not re.fullmatch('[0-9|\s|-]*', a)


        pandinghefakey('2023-04-23 8')
        for fenge in [':', '：', '∶']:
            for i in ocr_jieguo:
                zifu = i['DetectedText']
                if fenge in zifu and zifu.split(fenge) and zifu.split(fenge)[0] and zifu.split(fenge)[1] and pandinghefakey(zifu.split(fenge)[0]):
                    if zifu.split(fenge)[1] in jieguo1.values():
                        continue  # 不要value重复录入.

                    if zifu.split(fenge)[0] in jieguo1:
                        # 如果之前已经存在了. 那么我们取信息最详细的那个
                        if len(zifu.split(fenge)[1]) > len(jieguo1[zifu.split(fenge)[0]]):
                            jieguo1[zifu.split(fenge)[0]] = zifu.split(fenge)[1]
                        else:
                            pass
                    else:

                        jieguo1[zifu.split(fenge)[0]] = zifu.split(fenge)[1]
                    pass

        # print('jieguo1', jieguo1)
        pass


        # ==========数据进行行融合!!!!!!
        ocr_jieguo
        # 每一个数据的中心坐标:
        # from tools_for_geo import *
        ocr_jieguo2 = []
        for dex in range(len(ocr_jieguo)):
            i = ocr_jieguo[dex]

            line1 = i['Polygon'][0]['X'], i['Polygon'][0]['Y'], i['Polygon'][2]['X'], i['Polygon'][2]['Y']
            line1with_x_axis = math.atan(
                (-line1[3]+line1[1])/(line1[2]-line1[0]))/math.pi*180 if line1[2] != line1[0] else 90
            # print(line1with_x_axis)
            #  if abs(line1with_x_axis)   >25: # 对于10度都扔了.
            # continue

            i['center_point'] = (i['Polygon'][0]['X']+i['Polygon'][2]
                                ['X'])/2, (i['Polygon'][0]['Y']+i['Polygon'][2]['Y'])/2
            ocr_jieguo2.append(i)
        # 一定还要先按照列排序!!!!!!!!!!否则逻辑不对.
        ocr_jieguo2.sort(key=lambda x: (x['center_point'][1], x['center_point'][0]))
        pass

        alltext = []
        # print('打印腾通ocr原始返回值.')
        for i in ocr_jieguo2:
            # print(i['DetectedText'], i['center_point'][0], i['center_point'][1])
            # print()
            # print()
            alltext.append(i['DetectedText'])


        # 生成一个包含30个随机整数的数组(1~100)
        data = np.random.randint(1, 101, size=30)
        data = np.array([i['center_point'][1] for i in ocr_jieguo2])

        zigao
        # 应用DBSCAN算法, 进行行分割. 设置好eps:类内最大距离, 和min_sample=1即可.
        # db = DBSCAN(eps=zigao/2+2, min_samples=1)
        # # db = DBSCAN(eps=3, min_samples=1)
        # db.fit(data.reshape(-1,1))
        # # 获取聚类标签
        # labels = db.labels_
        # pass

        # ======dbscan还不是我们想要的行分割函数.
        pass


        # =========对data进行分类,让所有分类的mean互相都大于 11: zigao/2+2
        # =======这个算法,目前有点慢, 可以再改吧以后.
        d = [[i] for i in range(len(data))]
        pass


        def hebing():  # 对d的子数组进行合并.
            nonlocal d
            hebingma = False
            for dex, i in enumerate(d):
                for dex2, j in enumerate(d):
                    if j != i and abs(np.mean(data[j])-np.mean(data[i])) < zigao/2+2:
                        hebingma = True

                        d[dex] = i+j
                        # 把j添加到i的后面即可.
                        d.pop(dex2)
                        return hebingma  # 每一次合并,d内元素都修改了.所以每一次函数只合并一次更稳妥.
            return hebingma


        aaa = hebing()
        # print(aaa)
        while hebing():
            pass
        pass


        # ========debug
        print('下面进行文本分行结果的debug')

        # 行拆分的结果. 结果是一个数组, 数组里面每一个元素是一个数组,小数组表示一行的全部识别结果. #先进行排序!!!!!!!!!!!!!!!!!!!!!!
        ocr_hangchaifen = []
        for i in d:
            tmp = []
            for i1 in i:
                tmp.append(ocr_jieguo2[i1])
            ocr_hangchaifen.append(sorted(tmp, key=lambda x: (x['center_point'][0])))
        ocr_hangchaifen.sort(key=lambda x: np.mean([y['center_point'][1] for y in x]))
        pass
        #2024-10-15,7点52   对ocr_hangchaifen 结果加入空格的信息!!!!!!!!!!!!!!
        hangweizhi=[]
        zigao
        for i in ocr_hangchaifen:
                yihangbox=[]
                ocr_yihangxinxi = i[0]# ocr_yihangxinxi={'DetectedText': 'CS', 'Confidence': 100, 'Polygon': [{...}, {...}, {...}, {...}], 'AdvancedInfo': '{"Parag":{"ParagNo":31}}', 'ItemPolygon': {'X': 1285, 'Y': 1946, 'Width': 29, 'Height': 25}, 'Words': [], 'WordCoordPoint': [], 'center_point': (1299.0, 1958.0)}

                yihangbox.append(ocr_yihangxinxi['Polygon'][0])
                yihangbox.append(ocr_yihangxinxi['Polygon'][3])
                yihangbox.append(i[-1]['Polygon'][1])
                yihangbox.append(i[-1]['Polygon'][2])
                # yihangbox.append(i[-1]['Polygon'][1],i[-1]['Polygon'][2])
                hangweizhi.append(yihangbox)
        pass
        # 2024-10-15,10点18 添加空格信息.
        leftest=0 # 最左边的文字的横坐标
        leftest=min([i[0]['X'] for i in hangweizhi])




        ocr_hangronghe = []
        for i in ocr_hangchaifen:
            tmp = '  '.join([j['DetectedText'] for j in i])
            ocr_hangronghe.append(tmp)

        import re
        out=ocr_hangronghe

        leftlist=[i[0]['X'] for i in hangweizhi]
        for i in range(len(out)):
            out[i]=' '*int(  (leftlist[i]-leftest)/zigao)+out[i]
        # 加上了前空格.



        # 加入空白行!
        heightlist=[(i[0]['Y']+i[2]['Y'])/2 for i in hangweizhi]
        if len(heightlist)>=2:

            gaoducha=[0]+[heightlist[i]-heightlist[i-1] for i in range(1,len(heightlist))] # gaoducha[i] =heightlist[i]-heightlist[i-1]
        else:
                gaoducha=[0]
        out2=[]
        for i in range(len(gaoducha)):
            if gaoducha[i]>zigao*2:
               out2.append('')  
               out2.append(out[i])
            else:
                out2.append(out[i])
        out=out2

        for i in range(len(out)):
            out[i]=re.sub('CS.*扫描全能王','',out[i])
            out[i]=re.sub('Cs.*扫描全能王','',out[i])
            out[i]=re.sub('cs.*扫描全能王','',out[i])
            out[i]=re.sub('Os.*扫描全能王','',out[i])
            out[i]=re.sub('os.*扫描全能王','',out[i])
            out[i]=re.sub('扫描全能王','',out[i])
            out[i]=re.sub('第\d页','',out[i])
        
        
        
        
        
        
        return out

































if __name__ == '__main__':
    # 大模型调用只需要在这里面设置好参数即可. 用的是腾讯最好的模型.混元pro
    # 1w token 1yuan # 8b  f16 int8 int4  24G    3080- 4090做finetune和推理   2w  Dell 本地部署  本地电脑+公网ip  品牌机  ubuntu
    import time
    aaaaaa=time.time()
    ocr_my('33.jpg')
    # ocr_my('108888.png')