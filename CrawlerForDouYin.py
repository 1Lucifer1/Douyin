import requests
import json
import time,random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
class Douyin:

    def page_num(self, cursor, count):
        # 网站后随机生成的签名，经检验一个签名可以用来加载多个数据包
        random_field = 'IZ4AtAAAfpLJRCLJtb8QYyGeAK'

        #网址的主体


        url = 'https://www.iesdouyin.com/web/api/v2/challenge/aweme/?ch_id=1561238083888129&count=3&cursor=' + str(
            cursor) + \
              '&aid=1128&screen_limit=3&download_click_limit=0&_signature=' + random_field

        #请求头

        headers = {

            'user-agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',

        }

        response = requests.get(url, headers=headers).text

        #转换成json数据

        resp = json.loads(response)

        #遍历

        for data in resp["aweme_list"]:
            # id值

            video_id = data['aweme_id']

            # 视频简介

            video_title = data['desc']

            # 构造视频网址

            video_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + video_id

            video_response = requests.get(video_url, headers=headers).text

            video_resp = json.loads(video_response)


            for video_data in video_resp["item_list"]:
                video_dict={}

                # 获取视频创作者

                video_dict['video_author'] = video_data['author']['nickname']

                # 获取视频描述

                video_dict['video_desc'] = video_data['desc']

                video_dict['video_aweme_id'] = video_data['statistics']['aweme_id']

                # 获取视频评论量

                video_dict['comment_count'] = video_data['statistics']['comment_count']

                # 获取视频点赞量

                video_dict['digg_count'] = video_data['statistics']['digg_count']

                # 获取视频下载地址

                video_dict['video_addr'] = video_data['video']['play_addr']['url_list'][0]

                # 获取BGM下载地址

                video_dict['music_addr'] = video_data['music']['play_url']['url_list']

                video_dict['video_vid'] = video_data['video']['vid']

                # 将字典转换为json字符串

                json_str = json.dumps(video_dict, indent=2, sort_keys=True, ensure_ascii=False)
                count += 1

                # 将获取的数据存储到json文件中

                with open('./statistics.json', 'a', encoding='utf-8', newline=None) as json_file:
                    json_file.write('\n'+json_str+',')

        # 每次爬取999个视频

        if count >= 999:
            return 1
        else:
            # 每个数据包最多只含9个视频，加载下一个数据包
            douyin.page_num(cursor+9, count)
            return
if __name__ == '__main__':

     douyin = Douyin()

     douyin.page_num(0,0)