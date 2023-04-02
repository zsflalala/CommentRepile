import requests
from lxml import etree
import re
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp


# 注: 想要运行成功,首先登录美团网站,根据获得Cookie修改以下代码中Headers中Cookie值,具体看文件夹流程图
# 截至2023/4/2 美团网页美食评论页面出现故障,可能是修改页面,可能是页面崩了,暂时爬不了评论数据
# 不过已将评论数据内容url放置 meituan_url.txt 文件中,截至2023/4/2 仍能访问(网页先登录美团), 可直接运行main函数中后两步

# 初步测试如何爬取美团评论数据
def meituan_url():

    # 美团评论
    # 1.寻找poiId
    # url = 'https://bj.meituan.com/meishi/'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    #     'Cookie':'uuid=702525fd116b48578bc4.1675943406.1.0.0; _lxsdk_cuid=1863602fe4ec8-00221287d3f5ff-26021051-168000-1863602fe4eaa; WEBDFPID=3wx7944x830v5y120vy65zwyu72046288136397u9z3979583724v7z3-1991303412282-1675943411504SICWEKWfd79fef3d01d5e9aadc18ccd4d0c95074238; ci=1; rvct=1; client-id=0d2945ed-68f2-413d-b85c-b20b0037249f; mtcdn=K; _hc.v=f708e0ca-90c8-32f8-309f-2dbe356faf69.1675943516; iuuid=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; _lxsdk=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; IJSESSIONID=node0eipfnxkad9ml137lduez07smu12501051; cityname=%E5%8C%97%E4%BA%AC; userTicket=FHjqZLRdtNLYdnFTFEbEFiKMPEnFczUaBxUcawiV; lat=39.729356; lng=116.12302; n=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; qruuid=888bb86a-c2da-4c83-8a8b-e7bf0a727716; token2=AgEcIgjsW2FFtJ8T48MbsNk7LOpV8ZtCNvjT4x9Ohd-7sCA_mIxG2hcnzwS9fTaPnoF3593VA2b2HQAAAACMFgAAFxDr9VjmrgIN5KHiOkEh05O6XK8A1eJ2NE2LdwY_vmPNlQgPx7Kx8Am9X_DnhwBC; oops=AgEcIgjsW2FFtJ8T48MbsNk7LOpV8ZtCNvjT4x9Ohd-7sCA_mIxG2hcnzwS9fTaPnoF3593VA2b2HQAAAACMFgAAFxDr9VjmrgIN5KHiOkEh05O6XK8A1eJ2NE2LdwY_vmPNlQgPx7Kx8Am9X_DnhwBC; lt=AgEcIgjsW2FFtJ8T48MbsNk7LOpV8ZtCNvjT4x9Ohd-7sCA_mIxG2hcnzwS9fTaPnoF3593VA2b2HQAAAACMFgAAFxDr9VjmrgIN5KHiOkEh05O6XK8A1eJ2NE2LdwY_vmPNlQgPx7Kx8Am9X_DnhwBC; u=3352525637; unc=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; __mta=145128971.1675943418903.1676029115023.1676029267470.17; firstTime=1676029273969; _lxsdk_s=1863b1e20d5-0e1-585-c0b%7C%7C49'
    # }
    # session = requests.Session()
    # response = session.get(url=url,headers=headers).text
    # with open("meituan.html",'w',encoding='utf-8') as f:
    #     f.write(response)

    # 2.利用正则保存商家poiId
    # fp = open('./meituan.html','r',encoding='utf-8').read()
    # ex = '"poiId":(.*?),"frontImg"'
    # poiId = re.findall(ex,fp)
    # print(poiId)

    # 3.获得li标签中的originUrl
    # ex = '<a class="" href="(.*?)" data-reactid='
    # info = re.findall(ex,fp)
    # 处理
    # originUrl = [i for i in info if (i.startswith('http:') and i.endswith('/'))]
    # print(len(originUrl))
    # print(originUrl)
    
    # originUrl = ['http://bj.meituan.com/meishi/c393/', 'http://bj.meituan.com/meishi/c11/', 'http://bj.meituan.com/meishi/c17/', 'http://bj.meituan.com/meishi/c40/', 'http://bj.meituan.com/meishi/c36/', 'http://bj.meituan.com/meishi/c28/', 'http://bj.meituan.com/meishi/c35/', 'http://bj.meituan.com/meishi/c395/', 'http://bj.meituan.com/meishi/c54/', 'http://bj.meituan.com/meishi/c20003/', 'http://bj.meituan.com/meishi/c55/', 'http://bj.meituan.com/meishi/c56/', 'http://bj.meituan.com/meishi/c20004/', 'http://bj.meituan.com/meishi/c57/', 'http://bj.meituan.com/meishi/c400/', 'http://bj.meituan.com/meishi/c58/', 'http://bj.meituan.com/meishi/c41/', 'http://bj.meituan.com/meishi/c60/', 'http://bj.meituan.com/meishi/c62/', 'http://bj.meituan.com/meishi/c63/', 'http://bj.meituan.com/meishi/c217/', 'http://bj.meituan.com/meishi/c227/', 'http://bj.meituan.com/meishi/c228/', 'http://bj.meituan.com/meishi/c229/', 'http://bj.meituan.com/meishi/c232/', 'http://bj.meituan.com/meishi/c233/', 'http://bj.meituan.com/meishi/c24/', 'http://bj.meituan.com/meishi/c59/']

    # 4.获得类别cateId
    # cateId = []
    # for Url in originUrl:
    #     cateId.append(Url.split('/')[-2][1:])
    # print(cateId)

    # 5.拼接poiId,获得评论的url
    # url = f'https://bj.meituan.com/meishi/api/poi/getMerchantComment?uuid=702525fd116b48578bc4.1675943406.1.0.0&platform=1&partner=126&originUrl={originUrl[1]}&optimusCode=10&id={poiId[4]}&userId=3352525637&offset=0&pageSize=10&sortType=1&tag'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    #     'Cookie':'uuid=702525fd116b48578bc4.1675943406.1.0.0; _lxsdk_cuid=1863602fe4ec8-00221287d3f5ff-26021051-168000-1863602fe4eaa; WEBDFPID=3wx7944x830v5y120vy65zwyu72046288136397u9z3979583724v7z3-1991303412282-1675943411504SICWEKWfd79fef3d01d5e9aadc18ccd4d0c95074238; ci=1; rvct=1; client-id=0d2945ed-68f2-413d-b85c-b20b0037249f; mtcdn=K; _hc.v=f708e0ca-90c8-32f8-309f-2dbe356faf69.1675943516; iuuid=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; _lxsdk=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; IJSESSIONID=node0eipfnxkad9ml137lduez07smu12501051; cityname=%E5%8C%97%E4%BA%AC; userTicket=FHjqZLRdtNLYdnFTFEbEFiKMPEnFczUaBxUcawiV; lat=39.729356; lng=116.12302; n=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; qruuid=888bb86a-c2da-4c83-8a8b-e7bf0a727716; token2=AgEcIgjsW2FFtJ8T48MbsNk7LOpV8ZtCNvjT4x9Ohd-7sCA_mIxG2hcnzwS9fTaPnoF3593VA2b2HQAAAACMFgAAFxDr9VjmrgIN5KHiOkEh05O6XK8A1eJ2NE2LdwY_vmPNlQgPx7Kx8Am9X_DnhwBC; oops=AgEcIgjsW2FFtJ8T48MbsNk7LOpV8ZtCNvjT4x9Ohd-7sCA_mIxG2hcnzwS9fTaPnoF3593VA2b2HQAAAACMFgAAFxDr9VjmrgIN5KHiOkEh05O6XK8A1eJ2NE2LdwY_vmPNlQgPx7Kx8Am9X_DnhwBC; lt=AgEcIgjsW2FFtJ8T48MbsNk7LOpV8ZtCNvjT4x9Ohd-7sCA_mIxG2hcnzwS9fTaPnoF3593VA2b2HQAAAACMFgAAFxDr9VjmrgIN5KHiOkEh05O6XK8A1eJ2NE2LdwY_vmPNlQgPx7Kx8Am9X_DnhwBC; u=3352525637; unc=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; __mta=145128971.1675943418903.1676029115023.1676029267470.17; firstTime=1676029273969; _lxsdk_s=1863b1e20d5-0e1-585-c0b%7C%7C49'
    # }
    # session = requests.Session()
    # response = session.get(url=url,headers=headers)
    # js_data = response.json()
    # comment_list = js_data['data']['comments']
    # for comment in comment_list:
    #     content = comment['comment'].replace('\n',' ')
    #     print(content)
    # with open("pinglun.html",'w',encoding='utf-8') as f:
    #     f.write(response)
    pass



    # 抖音视频
    # url = 'https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7193606175580032312&cursor=0&count=20&item_type=0&insert_ids=&rcFT=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=960&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=110.0.0.0&browser_online=true&engine_name=Blink&engine_version=110.0.0.0&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7196130140362655290&msToken=E_vHo6vTm2adsdh5TXUT2sgsqvYXKbVaAv8WIBhDCCgjYFWNjS1KsRtBJNwzVhzbJnfrWyHqZwOdDjhypFOSU22aYLj8uFW_p3Fwd01-5adfg_CXKFWVDqIWTG-XUxQ=&X-Bogus=DFSzswVY41sANcqfShBjml9WX7rz'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    #     'cookie': 'ttwid=1%7CxeBwaZXoWZnWuTa73rk8N6C7zLc0L1Zx8y88YF-dJf4%7C1675479627%7C4ce560bf28e1619c6503c587542c6b95304097a4de3d53a8b62c47dee2abe3ab; passport_csrf_token=cf2037c0f0d1c2986655da89f9cfbb83; passport_csrf_token_default=cf2037c0f0d1c2986655da89f9cfbb83; s_v_web_id=verify_ldpdba0o_tmgw2Z1U_E4A3_4DFI_8x6k_brfizr8X0lii; ttcid=9fb553b09a674788903fa3dbfbebae5428; douyin.com; AB_LOGIN_GUIDE_TIMESTAMP=%221675998141975%22; n_mh=aqBX69R0aKSmlk3OhZyvPUsNpXcw_h5h0tGvgPurixE; passport_auth_status=c48b4c05d40ded276462277eca7c951f%2C; passport_auth_status_ss=c48b4c05d40ded276462277eca7c951f%2C; _tea_utm_cache_2018=undefined; LOGIN_STATUS=1; store-region=cn-js; store-region-src=uid; csrf_session_id=88f0e5be5cf0bbcca01b8976f002fca5; d_ticket=187b4e597b7e6194313cbb08db69fb8757cac; download_guide=%223%2F20230210%22; passport_assist_user=CkHVrgCgwjS_l-DC2UlDJRbssBL-0mIQ7k5sUo2bBYeSsD_6DSTuimjIUDeccbX9SST_Qwv3dhjIIah1_ecNW5_qwxpICjxwDFNM7ereFBJGTFTiOPX7t5hyZzzrwSnNOaI2wIaaSGubVmLnZuApWW4VcZfsVdbAZu6bQzK2lea6oCwQsPeoDRiJr9ZUIgEDFuea3A%3D%3D; sso_uid_tt=87ba326758a85257a91561c8a0ffce48; sso_uid_tt_ss=87ba326758a85257a91561c8a0ffce48; toutiao_sso_user=3a4bf0fd1931ea921f454615ec1e68bf; toutiao_sso_user_ss=3a4bf0fd1931ea921f454615ec1e68bf; sid_ucp_sso_v1=1.0.0-KDE0NWIwNjJiYjZjNjQyZmVkNTBjNGNjNWE3MGFlYzQ4NjQyNjk3MjcKHwjowfDJqPT_BhCohJifBhjvMSAMMPypovkFOAJA7wcaAmxmIiAzYTRiZjBmZDE5MzFlYTkyMWY0NTQ2MTVlYzFlNjhiZg; ssid_ucp_sso_v1=1.0.0-KDE0NWIwNjJiYjZjNjQyZmVkNTBjNGNjNWE3MGFlYzQ4NjQyNjk3MjcKHwjowfDJqPT_BhCohJifBhjvMSAMMPypovkFOAJA7wcaAmxmIiAzYTRiZjBmZDE5MzFlYTkyMWY0NTQ2MTVlYzFlNjhiZg; odin_tt=4dc812f9c3f55b15cf06efc142958465d5c6dd749fdd883e7f3f9fc867e7f8cd6dcca45bebefe5c2131defe647b5f9dcdcc777fe072945ad3e111064fb30f0e2; uid_tt=44cdd04c7b3136e6e0a041830c43c819; uid_tt_ss=44cdd04c7b3136e6e0a041830c43c819; sid_tt=05d259757786d7db7ec4ad23b988fdc4; sessionid=05d259757786d7db7ec4ad23b988fdc4; sessionid_ss=05d259757786d7db7ec4ad23b988fdc4; sid_guard=05d259757786d7db7ec4ad23b988fdc4%7C1676018221%7C5183995%7CTue%2C+11-Apr-2023+08%3A36%3A56+GMT; sid_ucp_v1=1.0.0-KDUyNzhhY2Y3OGZhYWUwZjY4N2VlMmU5NDc5OTAwZGExOWJjZGZiMjAKGQjowfDJqPT_BhCthJifBhjvMSAMOAJA7wcaAmxxIiAwNWQyNTk3NTc3ODZkN2RiN2VjNGFkMjNiOTg4ZmRjNA; ssid_ucp_v1=1.0.0-KDUyNzhhY2Y3OGZhYWUwZjY4N2VlMmU5NDc5OTAwZGExOWJjZGZiMjAKGQjowfDJqPT_BhCthJifBhjvMSAMOAJA7wcaAmxxIiAwNWQyNTk3NTc3ODZkN2RiN2VjNGFkMjNiOTg4ZmRjNA; tt_scid=kKlnFm9Dy7VHBhD48RrNMHMILVVltdAl8AmwFWv06IM95LVJ34ihDyjRd-m1GKiW331e; __ac_nonce=063e634ce00f950455a25; __ac_signature=_02B4Z6wo00f01R5HoFQAAIDBnkVaFDk1JLUeZ6TAACR6sA68baqh-fEccPwGmdiMfFKJ7DbXnacu-NGAqH21bd3QuB03sichpuY1pS.On1DzMeF2ZMj2Jz1Da6gZJlVZUEw5a0KfqADUxO7Ja4; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1676635985268%2C%22type%22%3A1%7D; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAASvwUvP3haZKQpoNmfCo7ps7Wl5lakpRtrnAvgGNzJvuoVvfe-kitOZ_LT1HW5jC7%2F1676044800000%2F0%2F0%2F1676031786203%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAASvwUvP3haZKQpoNmfCo7ps7Wl5lakpRtrnAvgGNzJvuoVvfe-kitOZ_LT1HW5jC7%2F1676044800000%2F0%2F0%2F1676032386204%22; msToken=FiyzrvBFdgD7VEHRuRxStEd9ODMQU8PIN4BIhB1WTZYOX0y5HM-Kw0Nk-2iIHm3As-sCjP7AEblZLpHotAz49V6Mtyn0KCaPubl7jcoQ0NNflV8UUmSZj7PogNo15wc=; msToken=E_vHo6vTm2adsdh5TXUT2sgsqvYXKbVaAv8WIBhDCCgjYFWNjS1KsRtBJNwzVhzbJnfrWyHqZwOdDjhypFOSU22aYLj8uFW_p3Fwd01-5adfg_CXKFWVDqIWTG-XUxQ=; passport_fe_beating_status=true; home_can_add_dy_2_desktop=%221%22; strategyABtestKey=%221676031189.233%22'
    # }
    # page_text = requests.get(url=url,headers=headers).text
    # # info = re.findall('<script id="RENDER_DATA" type="application/json">(.*?) .*?',page_text)
    # print(page_text)

