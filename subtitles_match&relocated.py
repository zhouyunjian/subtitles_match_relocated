# Project   : subtitles_match_relocated_video
# File      : subtitles_match&relocated.py
# Author    : zhouyunjian
# Email     : 121105729@qq.com
# DateTime  : 2022/8/9
# MadeBy    : PyCharm


import os
import re
import fs


#定义常量 请根据实际情况调整
#BASE_PATH电影文件路径,程序使用fs模块可以支持多种文件系统.示例用smb来演示
BASE_PATH = 'smb://guest:@192.168.1.1:139/disk/movies/Top.Gun.Maverick.2022.IMAX.2160p.WEB-DL.x265.8bit.SDR.DDP5.1.Atmos-PLZPLZPROPER/'
#匹配os.path.splitext的extension格式
MOVIE_TARGET = ['.mp4','.avi','.rmvb','.mkv']
#fs.walke filter的匹配模式
SUB_TARGET = ['*.srt','*.ass','*.ass','*.sub','*.idx']
#re.search搜索用途,特殊符号加双反斜线
SUB_COUNTRY_TARGET = ['中英','英文\\.','简体\\.','简体\\&英文\\.','English\\.','Chinese\\.','\\.en\\.','\\.cn\\.','\\.eng\\.','\\.chs\\.','\\.chs\\&eng\\.']
#fs.filterdir匹配规则为shell通配符规则subs,sub忽略大小写匹配
SUB_FOLDER_TARGET = ['[Ss][Uu][Bb][Ss]','[Ss][Uu][Bb]']


def list_movie_file_dir(full_path):     # 搜索目录下的电影文件,并将电影名列表返回
    list_movie_path_res = movie_fs.listdir(full_path)
    list_movie_name = []    # 电影文件列表
    for i in range(len(list_movie_path_res)):   # 对电影目录下的文件列表进行循环
        if movie_fs.isfile(list_movie_path_res[i]): # 确认是否是普通文件
            extension = os.path.splitext(list_movie_path_res[i])[1]
            if extension in MOVIE_TARGET:
                movie_name = os.path.splitext(list_movie_path_res[i])[0]   # 判断是否是电影文件,并将确认是结果返回给变量
                if movie_name is not None:  # 如果变量非空
                    list_movie_name.append(movie_name)
    return list_movie_name

def all_unique(list_sub_sfx):   # 字幕文件后缀名列表,判断确认是否唯一
    if list_sub_sfx is not None:
        return len(set(list_sub_sfx)) == len(list_sub_sfx)
    else:
        return False

def check_sub_country(full_path):  # 检查是否是想要处理的字幕语言
    for i in range(len(SUB_COUNTRY_TARGET)):    #   遍历查找语言种类
        sub_check_result = re.search(SUB_COUNTRY_TARGET[i], full_path, re.IGNORECASE)   #   匹配语言种类结果
        if sub_check_result:    # 判断结果
            return SUB_COUNTRY_TARGET[i].strip('\.')    # 输出字幕语言国家

def check_movie_ep(movie_name):  # 函数检查电影名剧集
    list_movie_ep = re.findall(r"(?:s|season|se|ssn)\d{2}(?:e|x|episode|episodes)\d{2}", movie_name, re.IGNORECASE)
    if len(list_movie_ep) >= 1:
        return list_movie_ep[0]
    else:
        print(movie_name+'  电视剧剧集匹配不正确')
        print(list_movie_ep)
        pass

def copy_subs(list_sub_path,list_sub_country,movie_name):  # 一次性复制语言字幕文件列表的的字幕文件
    if len(list_sub_path) == len(list_sub_country):
        for i in range(len(list_sub_path)):
            extension = os.path.splitext(list_sub_path[i])[1]   # 字幕文件后缀名
            sub_name = os.path.splitext(list_sub_path[i])[0]    # 字幕文件路径前缀名
            sub_final_name = movie_name +'.'+ list_sub_country[i]+'('+str(i)+')' + extension
            movie_fs.copy(list_sub_path[i], sub_final_name, overwrite=True)   # 进行复制
            print('已经成功复制字幕' + list_sub_path[i] + '  复制成的名字:' + sub_final_name)

def copy_def_subs(list_sub_path,movie_name):  # 复制默认字幕文件
    for i in range(len(list_sub_path)):
        extension = os.path.splitext(list_sub_path[i])[1]
        sub_name = os.path.splitext(list_sub_path[i])[0]
        sub_final_name = movie_name +'.'+'English' + extension
        movie_fs.copy(list_sub_path[i], sub_final_name, overwrite=True)
        print('已经复制默认字幕成功字幕' + list_sub_path[i] + '  复制成的名字:' + sub_final_name)

def find_sub(sub_folder_path):  # 递归搜索路径下的所有字幕文件,返回字幕文件路径列表
    list_sub_path = []
    for path in movie_fs.walk.files(sub_folder_path,filter=SUB_TARGET):
        list_sub_path.append(path)
    return list_sub_path

def find_ep_sub(sub_folder_path,movie_ep):  # 递归寻找路径下的剧集字幕文件,并返回剧集的字幕文件列表
    list_sub_path = []
    for path in movie_fs.walk.files(sub_folder_path,filter=SUB_TARGET):
        if re.search(movie_ep, path ,re.IGNORECASE) is not None:
            list_sub_path.append(path)
    return list_sub_path

