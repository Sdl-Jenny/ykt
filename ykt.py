import asyncio
import time
import requests
import websockets
import json
import webbrowser
import os


session = requests.Session()

async def websocket_session():
    uri = "wss://www.yuketang.cn/wsapp"  # WebSocket 服务器的 URI
    headers = {

        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
        'Origin': "https://www.yuketang.cn",
    }
    data = {
        "op": "requestlogin",
        "role": "web",
        "version": 1.4,
        "type": "qrcode",
        "from": "web"
    }

    async with websockets.connect(uri, extra_headers=headers) as websocket:
        # 将字典转换为JSON字符串并发送

        json_data = json.dumps(data)
        await websocket.send(json_data)


        # 保持连接并监听服务器的消息
        while True:

                response = await websocket.recv()

                if 'ticket' in response:
                    response_json = json.loads(response)
                    url = response_json['ticket']

                    response = session.get(url=url)

                    # 使用默认的图像查看器打开图像
                    if response.status_code == 200:
                        # 保存图片
                        with open('sunci.png', 'wb') as file:
                            file.write(response.content)


                        # 打开图片
                        print("大人请微信扫码！！")
                        webbrowser.open('file://' + os.path.realpath('sunci.png'))
                    else:
                        print(f"Failed to retrieve the image. Status code: {response.status_code}")
                if 'subscribe_status' in response:

                    json_data = json.loads(response)
                    auth = json_data['Auth']
                    UserID = json_data['UserID']

                    url = "https://www.yuketang.cn/pc/web_login"
                    data = '{"UserID":'+str(UserID)+',"Auth":"'+auth+'"}'
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
                    response = session.post(url,data,headers)
                    break

        ssxx()




def ssxx():
    url = 'https://www.yuketang.cn/v2/api/web/courses/list?identity=2'

    response = session.get(url=url)

    JSON = json.loads(response.text)

    if len(JSON['data']['list']) > 1:
        for i in range(0, len(JSON['data']['list'])):
            print("序号：" + str(i) + "-----" + JSON['data']['list'][i]['name'])
        print('---------------------------------------------')
        print('---------------------------------------------')
        print('---------------------------------------------')
        print('---------------------------------------------')

        min_value = 0  # 定义范围的最小值
        max_value = len(JSON['data']['list']) - 1  # 定义范围的最大值

        while True:
            user_input = input(f"请输入您想观看的课程序号：\n")
            try:
                num = int(user_input)
                if num >= min_value and num <= max_value:

                    global classroom_id
                    classroom_id = str(JSON['data']['list'][num]['classroom_id'])

                    url = "https://www.yuketang.cn/v2/api/web/logs/learn/" + str(
                        classroom_id) + "?actype=-1&page=0&offset=20&sort=-1"
                    response = session.get(url)

                    JSON = json.loads(response.text)

                    break
                else:
                    print(f"输入错误，请输入一个介于 {min_value} 和 {max_value} 之间的课程编号。")
            except ValueError:
                print("输入错误，请确保您输入的是一个整数。")

    else:
        print("你没选课？！ 你疯啦？")
        exit(-1)

    url = 'https://www.yuketang.cn/c27/online_courseware/xty/kls/pub_news/' + str(
        JSON['data']['activities'][1]['courseware_id']) + '/'
    headers = {
        'xtbz': 'ykt',
        'classroom-id': str(classroom_id)
    }
    response = session.get(url, headers=headers)

    JSON = json.loads(response.text)
    c_course_id = str(JSON['data']['course_id'])
    s_id = str(JSON['data']['s_id'])

    for i in range(len(JSON['data']['content_info'])):
        print("正在观看----" + JSON['data']['c_short_name'] + " 第" + str(i) + "章" + "----共找到" + str(
            len(JSON['data']['content_info'][i]['section_list'])) + "个视频。")
        for j in range(len(JSON['data']['content_info'][i]['section_list'])):
            cards_id = '0'

            video_id = str(JSON['data']['content_info'][i]['section_list'][j]['leaf_list'][0]['id'])

            url = 'https://www.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/' + classroom_id + '/' + video_id + '/'
            response = session.get(url=url, headers=headers)

            JSON_TEMP = json.loads(response.text)

            ccid = JSON_TEMP['data']['content_info']['media']['ccid']
            d = JSON_TEMP['data']['content_info']['media']['duration']

            v = str(JSON_TEMP['data']['id'])
            u = str(JSON_TEMP['data']['user_id'])
            timestamp_ms = int(time.time() * 1000)
            url = "https://www.yuketang.cn/video-log/get_video_watch_progress/?cid=" + c_course_id + "&user_id=" + u + "&classroom_id=" + classroom_id + "&video_type=video&vtype=rate&video_id=" + video_id + "&snapshot=1"
            response_new = session.get(url=url, headers=headers)
            JSON_NEW = json.loads(response_new.text)
            if d == 0:
                url = "https://www.yuketang.cn/video-log/get_video_watch_progress/?cid=" + c_course_id + "&user_id=" + u + "&classroom_id=" + classroom_id + "&video_type=video&vtype=rate&video_id=" + video_id + "&snapshot=1"
                response_new = session.get(url=url, headers=headers)
                JSON_NEW = json.loads(response_new.text)
                d = int(JSON_NEW[video_id]['video_length'])

            try:
                sunci = JSON_NEW['data'][video_id]['completed']
            except Exception as e:
                sunci = 0

            while sunci != 1:
                for k in range(25):
                    time.sleep(0.6)
                    print("正在观看第" + str(i) + "章 第" + str(j + 1) + "个视频----当前进度：" + str(4 * (k + 1)) + "%")
                    url = 'https://www.yuketang.cn/video-log/heartbeat/'
                    data = '{"heart_data":[{"i":5,"et":"heartbeat","p":"web","n":"ali-cdn.xuetangx.com","lob":"ykt","cp":' + str(
                        d * (1 + k) / 25) + ',"fp":100,"tp":100,"sp":5,"ts":"' + str(timestamp_ms + d * (
                            1 + k) * 2500) + '","u":' + u + ',"uip":"","c":' + c_course_id + ',"v":' + v + ',"skuid":' + str(
                        s_id) + ',"classroomid":"' + classroom_id + '","cc":"' + ccid + '","d":' + str(
                        d) + ',"pg":"' + video_id + '_x33v","sq":11,"t":"video","cards_id":0,"slide":0,"v_url":""}]}'

                    headers1 = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
                        'Content-Type': 'application/json',
                        'authority': 'changjiang.yuketang.cn',
                        'method': 'GET',
                        'path': '/v2/api/web/courses/list?identity=2',
                        'referer': 'https://changjiang.yuketang.cn/v2/web/personal/info',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        # 'university-id':'2727',
                    }

                    response = session.post(url=url, data=data, headers=headers1)

                    url = "https://www.yuketang.cn/video-log/get_video_watch_progress/?cid=" + c_course_id + "&user_id=" + u + "&classroom_id=" + classroom_id + "&video_type=video&vtype=rate&video_id=" + video_id + "&snapshot=1"
                    response_new = session.get(url=url, headers=headers)
                    JSON_NEW = json.loads(response_new.text)
                    has_watched = JSON_NEW['data'][video_id]['watch_length']
                    if d == 0:
                        d = int(JSON_NEW[video_id]['video_length'])
                    

                    try:
                        sunci = JSON_NEW['data'][video_id]['completed']
                    except Exception as e:
                        sunci = 0
                    if sunci == 1:
                        break
    print("这门课看完了啊！ 孙辞期待与您的下次相遇！")







# 运行异步函数
asyncio.run(websocket_session())
