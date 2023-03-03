from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pdb

def get_comment():
    # ***********关键行***********
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 这里是Chrom驱动器的exe文件
    web = webdriver.Chrome(service=Service('D:/Anaconda/envs/pythonProject/chromedriver.exe'), options=option)
    # ***********关键行结束***********

    # 抖音
    web.get('https://www.douyin.com/discover')
    # 人工调试,直到打开视频评论为止,按 c 键
    pdb.set_trace()
  
    while(1):
        data = web.find_elements(By.CLASS_NAME,'VD5Aa1A1')
        with open('douyin_comment2.txt','a+',encoding='utf-8') as f:
            for span in data:
                f.write(span.text)
                f.write('\n')
                # print(span.text)
        print('写入完成！')
        # 打开另一个视频, 按 c 键
        pdb.set_trace()


if __name__ == '__main__':
    get_comment()
