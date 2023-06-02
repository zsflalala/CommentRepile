import jieba
import stylecloud
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def Cloud():
    with open('new_file.txt','r',encoding='utf-8') as f:
        word_list = jieba.cut(f.read())
        result = " ".join(word_list) #分词用空格隔开
        
    stylecloud.gen_stylecloud(
        text=result, # 上面分词的结果作为文本传给text参数
        size=512,
        font_path='msyh.ttc', # 字体设置
        palette='cartocolors.qualitative.Pastel_7', # 调色方案选取，从palettable里选择
        gradient='horizontal', # 渐变色方向选了垂直方向
        icon_name='fab fa-weixin',  # 蒙版选取，从Font Awesome里选
        output_name='test_ciyun.png') # 输出词云图


def Cloud2():
    
    mask = np.array(Image.open("dance.png"))
    with open('new_file.txt','r',encoding='utf-8') as f:
        word_list = jieba.cut(f.read())
        result = " ".join(word_list) #分词用空格隔开
        wordcloud = WordCloud(background_color="white",\
                        width = 800,\
                        height = 600,\
                        max_words = 200,\
                        max_font_size = 80,\
                        mask = mask,\
                        contour_width = 3,\
                        contour_color = 'steelblue'
                        ).generate(result)
        wordcloud.to_file('美团评论_词云图.png')


def Cloud3():
    # 打开文本
    with open("meituan_comment2.txt",encoding="utf-8") as f:
        s = f.read()

    # 中文分词
    text = ' '.join(jieba.cut(s)) # 生成分词列表,连接成字符串

    # 生成对象
    img = Image.open("flyHeart.png") # 打开遮罩图片
    mask = np.array(img) #将图片转换为数组

    stopwords = ["我","你","她","的","是","了","在","也","和","就","都","这","吗","@"] # 去掉不需要显示的词
    wc = WordCloud(font_path="msyh.ttc",
                mask=mask,
                width = 1000,
                height = 700,
                background_color='white',
                max_words=200,
                stopwords=stopwords).generate(text)

    # 显示词云
    plt.imshow(wc, interpolation='bilinear')# 用plt显示图片
    plt.axis("off")  # 不显示坐标轴
    plt.show() # 显示图片

    # 保存到文件
    wc.to_file("美团评论词云图2.png")

if __name__ == '__main__':
    Cloud3()