def find_sub_folder(full_path): # 寻找当前路径下的字幕文件夹,并返回列表
    list_sub_folder=[]
    gen_sub_folder = movie_fs.filterdir(full_path, dirs=SUB_FOLDER_TARGET, exclude_files=['*'])
    for i in gen_sub_folder:
        list_sub_folder.append(i.name)
    return list_sub_folder

try:
    movie_fs = fs.open_fs(BASE_PATH)
    try:
        # list the files on each share and suffixname
        list_movie_name = list_movie_file_dir('') # 根据视频文件获取所有电影名字列表
        movie_num = len(list_movie_name)  # 判断电影文件数量 分为 0 1 >1进行处理
        if movie_num == 0:      # 没有电影退出
            print('没有视频文件')
        elif movie_num == 1:    #
            print('只有一个视频文件')
            print(list_movie_name)
            sub_folder_num = 0
            list_sub_folder = find_sub_folder('')   # 搜索subs字幕文件夹 根据 0 1 >1进行处理
            sub_folder_num = len(list_sub_folder)
            if sub_folder_num == 0 :  # 判断字幕文件夹数量为0
                print('没有字幕文件夹')
            elif sub_folder_num == 1:  # 判断字幕文件夹数量为1则搜索字幕
                list_sub_path = []  # 初始定义字幕列表为空
                list_sub_sfx = [] # 初始定义字幕后缀名列表为空
                list_sub_country = []   # 初始定义字幕国家语言列表为空
                list_def_sub_path = find_sub(list_sub_folder[0])   # 遍历字幕文件夹文件得到字幕列表
                for i in range(len(list_def_sub_path)):
                    extension = os.path.splitext(list_def_sub_path[i])[1]
                    list_sub_sfx.append(extension)
                    sub_country = check_sub_country(list_def_sub_path[i])
                    if sub_country is not None:
                        list_sub_country.append(sub_country)
                        list_sub_path.append(list_def_sub_path[i])
                if len(list_sub_path) == 0: # 判断语言字幕匹配结果为0
                    if all_unique(list_sub_sfx):    # 判断是否默认字幕(如果每种字幕文件有且只有一个则判断为英文默认字幕)
                        print('确认电影  '+list_movie_name[0]+' 找到默认字幕如下:')
                        print(list_def_sub_path)
                        if input("回车键确认复制默认字幕/输入其他则退出") == '':
                            copy_def_subs(list_def_sub_path, list_movie_name[0])    # 复制默认字幕
                    else:   # 如果默认字幕判断失败
                        print('没有找到需要的字幕文件')
                elif len(list_sub_path) > 0:
                    print('匹配到语言字幕文件')
                    print(list_sub_path)
                    if input("回车键确认复制语言字幕/输入其他则退出") == '':
                        copy_subs(list_sub_path,list_sub_country,list_movie_name[0]) # 移动字幕文件
            elif sub_folder_num > 1:
                print('有多个字幕文件夹,请处理后再执行程序')
        elif movie_num >= 2:    # 判断电影文件数量大于等于2
            print('有多个视频文件,一共' + str(movie_num) + '个')
            print('全部视频文件名列表如下')
            print(list_movie_name)
            list_sub_folder = find_sub_folder('')
            sub_folder_num = len(list_sub_folder)
            if sub_folder_num == 0 :  # 判断字幕文件夹数量为0
                print('没有字幕文件夹')
            elif sub_folder_num == 1:  # 判断字幕文件夹数量为1
                list_movie_ep=[]    # 初始定义电影剧集列表为空
                for i in range(len(list_movie_name)):
                    list_sub_sfx = []   # 初始定义字幕后缀名列表为空
                    list_sub_path = []  # 初始定义字幕列表为空
                    list_sub_country = []  # 初始定义字幕国家语言列表为空
                    movie_ep = check_movie_ep(list_movie_name[i])
                    if movie_ep is not None:    # 剧集字符串判断
                        list_movie_ep.append(movie_ep)    # 剧集列表追加
                        list_def_sub_path = find_ep_sub(list_sub_folder[0],movie_ep)# 遍历字幕文件夹文件得到字幕列表
                        for j in range(len(list_def_sub_path)):
                            extension = os.path.splitext(list_def_sub_path[j])[1]
                            list_sub_sfx.append(extension)
                            sub_country = check_sub_country(list_def_sub_path[j])
                            if sub_country is not None:
                                list_sub_country.append(sub_country)
                                list_sub_path.append(list_def_sub_path[j])
                        if len(list_sub_path) == 0: # 判断语言字幕匹配结果为0
                            if all_unique(list_sub_sfx):    # 判断是否默认字幕(如果每种字幕文件有且只有一个则判断为英文默认字幕)
                                print('剧集'+movie_ep+'找到默认字幕如下:')
                                print(list_def_sub_path)
                                if input("回车键确认复制默认字幕/输入其他则退出") == '':
                                    copy_def_subs(list_def_sub_path, list_movie_name[i])    # 复制默认字幕
                            else:   # 如果默认字幕判断失败
                                print('没有找到需要的字幕文件')
                        elif len(list_sub_path) > 0:
                            print('剧集'+movie_ep+'匹配到语言字幕文件')
                            print(list_sub_path)
                            if input("回车键确认复制语言字幕/输入其他则退出") == '':
                                copy_subs(list_sub_path,list_sub_country,list_movie_name[i]) # 移动字幕文件
            elif sub_folder_num > 1:
                print('有多个字幕文件夹,请处理后再执行程序')
        movie_fs.close()
    except:
        print('### 字幕检索存在问题')
except:
   print('### 连接不上smb服务器')
