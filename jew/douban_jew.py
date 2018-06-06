# -*- coding: utf-8 -*-
"""
Created on Sat May 26 18:00:33 2018

@author: Lenovo
"""
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import jieba.posseg as pseg
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
import pylab as plt

result=[]

book_href_list=[]
title_list=[]
urllist=['https://www.douban.com/search?cat=1001&q=%E7%8A%B9%E5%A4%AA+%E6%99%BA%E6%85%A7'
,'https://www.douban.com/search?cat=1001&q=%E7%8A%B9%E5%A4%AA+%E5%8A%B1%E5%BF%97'
,'https://www.douban.com/search?cat=1001&q=%E5%A1%94%E6%9C%A8%E5%BE%B7+%E6%99%BA%E6%85%A7'
,'https://www.douban.com/search?cat=1001&q=%E7%8A%B9%E5%A4%AA+%E7%BE%8A%E7%9A%AE%E5%8D%B7'
]
id_list=[]
url= 'https://book.douban.com/subject_search?search_text=%E7%8A%B9%E5%A4%AA&cat=1001'
num_list=[]
intro_list=[]
#存储书籍详情信息
book=[]
book_data_list=[]
#count=0
def getcontent(url):#,count):
    #urlapd=str(count)
    #url=url+'&start='+urlapd
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    #htmlname=urlapd+'.html'
    #f = open(htmlname,"w",encoding='utf-8')  
    #f.write(res.text)
    booklist=soup.select('.result-list .result')
    for b in booklist:
        href_text=b.select('.title a')
        title=href_text[0].text
        #print(title)
        title_list.append(title)
        href=href_text[0]['href']
        book_href_list.append(href)
        id_extend=href_text[0]['onclick']
        id_list.append(id_extend)
        #count=count+1
    #count=15
    #urlapd=str(count)
    #Nextpage=url+'&start='+urlapd
    #getcontent(Nextpage)

def getdetail():
    for i in id_list:
        pattern1=re.compile('sid:.*?,')
        s_extend=pattern1.findall(i)[0]
        pattern2=re.compile("\d+\.?\d*")
        num=pattern2.findall(s_extend)
        id_num=num[0]
        if id_num in num_list:
            pass
        else:
            num_list.append(num[0])
        #print(i,s_extend,num)
def getdetail2():
    basic_url='https://book.douban.com/subject/'
    for i in num_list:
    #i=3894821
    #if i==3894821:
        url=basic_url+str(i)
        res=requests.get(url)
        #f=open('book.html',"w",encoding='utf-8')  
        #f.write(res.text)
        soup=BeautifulSoup(res.text,'html.parser')
        #获取id
        id_detail=str(i)
        #获取书名
        bookname=soup.select('title')
        bookname_detail=bookname[0].text
        bookname_detail=bookname_detail.split('(')[0]
        #print(bookname_detail)
        #获取作者名
        author=soup.select('#info a')
        if len(author)>0:
            author_detail_list=author[0].text.split('\n')
            #print(author_detail_list)
            if len(author_detail_list)==3:
                author_detail=author_detail_list[2].strip()+author_detail_list[1].strip()
            elif len(author_detail_list)==2:
                author_detail=author_detail_list[1].strip()
            else:
                author_detail=author[0].text
        print(author_detail,author_detail_list)
        #print(author_detail)
        #print(soup)
        #获取简介
        intro=soup.select('.related_info .intro')
        if len(intro)>0:
            summary_detail=intro[0].text
        else:
            summary_detail=''
        #获取评分
        rating_num=soup.select('.rating_num')
        rating_num_detail=rating_num[0].text
        #获取目录
        id_dir='#dir_'+str(i)+'_full'
        catg=soup.select(id_dir)
        if len(catg)>0:
            catg_detail=catg[0].text
        else:
            catg_detail=''
        book.append(u'编号:'+id_detail+'\n'+
                     u'评分'+rating_num_detail+'\n'+
                     u'书名:'+bookname_detail+'\n'+
                     u'作者:'+author_detail+'\n'+
                     u'简介'+summary_detail+'\n'+
                     u'目录'+catg_detail+'\n')
        data_book=(id_detail,
                   rating_num_detail,
                   bookname_detail,
                   author_detail,
                   summary_detail,
                   catg_detail
                   )
        book_data_list.append(data_book)

def to_frame():
    data={"id":[],
          'rating_num':[],
          'bookname':[],
          'author':[],
          'summary':[],
          'catalogue':[]}
    frame_title=["id",
          'rating_num',
          'bookname',
          'author',
          'summary',
          'catalogue']
    for b in book_data_list:
        for no in range(6):
            data[frame_title[no]].append(b[no])
    frame=pd.DataFrame(data)
    frame.index=frame['id'].tolist()
    return frame

def clouds(frame,key_word):
    comments=frame[key_word]
    stop_words=set(line.strip() for line in open('stopwords.txt',encoding='utf-8'))
    commentlist=[]
    for comment in comments:
        word_list=pseg.cut(comment)
        #print(word_list)
        for word,flag in word_list:
            if not word in stop_words and flag=='n':
                commentlist.append(word)
    pic_name='word_cloud'+key_word+'.jpg'
    back_coloring=imread("jew_man.png")
    content=' '.join(commentlist)
    if len(content)>0:
        wordcloud = WordCloud(font_path='simhei.ttf',mask=back_coloring,max_words=100,background_color="white").generate(content)
        image_colors=ImageColorGenerator(back_coloring)
        plt.gcf().set_size_inches(20,20)
        plt.imshow(wordcloud.recolor(color_func=image_colors))
        plt.axis("off")
        wordcloud.to_file(pic_name)
        plt.show()
        
    
for i in urllist:
    getcontent(i)

getdetail()
'''
print(num_list)
#print(id_list)
f = open('title.txt',"w",encoding='utf-8')
f.write('\n'.join(title_list))
g=open('href.txt',"w")
g.write('\n'.join(book_href_list))
#print(num_list)
'''
getdetail2()
frame=to_frame()
frame.to_excel("fake_jew_books.xlsx")
key_words=['bookname',
          'summary',
          'catalogue']

#for kw in key_words:
    #clouds(frame,kw)