# import pandas as pd
# from collections import Counter
# import re
# import jieba
# import jieba.posseg as pseg
# import json
#
# from django.conf.urls.static import static
# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import render
# import os
# import requests
# import xml.etree.ElementTree as ET
# from django.views.decorators.csrf import csrf_exempt
# import yt_dlp as ydl
#
# from djangoProject1 import settings
# from djangoProject1.settings import BASE_DIR
# from pathlib import Path
#
#
# # 抓取Bilibili弹幕的函数
# def fetch_danmaku_data(video_url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
#     response = requests.get(video_url, headers=headers)
#     response.encoding = 'utf-8'
#     html_content = response.text
#
#     cid_start = html_content.find('"cid":') + len('"cid":')
#     cid_end = html_content.find(',', cid_start)
#     cid = html_content[cid_start:cid_end].strip()
#
#     if not cid.isdigit():
#         raise ValueError("无法提取有效的cid")
#
#     danmaku_url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
#     danmaku_response = requests.get(danmaku_url, headers=headers)
#     danmaku_response.encoding = 'utf-8'
#     danmaku_xml = danmaku_response.text
#
#     try:
#         root = ET.fromstring(danmaku_xml)
#         danmaku_list = [d.text for d in root.findall('.//d')]
#         return danmaku_list
#     except ET.ParseError as e:
#         raise ValueError(f"解析XML数据时出错: {e}")
#
# # 处理弹幕文本的高频词函数
# def process_text(danmaku_list):
#     texts = pd.Series(danmaku_list).astype(str)
#     all_text = ' '.join(texts)
#
#     cleaned_text = re.sub(r'[^\w\s]', '', all_text)
#     cleaned_text = re.sub(r'\d+', '', cleaned_text)
#     cleaned_text = cleaned_text.lower()
#
#     words = pseg.cut(cleaned_text)
#     words = [word for word, flag in words if flag.startswith('n') and len(word) > 2]
#
#     word_counts = Counter(words)
#     most_common_words = word_counts.most_common(5)
#
#     high_freq_data = {
#         'words': [word for word, _ in most_common_words],
#         'counts': [count for _, count in most_common_words]
#     }
#
#     return high_freq_data
#
#
#
# @csrf_exempt  # 如果使用POST请求，需要禁用CSRF保护（建议仅在开发环境中使用）
# def get_high_freq_data(request):
#     if request.method == 'POST':
#         body = json.loads(request.body)  # 解析请求体
#         video_url = body.get('danmaku')  # 从请求中获取URL
#         try:
#             danmaku_list = fetch_danmaku_data(video_url)  # 使用传入的URL获取弹幕
#             high_freq_data = process_text(danmaku_list)
#             return JsonResponse(high_freq_data)
#         except ValueError as e:
#             return HttpResponse(str(e), status=400)
#
#
# cookie_file_path = BASE_DIR / 'cookie' / 'cookie.txt'
# def download_video(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         url = data.get('url')
#
#         if url:
#             ydl_opts = {
#                 'http_headers': {
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
#                 },
#                 'format': 'bestvideo[height<=720]+bestaudio/best',
#                 'outtmpl': 'downloaded_video.%(ext)s',
#                 'cookiefile': str(cookie_file_path),
#                 'verbose': True,
#             }
#
#             try:
#                 with ydl.YoutubeDL(ydl_opts) as downloader:
#                     downloader.download([url])
#                 return HttpResponse("视频下载完成！")
#             except Exception as e:
#                 return HttpResponse(f"视频下载失败：{e}")
#         return HttpResponse("无效的 URL！")
#
#
#
# # @csrf_exempt
# # def download_video(request):
# #     if request.method == 'POST':
# #         data = json.loads(request.body)
# #         url = data.get('url')
# #
# #         if url:
# #             ydl_opts = {
# #                 'http_headers': {
# #                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
# #                 },
# #                 'format': 'bestvideo[height<=720]+bestaudio/best',
# #                 'outtmpl': str(Path(settings.BASE_DIR) / 'downloaded_video.%(ext)s'),
# #                 'cookiefile': str(cookie_file_path),
# #                 'verbose': True,
# #             }
# #
# #             try:
# #                 print(str(Path(settings.BASE_DIR)))  # 在下载后打印路径
# #                 with ydl.YoutubeDL(ydl_opts) as downloader:
# #                     downloader.download([url])
# #                 # 返回视频文件的路径
# #                 return JsonResponse({"message": "视频下载完成！", "file_path": "/downloaded_video.mp4"})
# #             except Exception as e:
# #                 return HttpResponse(f"视频下载失败：{e}")
# #         return HttpResponse("无效的 URL！")
# #
# #     return HttpResponse('Invalid request method. Please use POST.', status=405)
#
# # @csrf_exempt
# # def download_video(request):
# #     if request.method == 'POST':
# #         data = json.loads(request.body)
# #         url = data.get('url')
# #
# #         if url:
# #             ydl_opts = {
# #                 'http_headers': {
# #                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
# #                 },
# #                 'format': 'bestvideo[height<=720]+bestaudio/best',
# #                 'outtmpl': str(Path(settings.BASE_DIR) / 'downloaded_video.%(ext)s'),
# #                 'cookiefile': str(cookie_file_path),
# #                 'verbose': True,
# #             }
# #             try:
# #                 with ydl.YoutubeDL(ydl_opts) as downloader:
# #                     downloader.download([url])
# #                 return JsonResponse({"message": "视频下载完成！", "file_path": f"/downloaded_video.mp4"})
# #             except Exception as e:
# #                 return JsonResponse({"error": f"视频下载失败：{e}"}, status=400)
# #         return JsonResponse({"error": "无效的 URL！"}, status=400)
#
# # 上是完整逻辑代码，下是gpt测试
#
# def index(request):
#     return render(request, 'index.html')
# #
# #下方为最新
# ######整合测试######
import threading
from gzip import WRITE

