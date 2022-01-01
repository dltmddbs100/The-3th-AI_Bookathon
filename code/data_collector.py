import numpy as np
import pandas as pd
import os
import re
from tqdm.notebook import tqdm 
import pandas as dp

# view rows which contain specific regex
def contain(data=None,column='contents',regex=None):
  return data[data[column].str.contains(regex)][column]

# preprocessing function
def preprocess(data, column='contents'):
  data=data.dropna(subset=[column]).reset_index(drop=True)
  
  for i in range(len(data)):
    data.at[i,column]=re.sub('\d{4}\. *\d{1,2}\. *\d{1,2}\.*',' ',data[column][i]) # 날짜형식 제거
    data.at[i,column]=re.sub('〈끝〉|<끝>|\(끝\)|-끝-|＜ *끝 *＞|〈 *끝 *〉','',data[column][i]) # 끝 제거
    data.at[i,column]=re.sub('[a-z0-9]+@[a-z]+\.[a-z]+[a-z\.]*',' ',data[column][i]) # 이메일 양식 제거
    
    data.at[i,column]=data[column][i].replace('\u200b','').replace('\xa0','').replace('\ufeff','').replace('\u3000','') # 유니코드 제거
    data.at[i,column]=re.sub('\([^\(\)]+\)|\[.+\]',' ',data[column][i]) # (), [] 안의 내용제거
    data.at[i,column]=re.sub('_|\*|\+|─|=|\^|;',' ',data[column][i]) # 특수기호 제거
    data.at[i,column]=re.sub('-+|—+','-',data[column][i]) # --- 대체
    data.at[i,column]=re.sub('[ㄱ-ㅎㅏ-ㅣ]+',' ',data[column][i]) # 자모음 제거
    data.at[i,column]=re.sub('[一-龥]',' ',data[column][i]) # 한자제거
    data.at[i,column]=re.sub('!+','!',data[column][i]) # ! 중복제거
    data.at[i,column]=re.sub('\?+','?',data[column][i]) # ? 중복제거
    data.at[i,column]=re.sub('~+','~',data[column][i]) # ~ 중복제거


    data.at[i,column]=re.sub('(\n)+|(\r)+|(\t)+','\n',data[column][i])
    data.at[i,column]=re.sub('\n',' ',data[column][i])
    data.at[i,column]=re.sub(r'\\',' ',data[column][i])
    data.at[i,column]=re.sub('．','. ',data[column][i])
    data.at[i,column]=re.sub('(\.){2,}|ㆍ{3,}|·{3,}|…+','…',data[column][i]) # ...대체
    data.at[i,column]=re.sub('…+','…',data[column][i])
    data.at[i,column]=re.sub(' +',' ',data[column][i])
    data.at[i,column]=re.sub(' \.','\.',data[column][i])
    data.at[i,column]=re.sub(' ,',',',data[column][i])
    data.at[i,column]=data[column][i].strip()

  return data


# sentence tokenize
ending_chars='[다요죠오네나라자아"][\.]+'
ending_marks='[!?][\.]*'
ending_exceptions='["\'’”]'
whitespaces='[ \n\t\*]'
sep_token='<<SEP>>'

def split_text_into_sentences(text):
  converted=re.sub('(?P<ending>{})(?!{})[ ]*'.format(ending_chars, ending_exceptions), '\g<ending>{}'.format(sep_token),
      re.sub('(?P<ending>{})(?!{})[ ]*'.format(ending_marks,ending_exceptions), '\g<ending>{}'.format(sep_token),
      re.sub('[ ]+',' ',
      re.sub('{}+'.format(whitespaces),' ',text))))
  sents = converted.strip().split(sep_token)
  return sents[:-1] if len(sents)>1 and sents[-1] =='' else sents

# sentence tokenizer
# separating the corpus into sentences => split the corpus not to exceed max len
def sent_tokenizer(data,max_len):
  final_list=[]
  for contents in tqdm(data['contents']):
    sents = split_text_into_sentences(contents)
    sent_len = len(sents)
    if sent_len > 3:
      len_i=[0]
      while sent_len-(sum(len_i)+1)!=0: 
        imsi=[]
        sent=[]
        for i in sents[sum(len_i):]:
          if sum(imsi)<max_len:
            sent.append(i)
            imsi.append(len(mecab.morphs(i)))
          else:
            pass
        imsi.pop()
        sent.pop()
        
        final_list.append(' '.join(sent))
        len_i.append(len(imsi))
  return final_list


# apply to real data
fdata_path='/content/drive/MyDrive/AI_Bookathon/AItist/final_data/f_data/최종본/'

d1=pd.read_csv(fdata_path+'f_data_v02_part_1_fin.csv')
d2=pd.read_csv(fdata_path+'f_data_v02_part_2_fin.csv')
d3=pd.read_csv(fdata_path+'f_data_v02_part_3_fin.csv')
d4=pd.read_csv(fdata_path+'f_data_v02_part_4_fin.csv')

f_data=d1.append(d2).append(d3).append(d4).reset_index(drop=True)
f_data=preprocess(f_data)

final_data=sent_tokenizer(f_data,378)

final_dataframe=pd.DataFrame({'contents':final_data})
final_dataframe['token_len']=0

for i in tqdm(range(0,len(final_dataframe))):
  final_dataframe.at[i,'token_len']=len(mecab.morphs(final_dataframe['contents'][i]))

# drop short corpus
final_dataframe=final_dataframe[final_dataframe['token_len']>100].reset_index(drop=True)
fin=final_dataframe[['contents']]


# making train text files
n = 0

file = 'train_{}.txt'
for row in tqdm(fin.contents.values):
  with open('train_txt_v02/'+file.format(n), 'w') as f:
    f.write(str(row))
    n += 1
