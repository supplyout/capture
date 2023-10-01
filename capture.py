# encoding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pyautogui
import os
import shutil
import struct
import socket
import binascii
import scapy
from scapy.all import *

total_packets = []

js = "window.open('{}','_blank');"


def del_dir(path):
    shutil.rmtree(path)


def search_file(path, new_path, count):
    for textile in os.listdir(path):
        if textile.find('chrome') != -1:
            if os.path.getsize(path + '/' + textile) > 50000:
                print(path + '/' + textile, os.path.getsize(path + '/' + textile))
                shutil.copy(path + '/' + textile, new_path + '/' + str(count) + '.pcap')


def get_dir(path):
    import os
    dir_list = []
    for defile in os.listdir(path):
        if os.path.isdir(path + '/' + defile):
            dir_list.append(defile)
    return dir_list


def read_txt(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    return [line.strip('\n').strip('\r').strip('\t').strip(' ').strip('\n').strip('\r').strip('\t').strip(' ') for line
            in lines]


'''
随机选择列表中的5个元素
'''


def random_select(list):
    import random
    if len(list) < 5:
        return list
    else:
        return random.sample(list, 5)


conf = {"conf", "connect", "css", "html", "imgs", "js"}

urls = ["blog.csdn.net"]

back_urls = read_txt("webpages.txt")
print(back_urls)
num = 0
user_data_dir = r'--user-data-dir=C:\Users\lenovo\AppData\Local\Google\Chrome\User Data\Default'

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument(user_data_dir)
# 这个是绝对路径配置webdriver
s = Service(executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe")
browser = webdriver.Chrome(service=s, options=options)

# 设置窗口大小
browser.set_window_rect(0, 0, 1500, 800)
# 清理缓存的代码
browser.get("chrome://settings/clearBrowserData")
# 2S 等待时间
time.sleep(5)
clearButton = browser.execute_script("return document.querySelector('settings-ui').shadowRoot.querySelector("
                                     "'settings-main').shadowRoot.querySelector("
                                     "'settings-basic-page').shadowRoot.querySelector('settings-section > "
                                     "settings-privacy-page').shadowRoot.querySelector("
                                     "'settings-clear-browsing-data-dialog').shadowRoot.querySelector("
                                     "'#clearBrowsingDataDialog').querySelector('#clearBrowsingDataConfirm')")
clearButton.click()
time.sleep(3)

browser.close()
browser.quit()
# 捕包 每个网页捕包15次
count = 442

def CallBack(packet):
    if packet.haslayer('TCP'):
        print(packet['IP'].src)
        print(packet['IP'].dst)
        print(packet['TCP'].sport)
        print(packet['TCP'].dport)
        print(packet['TCP'].seq)
        print(packet['TCP'].dataofs)
        total_packets.append(packet)

def ooosniff(e):
    p_filter = "tcp"
    a = sniff(filter=p_filter, prn=CallBack, iface='WLAN',stop_filter=lambda p: e.is_set(),count=0)
    print("已停止，共捕获包", a)


for url in back_urls:
    for i in range(0, 15):
        print(num, url)
        num = num + 1
        user_data_dir = r'--user-data-dir=C:\Users\lenovo\AppData\Local\Google\Chrome\User Data\Default'
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        options.add_argument(user_data_dir)
        # 这个是绝对路径配置webdriver
        s = Service(executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe")
        browser = webdriver.Chrome(service=s, options=options)
        # 设置窗口大小
        browser.set_window_rect(0, 0, 1700, 1000)
        # 清理缓存的代码

        time.sleep(5)
        # 打开页面
        e = threading.Event()
        t = threading.Thread(target=ooosniff, args=(e,))
        t.start()
        time.sleep(1)
        try:
            browser.get('https://' + url)
        except:
            print('nonononononononohttps')
            pass
        time.sleep(15)
        e.set()
        t.join()

        browser.get("chrome://settings/clearBrowserData")
        # 2S 等待时间
        time.sleep(3)
        clearButton = browser.execute_script("return document.querySelector('settings-ui').shadowRoot.querySelector("
                                             "'settings-main').shadowRoot.querySelector("
                                             "'settings-basic-page').shadowRoot.querySelector('settings-section > "
                                             "settings-privacy-page').shadowRoot.querySelector("
                                             "'settings-clear-browsing-data-dialog').shadowRoot.querySelector("
                                             "'#clearBrowsingDataDialog').querySelector('#clearBrowsingDataConfirm')")
        clearButton.click()
        time.sleep(1)

        browser.close()

        browser.quit()
        time.sleep(1)
        command = 'ipconfig /flushdns'
        print(command)
        os.system(command)

        # print os.path.getsize("C:/Users/lenovo/Desktop/openQPA/2022-02-04-07-23-31/chrome.exe_19692.pcap")
        if not os.path.exists("D:/pcap/" + str(count)):
            os.mkdir("D:/pcap/" + str(count))
        wrpcap('D:/pcap/'+str(count)+'/'+str(i+1)+'.pcap', total_packets)
        total_packets = []
        time.sleep(2)
    count = count + 1

time.sleep(10)
browser.quit()
