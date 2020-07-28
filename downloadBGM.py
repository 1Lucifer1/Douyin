import json
import requests
import os

def get_url():
    # 打开存放有BGM地址的json文件
    json_file = open('./statistics3735-4515.json', encoding='utf-8')
    # 打开用来写入BGM地址的txt文件
    music_file = open('./music3735-4515.txt', mode='a')
    json_str = json_file.read()
    json_list = json.loads(json_str)
    for record in json_list:
        try:
            music_url = record['music_addr'][0]
        except IndexError:
            # 用于列出没有BGM地址的视频
            print(record['video_vid'])
        else:
            # 将BGM地址写入txt
            music_file.write(music_url)
            music_file.write('\n')

    json_file.close()

def download():
    url_file = open('./music3735-4515.txt', encoding='utf-8')
    url_list = url_file.readlines()
    k = 3735
    for url in url_list:
        try:
            url = url.replace('\n', '')
            res = requests.get(url, stream=True)
        except:
            print("error")
        else:
            fileName = "music" + str(k) + '.mp3'
            file_path = os.path.join('./music3735-4515', fileName)
            print('开始写入文件：', file_path)
            with open(file_path, 'wb') as fd:
                for chunk in res.iter_content():
                    fd.write(chunk)
            print(fileName + ' 成功下载！')
            k += 1
    url_file.close()

if __name__=='__main__':
    download()
    # get_url()