# 同步操作，获取美团网页北京市所有商铺评论 1646条
def getMeituan():
    CITYNAME = '北京'

    COMMENTURL = []
    basicUrl = 'https://bj.meituan.com/meishi/'
    originUrl = 'https://bj.meituan.com/meishi/c393/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie':'uuid=702525fd116b48578bc4.1675943406.1.0.0; _lxsdk_cuid=1863602fe4ec8-00221287d3f5ff-26021051-168000-1863602fe4eaa; WEBDFPID=3wx7944x830v5y120vy65zwyu72046288136397u9z3979583724v7z3-1991303412282-1675943411504SICWEKWfd79fef3d01d5e9aadc18ccd4d0c95074238; ci=1; rvct=1; client-id=0d2945ed-68f2-413d-b85c-b20b0037249f; mtcdn=K; _hc.v=f708e0ca-90c8-32f8-309f-2dbe356faf69.1675943516; iuuid=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; _lxsdk=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; IJSESSIONID=node0eipfnxkad9ml137lduez07smu12501051; cityname=%E5%8C%97%E4%BA%AC; userTicket=FHjqZLRdtNLYdnFTFEbEFiKMPEnFczUaBxUcawiV; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; lat=39.92501; lng=116.59771; qruuid=1715ed80-ab43-4740-8075-3847ff6f383f; token2=AgFnIiDzwAgXonbHpNm0jX2q0pxzuh275jpBB17foauYfJWs_pRqRvQh4ccTPMMq2qpN_jgUrkllWwAAAACMFgAABKZXTexo5bNQlw2GLf-UHdePjQbS5_ZiW8-2c4tqmb2sXiouAv0gT0zginxPwusS; oops=AgFnIiDzwAgXonbHpNm0jX2q0pxzuh275jpBB17foauYfJWs_pRqRvQh4ccTPMMq2qpN_jgUrkllWwAAAACMFgAABKZXTexo5bNQlw2GLf-UHdePjQbS5_ZiW8-2c4tqmb2sXiouAv0gT0zginxPwusS; lt=AgFnIiDzwAgXonbHpNm0jX2q0pxzuh275jpBB17foauYfJWs_pRqRvQh4ccTPMMq2qpN_jgUrkllWwAAAACMFgAABKZXTexo5bNQlw2GLf-UHdePjQbS5_ZiW8-2c4tqmb2sXiouAv0gT0zginxPwusS; u=3003462955; n=gIa130670404; unc=gIa130670404; firstTime=1676081255132; __mta=145128971.1675943418903.1676080512699.1676081255958.22; _lxsdk_s=1863e2cfb3c-63f-38c-9e6%7C%7C41'
    }
    
    session = requests.Session()
    response = session.get(url=basicUrl,headers=headers)

    ex = '<a class="" href="(.*?)" data-reactid='
    info = re.findall(ex,response.text)
    originUrl_list = [i for i in info if (i.startswith('http') and i.endswith('/'))]
    print(len(originUrl_list))

    cateId = []
    for Url in originUrl_list:
        cateId.append(Url.split('/')[-2][1:])

    for cateid in cateId:
        maxUrl = f'https://bj.meituan.com/meishi/api/poi/getPoiList?cityName={CITYNAME}&cateId={cateid}&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=3352525637&uuid=702525fd116b48578bc4.1675943406.1.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fbj.meituan.com%2Fmeishi%2Fc393%2&riskLevel=1&optimusCode=10&_token=eJxVjl9vokAUxb%2FLvEJkgCkwvtEVELZot8CobPpAYfgrKjCguNnvvtPUPmxyk3Puub%2BbnD%2BgdzOwlCHEEIpgoj1YAnkBFxoQARv4RdM1iBCC2MBPIkj%2Fz7DBnz56sgLL3%2FKTqomaYrx%2FJm88%2BEqwBt%2FFh1W4VRCfT8blCCgZuwxLSfqoFy2t2JicFum5lbgfykpKVaxKvAjgfBtynmvz0OSh7Hv3eXPODlVx4o56V1JH8mjOll9SIXiOmHAt5pA43ltMdhetQ%2BuD%2F%2BwFZnookjbaKmEeCL%2BsbYT1%2Bt7P6KRO816no9mPL6T2Jssv4Hra5H7Yl5AVkoKkCRn6j7t96tw88HVUEXap4nR3oPUYmXbskfZs3PJbbKvM2W%2FGF%2Bt1a3uoPuxpInjWOr0fbdSV2ZAFVHO7ozuRmK3IsC%2BNLLCMSGYdVgU3sUdv9%2FM4Rc5dy5JaHpLznO%2Fo9aY0DdZXVhfTrNpARVdMOWudia7WXVhWzTBuJMNyor4Bf%2F8BEFuTHg%3D%3D'
        session = requests.Session()
        response = session.get(url=maxUrl,headers=headers)
        js_data = response.json()
        totalCounts = js_data['data']['totalCounts']
        maxPage = totalCounts // 15 + 1

        for page in range(1,maxPage+1):
            maxKindUrl = originUrl + f'pn{page}/'
            session = requests.Session()
            response = session.get(url=maxKindUrl,headers=headers)

            ex = '"poiId":(.*?),"frontImg"'
            poiId = re.findall(ex,response.text)
            print(poiId)

            for poiid in poiId:
                commentUrl = f'https://bj.meituan.com/meishi/api/poi/getMerchantComment?uuid=702525fd116b48578bc4.1675943406.1.0.0&platform=1&partner=126&originUrl={originUrl}&optimusCode=10&id={poiid}&userId=3352525637&offset=0&pageSize=10&sortType=1&tag'
                if commentUrl not in COMMENTURL:
                    COMMENTURL.append(commentUrl)

    print(len(COMMENTURL))
    # with open('meituan_url.csv','w',encoding='utf-8') as f:
    #     wirter = csv.writer(f)
    #     wirter.writerow(COMMENTURL)
    for commenturl in COMMENTURL: 
        session = requests.Session()
        response = session.get(url=commenturl,headers=headers)
        js_data = response.json()
        comment_list = js_data['data']['comments']
        for comment in comment_list:
            content = comment['comment'].replace('\n',' ')
            with open('meituan_comment.txt','a+',encoding='utf-8') as f:
                f.write(content)
                f.write('\n')


