# -*- coding: utf8 -*-

import requests
import re
import time
from urllib.parse import quote
import json
import logging
import os
import sys
import time
import traceback
import requests


# 需要修改的部分。
# 配置ck pc登录腾讯视频账号，自行获取cookie 【ptcz=....之后的完整部分】
ck = [
	'pgv_pvid=3382049682; o_cookie=309712560; sd_userid=77261629683156435; sd_cookie_crttime=1629683156435; _ga=GA1.2.32775168.1629863714; tvfe_boss_uuid=a7516dd677376a05; video_guid=71a5ab5d01246dee; video_platform=2; ts_uid=3938556660; login_remember=qq; tvfe_search_uid=0503f245-19c7-4ffd-9808-b04d76583edb; txv_boss_uuid=3ff230f1-2242-8851-c72c-6a885f4942af; pac_uid=1_309712560; iip=0; main_login=qq; vqq_vuserid=157740632; vqq_access_token=E1119CC09A647392E5490DE789C30840; vqq_openid=8F9FFDB35C6D3D6ABB750C49CA6A9496; vqq_appid=101483052; qq_head=https://tvpic.gtimg.cn/head/f94bfb87e03242503c3ae087d98ff36dd754fd2698b38c8a78d70c4ae8ad5c854e15a5bf/157; qq_nick=%E4%BD%A0%E5%88%AB%E5%AF%B9%E4%B8%8D%E8%B5%B7; bucket_id=9231000; pgv_info=ssid=s7603521412; vversion_name=8.2.95; video_omgid=71a5ab5d01246dee; _qpsvr_localtk=0.5050119576439802; vqq_vusession=vkrqedRGxv_5LFV_gQKDtg..; ptag=www_baidu_com; ad_play_index=77; uid=251768443; ts_last=v.qq.com/; ts_refer=www.baidu.com/; qv_als=3TJq2VUDMoFniwu5A116409374002lAPjw=='
]
# 需要修改的部分结束。下面的不要动


logger = logging.getLogger(name=None)  # 创建一个日志对象
logging.Formatter("%(message)s")  # 日志内容格式化
logger.setLevel(logging.INFO)  # 设置日志等级
logger.addHandler(logging.StreamHandler())  # 添加控制台日志
# logger.addHandler(logging.FileHandler(filename="text.log", mode="w"))  # 添加文件日志


# tx_getVsToken:2019.12.1
def jiemi(str1):
    i = 5381
    e = 0
    n = len(str1)
    while e < n:
        i = i + (i << 5) + ord(str1[e])
        e = e+1
        # print(i)
    # print(i)
    res = 2147483647 & i
    # print(res)
    return str(res)

# 更新cookie


def renew_cookie(cookie_list):
    # 获取刷新cookie的地址,自动跳过更新失败的cookie
    res = requests.get(
        'https://vm.gtimg.cn/tencentvideo_v1/script/txv.core.js?v=20210720').text
    url1 = re.search(r'authRefresh:o(.*?)",', res).group(1)
    auth_url = 'https://access.video.qq.com'+url1[2:]
    new_cookie_list = []

    # 循环更新cookie
    for cookie1 in cookie_list:
        try:
            s = requests.session()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36',
                       'referer': 'https://v.qq.com/', 'Cookie': cookie1}
            this_time = int(round(time.time() * 1000))

            cookies_arr = cookie1.split('; ')
            for cookie2 in cookies_arr:
                c1 = cookie2.split('=')
                if c1[0] == 'vqq_vusession':
                    vqq_vusession = c1[1]
                if c1[0] == 'vqq_access_token':
                    vqq_access_token = c1[1]

            #print('vqq_vusession:'+vqq_vusession )
            vqq_vusession1 = jiemi(vqq_vusession)
            g_actk = jiemi(vqq_access_token)
            #print('vqq_vusession加密后:'+vqq_vusession1 )
            url0 = auth_url + '&type=qq&g_tk=&g_vstk=' + \
                vqq_vusession1+'&g_actk='+g_actk+'&_=' + str(this_time)
            # print(url0)
            res = s.get(url0, headers=headers).text
            # print('访问结果1：'+res)
            new_vus = re.search(r'vusession":"(.*?)","', res).group(1)
            cookie2 = cookie1.replace(vqq_vusession, new_vus)
            new_cookie_list.append(cookie2)
        except Exception:
            # print('cookie更新失败【'+vqq_vuserid+'】，跳过。')
            print('签到失败')
            continue

    return new_cookie_list


def start():
    try:
        # 加载推送功能
        load_send()
        # for ck_new in ck:
        #     print(ck_new)

        # print(os.getenv('QYWX_VIDEO'))
        # send('11111','2222222222')
        # exit()
#
        s = requests.session()
        # 获取ck
        cookie1_list = ck

        this_time = int(round(time.time() * 1000))

        login_url = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2&_=' + \
            str(this_time)

        new_cookie_list = renew_cookie(cookie1_list)

        for new_cookie_one in new_cookie_list:
            cookie2 = new_cookie_one
            headers2 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36',
                'referer': 'https://v.qq.com/',
                'Cookie': cookie2
            }

            # 签到
            res2 = s.get(login_url, headers=headers2).text

            cookies_arr = cookie2.split('; ')
            for cookie in cookies_arr:
                c1 = cookie.split('=')
                if c1[0] == 'o_cookie':
                    user_name = c1[1]
            # print('签到结果：'+res2)
            send("腾讯视频-" + user_name + '-'+time.strftime('%Y.%m.%d %H:%M:%S',
                                                         time.localtime(time.time()))+"-签到结果：", res2)

    except Exception as e:
        # print("地址访问失败，通知SERVER酱！")
        print(e)
        send('腾讯视频自动签到失败', '腾讯视频自动签到失败~'+time.strftime('%Y.%m.%d %H:%M:%S',
                                                       time.localtime(time.time())) + '&desp='+'异常代码：\n'+str(e))


def main_handler(event, context):
    return start()


def load_send() -> None:
    logger.info("加载推送功能中...")
    global send
    send = None
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/notify_myself.py"):
        try:
            from notify_myself import send
        except Exception:
            send = None
            logger.info(f"❌加载通知服务失败!!!\n{traceback.format_exc()}")


if __name__ == '__main__':
    start()