import pandas as pd
from collections import Counter
import re
import jieba
import jieba.posseg as pseg
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import os
import requests
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
import yt_dlp as ydl
from urllib3 import request

from djangoProject1.settings import BASE_DIR
from collections import defaultdict
import pygame
import random
import re
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 抓取Bilibili弹幕的函数
def fetch_danmaku_data(video_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(video_url, headers=headers,verify=False)
    response.encoding = 'utf-8'
    html_content = response.text

    cid_start = html_content.find('"cid":') + len('"cid":')
    cid_end = html_content.find(',', cid_start)
    cid = html_content[cid_start:cid_end].strip()

    if not cid.isdigit():
        raise ValueError("无法提取有效的cid")

    danmaku_url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
    danmaku_response = requests.get(danmaku_url, headers=headers)
    danmaku_response.encoding = 'utf-8'
    danmaku_xml = danmaku_response.text

    try:
        root = ET.fromstring(danmaku_xml)
        danmaku_list = [(float(d.attrib['p'].split(',')[0]), d.text) for d in root.findall('.//d')]
        return danmaku_list
    except ET.ParseError as e:
        raise ValueError(f"解析XML数据时出错: {e}")


# 处理弹幕文本的高频词函数
# def process_text(danmaku_list):
#     texts = pd.Series([d[1] for d in danmaku_list]).astype(str)
#     all_text = ' '.join(texts)
#
#     cleaned_text = re.sub(r'[^\w\s]', '', all_text)
#     cleaned_text = re.sub(r'\d+', '', cleaned_text)
#     cleaned_text = cleaned_text.lower()
#
#     words = pseg.cut(cleaned_text)
#     words = [word for word, flag in words if len(word) > 2]
#
#     word_counts = Counter(words)
#     most_common_words = word_counts.most_common(5)
#
#     high_freq_data = {
#         'words': [word for word, _ in most_common_words],
#         'counts': [count for _, count in most_common_words]
#     }
#
#     return high_freq_data
# 使用jieba库进行词性划分后，大量数据被忽视，导致结果有误
# 下面是重构的方法，仅使用jieba库进行词的划分
def process_text(danmaku_list):
    texts = pd.Series([d[1] for d in danmaku_list]).astype(str)
    all_text = ' '.join(texts)

    # 保留中文字符的清洗步骤
    cleaned_text = re.sub(r'[^\u4e00-\u9fa5]', '', all_text)

    # 直接使用 jieba.cut 进行分词，去掉词性标注的过程
    words = jieba.cut(cleaned_text)
    words = [word for word in words if len(word) >=2]

    word_counts = Counter(words)
    most_common_words = word_counts.most_common(5)

    high_freq_data = {
        'words': [word for word, _ in most_common_words],
        'counts': [count for _, count in most_common_words]
    }

    return high_freq_data

# def calculate_max_danmaku(danmaku_times):
#     danmaku_times = [int(time) for time in danmaku_times]
#
#     time_counts = Counter()
#     for time in danmaku_times:
#         for offset in range(3):
#             time_counts[time + offset] += 1
#
#     most_common_time = time_counts.most_common(1)[0]
#     start_time = most_common_time[0]
#     end_time = start_time + 3
#
#     return start_time, end_time, most_common_time[1]
# 使用窗体中的弹幕计算，会造成计算时大量弹幕缺失
# 下面改为直接用发送时间统计
def calculate_max_danmaku(danmaku_times):
    # 将弹幕时间戳四舍五入为整数秒
    rounded_times = [round(float(time)) for time in danmaku_times]

    # 创建一个字典来统计每个时间点的弹幕数量
    time_counts = Counter(rounded_times)

    # 记录最大弹幕量和对应的时间段
    max_count = 0
    start_time = 0
    end_time = 0

    # 遍历每个弹幕时间，检查包含该时间的 3 秒窗口内的总弹幕数量
    for time in time_counts.keys():
        # 计算以 time 为起点的 3 秒窗口内的弹幕数量
        window_count = sum(time_counts.get(time + offset, 0) for offset in range(3))

        # 更新最大弹幕量和对应时间段
        if window_count > max_count:
            max_count = window_count
            start_time = time
            end_time = time + 2  # 3秒窗口，所以时间段为 [time, time+2]

    return start_time, end_time, max_count


@csrf_exempt
def get_high_freq_data(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        video_url = body.get('danmaku')
        try:
            danmaku_list = fetch_danmaku_data(video_url)
            high_freq_data = process_text(danmaku_list)
            return JsonResponse(high_freq_data)
        except ValueError as e:
            return HttpResponse(str(e), status=400)


@csrf_exempt
def get_max_danmaku(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        video_url = body.get('danmaku')
        try:
            danmaku_list = fetch_danmaku_data(video_url)
            danmaku_times = [d[0] for d in danmaku_list]
            start_time, end_time, count = calculate_max_danmaku(danmaku_times)
            result = {
                'start_time': start_time,
                'end_time': end_time,
                'count': count
            }
            return JsonResponse(result)
        except ValueError as e:
            return HttpResponse(str(e), status=400)

# # # # # 可用接口
# 使用户可以使用自己的cookie，防止被限制访问
# def your_cookie(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         cookie = data.get('cookie')
#     with open('cookie.txt', 'w', encoding='utf-8') as file:
#         file.write(cookie)


cookie_file_path = BASE_DIR / 'cookie' / 'cookie.txt'

# 清空download文件夹实现改文件夹中视频更新
def delete_downloaded_video():
    folder_path = 'download'
    file_name = 'downloaded_video.mp4'
    file_path = os.path.join(folder_path, file_name)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"文件 {file_name} 已成功删除。")
        else:
            print(f"文件 {file_name} 不存在。")
    except Exception as e:
        print(f"删除文件时出错：{e}")

def new_video_name(url):
    return url.split("video/")[1].split("/?")[0]

@csrf_exempt
def download_video(request):
    try:
        delete_downloaded_video()
    except Exception as e:
        print("未找到下载视频")
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        if url:
            video_name = new_video_name(url)
            ydl_opts = {
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
                },
                'format': 'bestvideo[height<=720]+bestaudio/best',
                # 'outtmpl': 'downloaded_video.%(ext)s',
                # 保存地址到下一级文件夹内
                # 'outtmpl': f'download/downloaded_video.mp4',
                # 可配合delete_downloaded_video方法实现更新
                # 'outtmpl': 'download/%(url[-3:])s.%(ext)s',
                # 错误：截取url最后三位作为文件名，截取到的内容与前端地址栏中显示的不符
                # 'outtmpl': 'download/%(video_name)s.%(ext)s',
                # 错误：无法直接使用
                'outtmpl': f'download/{video_name}.%(ext)s',
                # 成功：以video/后截取，便于前端也可以简单获取
                'cookiefile': str(cookie_file_path),
                'verbose': True,
            }

            def run_game_thread():
                run_pygame_game()
            # 获取到该接口的触发，同时触发游戏接口
            game_thread = threading.Thread(target=run_game_thread)
            game_thread.start()

            try:
                with ydl.YoutubeDL(ydl_opts) as downloader:
                    downloader.download([url])
                return HttpResponse("视频下载完成！")

            except Exception as e:
                return HttpResponse(f"视频下载失败：{e}")
        return HttpResponse("无效的 URL！")

def run_pygame_game():
    pygame.init()

    # 窗体大小
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DLW Game")

    # 颜色
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # 玩家类
    class Player:
        def __init__(self):
            self.x = 50
            self.y = 150
            self.width = 20
            self.height = 20
            self.dy = 0
            # 下落速度；值越大落越快
            self.gravity = 0.6
            # 跳跃高度；值越小跳越高
            self.jump_power = -10
            self.grounded = False

        def jump(self):
            if self.grounded:
                self.dy = self.jump_power
                self.grounded = False

        def update(self):
            self.y += self.dy
            if self.y + self.height < SCREEN_HEIGHT:
                self.dy += self.gravity
            else:
                self.y = SCREEN_HEIGHT - self.height
                self.dy = 0
                self.grounded = True

        def draw(self, screen):
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

    # 障碍物类
    class Obstacle:
        def __init__(self):
            self.x = SCREEN_WIDTH
            self.y = SCREEN_HEIGHT - random.randint(20, 60)
            self.width = 20
            self.height = random.randint(20, 40)

        def update(self):
            self.x -= game_speed

        def draw(self, screen):
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    # 初始化
    play = Player()
    obstacles = []
    game_speed = 5
    score = 0
    clock = pygame.time.Clock()
    game_over = False

    # # 设置字体，但仍然使用不了中文
    try:
        font = pygame.font.Font('msyh.ttc', 48)  # 微软雅黑字体
    except:
        font = pygame.font.Font(None, 48)  # 默认字体

    # 游戏循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #     监听点击，点击replay重置游戏界面，否则触发跳跃方法
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    mouse_x, mouse_y = event.pos
                    # 检查是否点击了“Replay”按钮
                    if replay_button.collidepoint(mouse_x, mouse_y):
                        # 重置游戏状态
                        game_over = False
                        play = Player()
                        obstacles = []
                        score = 0
                else:
                    play.jump()

        if not game_over:
            play.update()

            # 生成障碍物，随机生成障碍物,1/0.01*帧数
            if random.random() < 0.01:
                obstacles.append(Obstacle())

            # 刷新碍物
            for obstacle in obstacles:
                obstacle.update()
                if obstacle.x + obstacle.width < 0:
                    obstacles.remove(obstacle)
                    score += 1

                # 碰撞逻辑,玩家角色与障碍物出现重叠为碰撞
                if (play.x < obstacle.x + obstacle.width and
                    play.x + play.width > obstacle.x and
                    play.y < obstacle.y + obstacle.height and
                    play.y + play.height > obstacle.y):
                    game_over = True

            # 绘制
            screen.fill(WHITE)
            play.draw(screen)
            for obstacle in obstacles:
                obstacle.draw(screen)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            pygame.display.flip()

        if game_over:
            # 重新游戏按钮
            screen.fill(WHITE)
            text = font.render("Replay?", True, BLACK)
            replay_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100)
            pygame.draw.rect(screen, RED, replay_button)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()

        clock.tick(30)
    pygame.quit()