# 利用线程池获取所有下载评论数据url
# 获取美团网页所有城市信息
def get_cityname():
    cityurl = 'https://www.meituan.com/changecity/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie':'_lxsdk_cuid=1863602fe4ec8-00221287d3f5ff-26021051-168000-1863602fe4eaa; WEBDFPID=3wx7944x830v5y120vy65zwyu72046288136397u9z3979583724v7z3-1991303412282-1675943411504SICWEKWfd79fef3d01d5e9aadc18ccd4d0c95074238; _hc.v=f708e0ca-90c8-32f8-309f-2dbe356faf69.1675943516; iuuid=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; _lxsdk=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; cityname=%E5%8C%97%E4%BA%AC; ci=1; rvct=1%2C140%2C382%2C10; __mta=145128971.1675943418903.1676084135258.1676104841696.24; uuid=2700efcb13bc4b01b495.1679800560.1.0.0; latlng=39.928159%2C116.301426; ci3=1; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; qruuid=2c6cdb43-d56e-47e9-b318-e0fa9f77f1b8; token2=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; oops=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; lt=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; u=3352525637; n=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; unc=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; lat=40.052377; lng=116.310177; client-id=79f01014-150a-4c33-bfec-56032a3886de; firstTime=1680436820577; _lxsdk_s=18741d40e86-4a5-b61-636%7C%7C21'
    }
    response = requests.get(url=cityurl,headers=headers)

    # with open('meituancity.txt','w',encoding='utf-8') as f:
    #     f.write(response.text)

    tree = etree.HTML(response.text)
    alphabet_city_area = tree.xpath('//*[@id="react"]/div/div[5]')[0]
    for city_area in alphabet_city_area:
        a_llist = city_area.xpath('./span[2]/a')
        for a in a_llist:
            CITYURL.append('https:' + a.xpath('./@href')[0] + '/meishi/') 
            CITYNAME.append(a.xpath('./text()')[0])
    print('所有城市列表: ',CITYNAME)

