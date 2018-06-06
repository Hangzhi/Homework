# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:45:58 2017

@author: Lenovo
"""
import pandas as pd
import requests
import re
import math
from bs4 import BeautifulSoup
import pylab as plt
import jieba
import jieba.posseg as pseg
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator

lurl = 'https://movie.douban.com/top250'
movie = []
result = []

def getlist(listurl, result):
    res = requests.get(listurl)
    soup = BeautifulSoup(res.text, 'html.parser')
    movielist = soup.select('.grid_view li')
    for m in movielist:
        rank = m.select('em')[0].text
        if len(m.select('.title')) > 1:
            other_name = m.select('.title')[1].text.strip().strip('/').strip()
        else:
            other_name = "No info"
        chinese_name = m.select('.title')[0].text
        info_str = m.select('.info .bd p')[0].text.strip().replace(u'\xa0', u' ')
        info_list = info_str.split('\n')
        time_list = info_list[1].strip().split('/')
        temp=m.select('.info .bd .star .rating_num')[0].text
        ranking_num=int(temp[0])+0.1*int(temp[2])
        movie_time = time_list[0].strip()
        if movie_time=='1961(中国大陆)':
            movie_time='1961'
        movie_place = time_list[1].strip()
        movie_type = time_list[2].strip()
        temp=m.select('.info .bd .star span')[3].text
        ranking_member=re.findall("\d+",temp)[0]
       
        director_list = info_list[0].strip(u'导演:').split('  ')
        director = director_list[0].strip()
        if len(director_list) > 1:
            main_actor = director_list[1].strip().strip(u"主演:").strip()
        else:
            main_actor = u"暂无信息"
        if m.select('.inq'):
            comments = m.select('.inq')[0].text.strip()
        else:
            comments = 'None'
        movie.append(u'排名: ' + rank + '\n' + u'电影名: ' + chinese_name + '\n' +  u'导演: ' + director + '\n' +  u'主演: ' +
                     main_actor + '\n' + u'时间: ' + movie_time + '\n' + u'产地： '+ movie_place + '\n'+ u'类型： '
                     + movie_type + '\n' + u'评论: ' + comments + '\n'+ u'评分人数: ' + ranking_member + '\n')
        data_movies = (rank,ranking_num, chinese_name, other_name, director, main_actor, movie_time,
                       movie_place, movie_type, comments,ranking_member)
        result.append(data_movies)
    
    if soup.select(u'.next a'):
        asoup = soup.select(u'.next a')[0][u'href']
        Next_page = lurl + asoup
        getlist(Next_page, result)
    else:
        print('Done')
    return result

result = getlist(lurl, result) 


def all_to_excel(frame):
    frame.to_excel("douban_movie.xlsx")
     
def print_type(frame):
    movie_type=frame['type']
    all_type=[]
    for t in movie_type:
        type_list=t.split(' ')
        all_type.extend(type_list)
    set_type=set(all_type)
    type_num=dict.fromkeys(set_type,0)
    for t in all_type:
        type_num[t]+=1
    if '1978(中国大陆)'in type_num.keys():
        del type_num['1978(中国大陆)']
    
    type_num= sorted(type_num.items(), key=lambda d:d[1])
    print (type_num)
    x=[]
    y=[]
    for t in type_num:
        x.append(t[0])
        y.append(t[1])
    #print(x) 
    #print(y)
    type_series=pd.Series(y,index=x)
    df = pd.DataFrame(type_series)
    print("fsjio")
    df.plot(kind = 'barh',color='b', alpha=0.5) 
    print("fjios")
    plt.mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.mpl.rcParams['axes.unicode_minus'] = False
    #font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    plt.xlabel('数值')
    plt.ylabel('类型')
    plt.title('豆瓣TOP250电影类型统计')
    j=0
    for a,b in type_num:
       plt.text( b+3,j, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
       j+=1
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(7.5, 10.5)
    fig.savefig('type_1.png', dpi=100)
    plt.show()
    
    
  
    explode=[0]
    f=[0]
    l=["灾难,情色,运动,恐怖\n武侠,纪录片,歌舞,西部\n儿童,音乐,同性,古装,历史\n (59)\n\n 注：一部电影的多种类型都将计入考虑"]
    c=[ '#FFFACD']
    colors=[ '#ADD8E6', '#F08080', '#E0FFFF',  '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1','#FFA07A']
    count=0    
    print(x)
    print (y)
    print(zip(x,y))
    for a,b in zip(x,y):
        if b>10:
            explode.append(b/1000)
            f.append(b)
            left=" ("
            right=")"
            temp=a+left+str(b)+right
            l.append(temp)
            c.append(colors[count%len(colors)])
            
        else:
            f[0]+=b;
        count+=1;
    print(f,l,c)
    plt.pie(f, explode=explode,labels=l,colors=c,autopct='%1.2f%%', shadow=True)
    plt.title("豆瓣TOP250电影类型比例统计")
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(9, 8)
    fig.savefig('type_2.png', dpi=100)
    plt.show()

    
    
    #无剧情版 类型统计
    print(type_num)
    del type_num[-1]
    x=[]
    y=[]
    for t in type_num:
        x.append(t[0])
        y.append(t[1])
    #print(x)
    #print(y)
    type_series=pd.Series(y,index=x)
    df = pd.DataFrame(type_series)
    df.plot(kind = 'barh') 
    plt.mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.mpl.rcParams['axes.unicode_minus'] = False
    #font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    plt.xlabel('数值')
    plt.ylabel('类型')
    plt.title('豆瓣TOP250电影类型统计')
    j=0
    for a,b in type_num:
       plt.text( b+1,j, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
       j+=1
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(7.5, 10.5)
    fig.savefig('type_3.png', dpi=100)
    plt.show()
    
    
    explode=[0]
    f=[0]
    l=["灾难,情色,运动,恐怖\n武侠,纪录片,歌舞,西部\n儿童,音乐,同性,古装,历史\n\n 注：不计入【剧情】类型\n 计入一部电影的多种类型"]
    c=[ '#FFFACD']
    colors=[ '#ADD8E6', '#F08080', '#E0FFFF',  '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1','#FFA07A']
    count=0    
    print(x)
    print (y)
    print(zip(x,y))
    for a,b in zip(x,y):
        if b>10:
            explode.append(b/1000)
            f.append(b)
            left="["
            right="]"
            temp=a+left+str(b)+right
            l.append(temp)
            c.append(colors[count%len(colors)])
            
        else:
            f[0]+=b;
        count+=1;
    print(f,l,c)
    plt.pie(f, explode=explode,labels=l, colors=c,autopct='%1.2f%%', shadow=True)
    plt.title("豆瓣TOP250电影类型比例统计")
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(9, 8)
    fig.savefig('type_4.png', dpi=100)
    plt.show()
    
  
def pict_place(frame):
    movie_type=frame['movie_place']
    all_type=[]
    for t in movie_type:
        type_list=t.split(' ')
        all_type.extend(type_list)
    set_type=set(all_type)
    type_num=dict.fromkeys(set_type,0)
    for t in all_type:
        type_num[t]+=1
    type_num= sorted(type_num.items(), key=lambda d:d[1])
    print (type_num)
    x=[]
    y=[]
    count=0
    for t in type_num:
        if t[1]<5:
            print(t[0])
            count+=t[1]
            continue
        if t[0]=="1964(中国大陆)":
            continue
        if t[0]=="中国大陆":
             y.append(t[1]+1)
        else:
            y.append(t[1])
        x.append(t[0])
        
    print (count)
    #print(x)
    #print(y)
    type_series=pd.Series(y,index=x)
    df = pd.DataFrame(type_series)
    df.plot(kind = 'barh',color='b',alpha=0.5) 
    plt.mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.mpl.rcParams['axes.unicode_minus'] = False
    #font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    plt.xlabel('数值')
    plt.ylabel('产地')
    plt.title('豆瓣TOP250主要电影产地统计（5部及以上）')
    j=0
    for b in y:
       plt.text(b+3 ,j, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
       j+=1
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(7.5, 10.5)
    fig.savefig('place_1.png', dpi=100)
    plt.show()
    
    explode=[0]
    f=[30]
    l=["其他国家：博茨瓦纳,捷克,波兰,比利时,巴西\n阿根廷,冰岛,泰国,阿联酋,丹麦\n西德,奥地利,爱尔兰,印度,伊朗\n南非,瑞典,新西兰,瑞士[30]"]
    c=[ '#FFFACD']
    colors=[ '#ADD8E6', '#F08080', '#E0FFFF',  '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1','#FFA07A']
    count=0    
    print(x)
    print (y)
    print(zip(x,y))
    for a,b in zip(x,y):
        if b>=5:
            explode.append(b/1000)
            f.append(b)
            left="["
            right="]"
            temp=a+left+str(b)+right
            l.append(temp)
            c.append(colors[count%len(colors)])
        count+=1;
    print(f,l,c)
    plt.pie(f, explode=explode,labels=l, colors=c,autopct='%1.2f%%', shadow=True)
    plt.title('豆瓣TOP250主要电影产地统计')
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(9, 8)
    fig.savefig('place_pie.png', dpi=100)
    plt.show()

def pict_director(frame):
    movie_type=frame['director']
    all_type=[]
    for t in movie_type:
        type_list=t.split('/')
        all_type.extend(type_list)
    set_type=set(all_type)
    type_num=dict.fromkeys(set_type,0)
    d=list(type_num.keys())
    for t in all_type:
        type_num[t]+=1
    for i in d:
        if type_num[i]==1:
            del type_num[i]
    #fromkeys( ,val) val是一个定值 由指针指向 所以如果一个改变 新建字典中所有的都会改变
    director=dict.fromkeys(type_num.keys(),[]) 
    for d in director:
        director[d]=[]
    
    l=list(director.keys())
    for index, row in frame.iterrows():
        #print(index,row)
        t=row["director"]
        temp_l=t.split('/')
        for temp in temp_l:
            if temp in l:
                director[temp].append(row["chinese_name"])
           
           
            
    #print(count)
    #print(director)
    type_num= sorted(type_num.items(), key=lambda d:d[1])
    #print (type_num)
    x=[]
    y=[]
    for t in type_num:
        x.append(t[0])
        y.append(t[1])
    #print(x)
    #print(y)
    type_series=pd.Series(y,index=x)
    df = pd.DataFrame(type_series)
    df.plot(kind = 'barh',alpha=0.5) 
    plt.mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.mpl.rcParams['axes.unicode_minus'] = False
    #font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    plt.xlabel('数值')
    plt.ylabel('导演')
    plt.title('豆瓣TOP250主要电影导演统计（多于1部）')
    j=0
    print(director)
    for a,b in type_num:
       plt.text( 0,j, director[a], ha='left', va= 'bottom',fontsize=11)
       j+=1
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(23, 18)
    fig.savefig("director123.png", dpi=200)
    plt.show()
    
def form_data(result):
    data={"rank":[],'ranking_num':[],"chinese_name":[],'other_name':[],'director':[],'main_actor':[],'movie_time':[],'movie_place':[],'type':[],'comment':[],'ranking_member':[]}
    frame_title=["rank",'ranking_num',"chinese_name",'other_name','director','main_actor','movie_time','movie_place','type','comment',"ranking_member"]
    for m in result :
       for no in range(11):
           data[frame_title[no]].append(m[no])
    frame=pd.DataFrame(data)
    frame.index=frame['rank'].tolist()
    return frame
    
def popular_rank(frame):
    ranking_member=frame["ranking_member"]
    rm_num=[]
    rk_num=[]
    rank=1
    for a in ranking_member:
        rk_num.append(rank)
        rm_num.append(round(math.sqrt(int(a)%10000)))
        rank+=1
    plt.mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.mpl.rcParams['axes.unicode_minus'] = False
    plt.plot(rk_num,rm_num,'.-')
    plt.xlabel("Top250排名")
    plt.ylabel("人气值")
    plt.title("豆瓣TOP250电影排名-人气趋势")
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(15,10)
    fig.savefig('popular_index.png', dpi=100)
    plt.show()
    
    frame_num=frame.sort_values(by='ranking_num',ascending=False)
    ranking_member=frame_num["ranking_member"]
    rm_num=[]
    rk_num=[]
    rank=1
    for a in ranking_member:
        rk_num.append(rank)
        rm_num.append(round(math.sqrt(int(a)%10000)))
        rank+=1
    plt.mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.mpl.rcParams['axes.unicode_minus'] = False
    name=frame_num["chinese_name"]
    num=frame_num["ranking_num"]
    
    print(len(rm_num),len(rk_num))
    for a,b in zip(rk_num,rm_num):
        #print(a,b)
        s_temp=name[a-1]+str(num[a-1])
        #print(s_temp)
        plt.text(a,b,s_temp,rotation=25)
  
    plt.plot(rk_num,rm_num,'.')
    plt.xlabel("评分排名")
    plt.ylabel("人气值")
    plt.title("豆瓣TOP250电影评分-人气趋势")
    print(0)
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(80,10)
    fig.savefig('rank-pop.png', dpi=100)
    plt.show()
    
    
def period_split(frame):
    time=frame["movie_time"]
    period=[]
    for i in time:
        if i=='1961(中国大陆)':
            i=1961
        period.append(int(int(i)/10))
    period_set=set(period)
    pd_split=dict.fromkeys(period_set,0)
    for i in time:
        if i=='1961(中国大陆)':
            i=1961
        temp=int(int(i)/10)
        pd_split[temp]+=1
    pd_label=[]
    s=pd_split.keys()
    for i in s:
        temp=i
        t='-'
        temp_s=str(int(temp)*10)+t+str((int(temp)+1)*10)
        pd_label.append(temp_s)
    x=[]
    y=[]
    for a,b in zip(pd_label,pd_split.values()):
        x.append(a)
        y.append(b)
    print(x,y)
    plt.mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.mpl.rcParams['axes.unicode_minus'] = False
    #font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    explode=[0]
    f=[]
    l=[]
    c=[ '#FFFACD']
    colors=[ '#ADD8E6', '#F08080', '#E0FFFF',  '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1','#FFA07A']
    count=0    
    print(x)
    print (y)
    print(zip(x,y))
    for a,b in zip(x,y):
        explode.append(b/1000)
        f.append(b)
        l.append(a)
        c.append(colors[count%len(colors)])
        count+=1
    print(f,l,c)
    print(explode)
    plt.pie(f,labels=l, colors=c,autopct='%1.2f%%', shadow=True)
    plt.title('豆瓣TOP 250 年份统计')
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(9, 8)
    fig.savefig('period.png', dpi=100)
    plt.show()
    
    time_p=frame["movie_time"]
    time=[]
    for i in time_p:
        time.append(int(i))
    print(time)
    n, bins, patches = plt.hist(time, 40, normed=1, facecolor='g', alpha=0.6)
    plt.title('豆瓣TOP 250 年份统计')
    fig = plt.matplotlib.pyplot.gcf()
    fig.set_size_inches(9, 8)
    plt.axis([1930,2020,0.000,0.060])
    fig.savefig('period_2.png', dpi=100)
    plt.grid(True)
    plt.show()


def comment_cloud(frame):
    comments=frame["comment"]
    stop_words=set(line.strip() for line in open('stopwords.txt',encoding='utf-8'))
    commentlist=[]
    for comment in comments:
        word_list=pseg.cut(comment)
        #print(word_list)
        for word,flag in word_list:
            if not word in stop_words and flag=='n':
                commentlist.append(word)
                
    back_coloring=imread("hat.jpg")
    
    content=' '.join(commentlist)
    wordcloud = WordCloud(font_path='simhei.ttf',mask=back_coloring,max_words=100,background_color="green").generate(content)
    image_colors=ImageColorGenerator(back_coloring)
    plt.gcf().set_size_inches(10, 8)
    plt.imshow(wordcloud.recolor(color_func=image_colors))
    plt.axis("off")
    wordcloud.to_file('wordcloud_hat.jpg')
    plt.show()
    
    
frame=form_data(result)
#整理所有数据
print_type(frame)
#输出类型分析
all_to_excel(frame)
#输出人气——排名分析
popular_rank(frame)
#输出所有数据到一个Excel文件
pict_place(frame)
#输出产地分析
pict_director(frame)
#输出导演分析
period_split(frame)
#输出断代分析
comment_cloud(frame)
#输出短评的词云分析

        