def index(request):
    return render(request, 'index.html')

def write_error_log(message):
    with open("video_errorlist.txt", "a") as file:
        file.write(message + "\n")


@csrf_exempt
def download_excel(request):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76",
        "Referer": "https://www.bilibili.com/",  # 设置防盗链
    }
    new_wb = Workbook()
    new_ws = new_wb.active
    new_ws.append(
        ["标题", "链接", "up主", "up主id", "精确播放数", "历史累计弹幕数", "点赞数", "投硬币枚数", "收藏人数",
         "转发人数",
         "发布时间", "视频时长(秒)", "视频简介", "作者简介", "标签", "视频aid"])
    output_folder = "./download"
    output_file = os.path.join(output_folder, "output.xlsx")
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        try:
            response = requests.get(url=url, headers=header,verify=False)
            soup = BeautifulSoup(response.text, "html.parser")

            # 视频 aid、视频时长和作者 id
            initial_state_script = soup.find(string=re.compile("window.__INITIAL_STATE__"))
            initial_state_text = initial_state_script.string

            author_id_pattern = re.compile(r'"mid":(\d+)')
            video_aid_pattern = re.compile(r'"aid":(\d+)')
            video_duration_pattern = re.compile(r'"duration":(\d+)')

            author_id = author_id_pattern.search(initial_state_text).group(1)
            video_aid = video_aid_pattern.search(initial_state_text).group(1)
            video_duration_raw = int(video_duration_pattern.search(initial_state_text).group(1))
            video_duration = video_duration_raw - 2

            # 提取标题
            title_raw = soup.find("title").text
            title = re.sub(r"_哔哩哔哩_bilibili", "", title_raw).strip()

            # 提取标签
            keywords_content = soup.find("meta", itemprop="keywords")["content"]
            content_without_title = keywords_content.replace(title + ',', '')
            keywords_list = content_without_title.split(',')
            tags = ",".join(keywords_list[:-4])

            meta_description = soup.find("meta", itemprop="description")["content"]
            numbers = re.findall(
                r'[\s\S]*?视频播放量 (\d+)、弹幕量 (\d+)、点赞数 (\d+)、投硬币枚数 (\d+)、收藏人数 (\d+)、转发人数 (\d+)',
                meta_description)

            # 提取作者
            author_search = re.search(r"视频作者\s*([^,]+)", meta_description)
            if author_search:
                author = author_search.group(1).strip()
            else:
                author = "未找到作者"

            # 提取作者简介
            author_desc_pattern = re.compile(r'作者简介 (.+?),')
            author_desc_match = author_desc_pattern.search(meta_description)
            if author_desc_match:
                author_desc = author_desc_match.group(1)
            else:
                author_desc = "未找到作者简介"

            # 提取视频简介
            meta_parts = re.split(r',\s*', meta_description)
            if meta_parts:
                video_desc = meta_parts[0].strip()
            else:
                video_desc = "未找到视频简介"

            if numbers:
                views, danmaku, likes, coins, favorites, shares = [int(n) for n in numbers[0]]
                publish_date = soup.find("meta", itemprop="uploadDate")["content"]
                new_ws.append(
                    [title, url, author, author_id, views, danmaku, likes, coins, favorites, shares, publish_date,
                     video_duration, video_desc, author_desc, tags, video_aid])
                print(f"视频{url}已完成爬取")

            else:
                print(f"视频 {url}未找到相关数据，可能为分集视频")
                return HttpResponse("Excel未找到相关数据！")

        except Exception as e:
            write_error_log(f"视频发生错误：{e}")
            print(f"发生错误，已记录到错误日志:出错数据为{url}")
            return HttpResponse("无效的 URL！")

    new_wb.save(output_file)
    return HttpResponse("Excel下载完成！")