# 获取所有类别选项id
def get_cateId():
    basicUrl = 'https://bj.meituan.com/meishi/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie':'_lxsdk_cuid=1863602fe4ec8-00221287d3f5ff-26021051-168000-1863602fe4eaa; WEBDFPID=3wx7944x830v5y120vy65zwyu72046288136397u9z3979583724v7z3-1991303412282-1675943411504SICWEKWfd79fef3d01d5e9aadc18ccd4d0c95074238; _hc.v=f708e0ca-90c8-32f8-309f-2dbe356faf69.1675943516; iuuid=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; _lxsdk=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; cityname=%E5%8C%97%E4%BA%AC; ci=1; rvct=1%2C140%2C382%2C10; __mta=145128971.1675943418903.1676084135258.1676104841696.24; uuid=2700efcb13bc4b01b495.1679800560.1.0.0; latlng=39.928159%2C116.301426; ci3=1; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; qruuid=2c6cdb43-d56e-47e9-b318-e0fa9f77f1b8; token2=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; oops=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; lt=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; u=3352525637; n=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; unc=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; lat=40.052377; lng=116.310177; client-id=79f01014-150a-4c33-bfec-56032a3886de; firstTime=1680436820577; _lxsdk_s=18741d40e86-4a5-b61-636%7C%7C21'
    }
    
    session = requests.Session()
    response = session.get(url=basicUrl,headers=headers)

    ex = '<a class="" href="(.*?)" data-reactid='
    info = re.findall(ex,response.text)
    originUrl_list = [i for i in info if (i.startswith('http') and i.endswith('/'))]
    print(len(originUrl_list))

    cateId = []
    for Url in originUrl_list:
        cateId.append(Url.split('/')[-2][1:])
    print('cateId 列表:',cateId)
    return cateId

# 获取商铺id
def get_poiId(pageShopUrl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie':'_lxsdk_cuid=1863602fe4ec8-00221287d3f5ff-26021051-168000-1863602fe4eaa; WEBDFPID=3wx7944x830v5y120vy65zwyu72046288136397u9z3979583724v7z3-1991303412282-1675943411504SICWEKWfd79fef3d01d5e9aadc18ccd4d0c95074238; _hc.v=f708e0ca-90c8-32f8-309f-2dbe356faf69.1675943516; iuuid=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; _lxsdk=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; cityname=%E5%8C%97%E4%BA%AC; ci=1; rvct=1%2C140%2C382%2C10; __mta=145128971.1675943418903.1676084135258.1676104841696.24; uuid=2700efcb13bc4b01b495.1679800560.1.0.0; latlng=39.928159%2C116.301426; ci3=1; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; qruuid=2c6cdb43-d56e-47e9-b318-e0fa9f77f1b8; token2=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; oops=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; lt=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; u=3352525637; n=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; unc=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; lat=40.052377; lng=116.310177; client-id=79f01014-150a-4c33-bfec-56032a3886de; firstTime=1680436820577; _lxsdk_s=18741d40e86-4a5-b61-636%7C%7C21'
    }
    session = requests.Session()
    response = session.get(url=pageShopUrl,headers=headers)
    ex = '"poiId":(.*?),"frontImg"'
    poiId = re.findall(ex,response.text)
    return poiId

# 获取评论url
def get_commenturl(cityname,cityurl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie':'_lxsdk_cuid=1863602fe4ec8-00221287d3f5ff-26021051-168000-1863602fe4eaa; WEBDFPID=3wx7944x830v5y120vy65zwyu72046288136397u9z3979583724v7z3-1991303412282-1675943411504SICWEKWfd79fef3d01d5e9aadc18ccd4d0c95074238; _hc.v=f708e0ca-90c8-32f8-309f-2dbe356faf69.1675943516; iuuid=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; _lxsdk=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; cityname=%E5%8C%97%E4%BA%AC; ci=1; rvct=1%2C140%2C382%2C10; __mta=145128971.1675943418903.1676084135258.1676104841696.24; uuid=2700efcb13bc4b01b495.1679800560.1.0.0; latlng=39.928159%2C116.301426; ci3=1; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; qruuid=2c6cdb43-d56e-47e9-b318-e0fa9f77f1b8; token2=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; oops=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; lt=AgEOINpYfsxEQA8kSbpS3FPRZap9f2hL4FkujT7fMmRuDbNS-fQrUghBuKCZC8ZofYhzaXY1K7WmZAAAAAC2FwAAUhu1fipk4tAVkxMZZSTdB34EZuMvZ6ysv9B-S_W9c2UiLzktROrOz7ppqPpo0oQZ; u=3352525637; n=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; unc=%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%AF%BF%E6%AF%94%E5%8D%97%E5%B1%B1; lat=40.052377; lng=116.310177; client-id=79f01014-150a-4c33-bfec-56032a3886de; firstTime=1680436820577; _lxsdk_s=18741d40e86-4a5-b61-636%7C%7C21'
    }
    for cateid in CATEID:
        maxUrl = f'https://bj.meituan.com/meishi/api/poi/getPoiList?cityName={cityname}&cateId={cateid}&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=3352525637&uuid=702525fd116b48578bc4.1675943406.1.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fbj.meituan.com%2Fmeishi%2Fc393%2&riskLevel=1&optimusCode=10&_token=eJxVjl9vokAUxb%2FLvEJkgCkwvtEVELZot8CobPpAYfgrKjCguNnvvtPUPmxyk3Puub%2BbnD%2BgdzOwlCHEEIpgoj1YAnkBFxoQARv4RdM1iBCC2MBPIkj%2Fz7DBnz56sgLL3%2FKTqomaYrx%2FJm88%2BEqwBt%2FFh1W4VRCfT8blCCgZuwxLSfqoFy2t2JicFum5lbgfykpKVaxKvAjgfBtynmvz0OSh7Hv3eXPODlVx4o56V1JH8mjOll9SIXiOmHAt5pA43ltMdhetQ%2BuD%2F%2BwFZnookjbaKmEeCL%2BsbYT1%2Bt7P6KRO816no9mPL6T2Jssv4Hra5H7Yl5AVkoKkCRn6j7t96tw88HVUEXap4nR3oPUYmXbskfZs3PJbbKvM2W%2FGF%2Bt1a3uoPuxpInjWOr0fbdSV2ZAFVHO7ozuRmK3IsC%2BNLLCMSGYdVgU3sUdv9%2FM4Rc5dy5JaHpLznO%2Fo9aY0DdZXVhfTrNpARVdMOWudia7WXVhWzTBuJMNyor4Bf%2F8BEFuTHg%3D%3D'
        session = requests.Session()
        response = session.get(url=maxUrl,headers=headers)
        js_data = response.json()
        totalCounts = js_data['data']['totalCounts']
        maxPage = totalCounts // 15 + 1

        for page in range(1,maxPage+1):
            pageShopUrl = cityurl + f'c{cateid}/pn{page}/'
            poiId = get_poiId(pageShopUrl)
            for poiid in poiId:
                commentUrl = f'https://bj.meituan.com/meishi/api/poi/getMerchantComment?uuid=702525fd116b48578bc4.1675943406.1.0.0&platform=1&partner=126&originUrl={pageShopUrl}&optimusCode=10&id={poiid}&userId=3352525637&offset=0&pageSize=10&sortType=1&tag'
                if commentUrl not in COMMENTURL:
                    COMMENTURL.append(commentUrl)
    print('评论url长度:',len(COMMENTURL))

# 异步下载
async def download_one_comment(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie':'uuid=702525fd116b48578bc4.1675943406.1.0.0; _lxsdk_cuid=1863602fe4ec8-00221287d3f5ff-26021051-168000-1863602fe4eaa; WEBDFPID=3wx7944x830v5y120vy65zwyu72046288136397u9z3979583724v7z3-1991303412282-1675943411504SICWEKWfd79fef3d01d5e9aadc18ccd4d0c95074238; mtcdn=K; _hc.v=f708e0ca-90c8-32f8-309f-2dbe356faf69.1675943516; iuuid=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; _lxsdk=52920774B3C74F49D5EEC95BCA12A285143F22F41BB50BE38F5CF6F631F01DE7; IJSESSIONID=node0eipfnxkad9ml137lduez07smu12501051; cityname=%E5%8C%97%E4%BA%AC; userTicket=FHjqZLRdtNLYdnFTFEbEFiKMPEnFczUaBxUcawiV; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; lat=39.92501; lng=116.59771; ci=140; rvct=140%2C1%2C382%2C10; qruuid=e0e8991a-36a4-4a8b-8976-a5670c81e0d6; token2=AgE9Igd39m9WhQ7bvVM_uDiMfFTCy1-lINpOxRzqJAdRl92WEQpTpyupDyODNSqFureQZ5vHOK8A_wAAAACMFgAAXTOFC6El260vOV2KaBqbb5ZeO2ETE_ySmJ6CUr1RKeuZcDPkjPu7drh_1n-N9_Xt; oops=AgE9Igd39m9WhQ7bvVM_uDiMfFTCy1-lINpOxRzqJAdRl92WEQpTpyupDyODNSqFureQZ5vHOK8A_wAAAACMFgAAXTOFC6El260vOV2KaBqbb5ZeO2ETE_ySmJ6CUr1RKeuZcDPkjPu7drh_1n-N9_Xt; lt=AgE9Igd39m9WhQ7bvVM_uDiMfFTCy1-lINpOxRzqJAdRl92WEQpTpyupDyODNSqFureQZ5vHOK8A_wAAAACMFgAAXTOFC6El260vOV2KaBqbb5ZeO2ETE_ySmJ6CUr1RKeuZcDPkjPu7drh_1n-N9_Xt; u=3003462955; n=gIa130670404; unc=gIa130670404; firstTime=1676093705912; __mta=150229897.1676084143015.1676093704645.1676093705940.6; client-id=bbd63556-3500-42cc-b485-32e4d3c9d3a1; _lxsdk_s=1863ed44f29-ddd-fe3-bcd%7C%7C27'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,headers=headers) as response:
            js_data = await response.json()
            comment_list = js_data['data']['comments']
            print(comment_list)
            for comment in comment_list:
                content = comment['comment'].replace('\n',' ')
                with open('meituan_comment.txt','a+',encoding='utf-8') as f:
                    f.write(content)
                    f.write('\n')
    # 同步操作
    # session = requests.Session()
    # response = session.get(url=url,headers=headers)
    # js_data = response.json()
    # comment_list = js_data['data']['comments']
    # for comment in comment_list:
    #     content = comment['comment'].replace('\n',' ')
    #     with open('meituan_comment.txt','a+',encoding='utf-8') as f:
    #         f.write(content)
    #         f.write('\n')
    

if __name__ == '__main__':
    CATEID = get_cateId()
    CATEID = ['393', '11', '17', '40', '36', '28', '35', '395', '54', '20003', '55', '56', '20004', '57', '400', '58', '41', '60', '62', '63', '217', '227', '228', '229', '232', '233', '24', '59']
    CITYNAME = []
    CITYURL = []
    COMMENTURL = []
    get_cityname()

    # 线程池 100个子线程
    with ThreadPoolExecutor(100) as t:
        for index in range(len(CITYNAME)):
            t.submit(get_commenturl,CITYNAME[index],CITYURL[index])

    # 保存评论url链接
    with open('backup_url.txt','a+',encoding='utf-8') as f:
        for url in COMMENTURL:
            f.write(url)
            f.write('\n')

    # 打开文件中的评论链接,放入COMMENTURL列表中,已有美团评论链接txt--meituan_url.txt
    with open('backup_url.txt','r',encoding='utf-8') as f:
        for line in f.readlines():
            COMMENTURL.append(line.replace('\n',''))
    
    # 异步下载 每次100个异步任务
    loop = asyncio.get_event_loop()
    for i in range (0,148904,100):
        tasks = [asyncio.ensure_future(download_one_comment(url)) for url in COMMENTURL[i:i+100]]
        loop.run_until_complete(asyncio.wait(tasks))
    loop.close()