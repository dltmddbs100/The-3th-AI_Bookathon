## The 3th AI_Bookathon

**팀 AItist ([이승윤](https://github.com/dltmddbs100/), [장민석](http.github.com/jangsus1), 성민경, 이지현)**

<img src="https://user-images.githubusercontent.com/55730591/147868801-5c42edb0-5eb4-414e-bc16-4e057b587766.jpg" width="800" height="400"/>
     
    성균관대 & Mindslap 에서 주최한 제 3회 AI Bookathon 대회에 참여했습니다.
    지원한 60팀 중 예선을 거쳐 15팀 내에 선발되어 본선에 진출했고, 
    Mindslap에서 제공한 서버를 통해 GPT-2를 사용한 수필 창작을 수행했습니다.
     
    해당 대회에서 사용한 소스코드 레포입니다.

## 1. Introduction
AI Bookathon은 대회 시작 직전에 생성해야하는 수필에 대한 주제어가 주어지고 이에 따라
인공지능 모델을 사용하여 그에 맞는 작품을 생성하는 방식으로 진행됩니다.

#### - 대회시작 전 -

대회 시작 전 준비과정에서 저희는 수필의 **`고전스럽고 아름다운 수필`** 이라는 전반적인 방향을 설정했습니다

여기서 고전스러운 수필이란, 근대문학의 문체를 가진 산문형식의 수필을 말합니다.

일반적으로 AI로 수필을 생성한다고하면 주로 현대문학에 가까운 작품들이 많은 것을 볼 수 있습니다. 
따라서 저희는 차별화를 위해 반대로 고전 또는 근대와 같은 과거 문학의 느낌을 갖는 수필을 만들고 싶었습니다. 
따라서 저희 팀은 근대문학의 향수를 갖고있는 아름다운 문체의 작품을 생성하는데 주목하고자 했습니다.

#### - 대회 시작 -

대회가 시작되고 **'함께'** 라는 주제어가 주어졌습니다. 해당 주제어를 어떻게 수필에 녹여낼지,
갖고있는 데이터들을 고려했을때 어떤내용을 가진 수필이 가장 적합할지를 생각했습니다.
저희는 최종적으로 **`자연과 함께 성장하는 인간`** 을 주제로 선정해 수필을 생성하였습니다.


## 2. Data Crawling
데이터는 다양한 사이트에서 수집했습니다. 마인즈랩 서버에서 제공되는 모델은 뉴스 데이터와 같은
딱딱한 문체로 사전학습된 GPT2이기 때문에 fine tuning시에 사용할 데이터로 저희가 원하는 느낌의
수필문체를 가진 데이터를 중점적으로 수집했습니다.

+ 수집한 데이터 내역입니다.
  - 2000-2020 신춘문예 단편 수필(조선, 동아, 경향 등 8곳)
  - 글틴: 중.고등학생 수필 및 공모작
  - Brunch: 수필체를 가진 작가별 수집
  - 한국산문 작가협회: 수필 공모
  - 재미수필 문학가협회: 반숙자 수필 80선
  - 수필.net: 뜰 게시판 수필
+ Python에서 제공하는 selenium, beautiful soap, scrapy를 사용했습니다.
+ 총 약 20mb 크기의 데이터들을 수집했습니다.


## 3. Preprocessing
정제는 1차와 2차를 나누어 진행했습니다.  
1차적으로는 특수문자, 기호, 불용어와 같은 부분들을 자동으로 제거하도록 함수를 구성했습니다.
다음으로 2차에서는 20mb의 데이터 중, 질이 좋은 데이터들을 선별하기위해 모든 데이터를 직접 검수했습니다.

+ 수집된 data들을 dataframe 형식으로 통합
+ Regex를 이용해 전체 텍스트들을 통상적인 기준으로 1차 정제
+ 팀원들과 분담해 잘못된 문법 또는 일부주제에 지나치게 편향된 내용(여행기, 학창시절 이야기 등)을 가진 텍스트들을 눈으로 확인하며 제거
+ 최종적으로 약 6mb 크기의 질 좋은 데이터 선정


## 4. Model Training Strategy
제공된 서버에서는 NVIDIA T4 환경에서 마인즈랩의 자체 GPT2모델을 학습할 수 있도록되어있습니다.  
모델 자체는 비공개로 수정이 불가능하며, hyper-parameter와 모델에 데이터를 어떤방식으로 투입할지를 조절하는 feeder와
generation시에 사용하는 sampling method 정도만 수정이 가능했습니다. 제한된 환경에서 활용한 전략입니다.

**1. 제한된 메모리 - batch size의 제한**  
=> accumulation step 활용

**2. 문서의 max sequnece length 편차가 심함 - max sequence length 초과시 내용의 뒷부분이 소실**  
=> 로컬에서 sentence tokenizer 구현해 train data가 max sequnce length를 초과하지 않도록 여러 데이터 단위로 분할
```python
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
 ```

**3. train data를 모델에 주입시에 사용되는 feeder method가 문단 연결성을 저하**  
=> 문단 연결성의 저하를 막도록 custom feeder method 구현  
```python
def _sent_custom_append(self, text, length):
 sentences = split_text_into_sentences(text)
 sentences_tokenized = self.tokenizer.tokenize(sent) for sent in sentences if sent is not '']
 
 begin_index = 0
 
 selected_sents = sentences_tokenized[begin_index:]
 
 token_ids = self.tokenizer.convert_tokens_to_ids([token for sent in selected_sents for token in sent])
 while len(token_ids) < length:
  appending_text = random.choice(self.text_files).read_text(encoding='utf-8')
  token_ids += self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(appending_text))
  
 return token_ids[:length]
```

**4. generation시 top-p 또는 top-k만 사용 가능**  
=> top-p & top-k 동시적용으로 수정
```python
def top_p_tok_k_logits(logits, p, k):
 with tf.variable_scope('top_p_top_k_logits'):
  logits_sort = tf.sort(logits, direction='DESCENDING')
  probs_sort = tf.nn.softmax(logits_sort)
  indices = tf.constant(np.tile(np.arange(logits.shape[1].value), (logits.shape[0].values,1)))
  probs_sums = tf.cumsum(probs_sort, axis=-1, exclusive=True)
  
  logits_masked = tf.where((probs_sums < p) & (indeices < k), logits_sortm, tf.ones_like(logits_sort)*1000)
  min_logits = tf.reduce_min(logits_masked, axis=1, keepdims=True)
  
  return tf.where(
   logits < min_logits,
   tf.ones_like(logits, dtype=logits.dtype) * -1e10,
   logits
  )
```

**5. 두 가지 유형의 모델 사용**  

<img src="https://user-images.githubusercontent.com/55730591/147868729-cdafd639-c7dc-4eb7-bb86-3e199945b09c.png" width="900" height="400"/>


## 5. Model Inference
추론 단계에서 입력한 첫단어는 '햇살'입니다. 해당 단어를 통해 나온 **'햇살이 스르륵 손에 잡힐 듯한 투명한 창 안에는 봄이 떠오른다.'** 가 시작 문장으로 자연스럽게 계절로 연결되어 계절의 흐름으로 글을 시작할 수 있었습니다. 그 후 생성된 문장을 다시 입력으로 투입함을 반복하는 regressive한 방식으로 작품을 생성해나갔습니다. 내용의 구체화가 필요한 부분에서는 후자의 모델을, 추상화가 필요한 부분에서는 전자의 모델을 사용하는 방식으로 두 가지 유형의 모델을 적절히 선택하여 사용했으며, 계절의 변화가 필요한 부분에서는 '여름' 또는 '뜨거운'과 같이 연상되는 단어를 입력해 매끄럽게 연결될 수 있도록 했습니다.


## 6. Result
**`인연(人然): 교감, 그리고 성장`**

자연을 모티브로 삶아 계절이 바뀌어감에 따라 사람과 자연이 교감하며 비춰지는 사람의 성장의 모습을 그려냈습니다.  

![image](https://user-images.githubusercontent.com/55730591/147868962-0720ece6-1255-445d-8a6d-79c0d6e9f241.png)
![image](https://user-images.githubusercontent.com/55730591/147869009-9aaefd83-51cf-4ab5-a7fd-486f45489a5a.png)

#### 문장예시
+ 동행의 언어에는 삶의 이야기와 한 장의 문장이 담겨있다.
+ 창을 통해 비추는 햇살이 내 손을 잡았다. 싹이 돋은 솜털 같았다.
+ 봄의 산은 우리를 두근거리게 하고 그에 스며든 신록의 초록빛은 희망과 온기를 안겨준다.
+ 창을 통해 비친 푸른 바다와 눈부시게 비치는 햇살은 우리를 새로운 환상의 세계로 스며들게 하는 듯 하다.

최종적으로 생성된 수필의 내용은 [이곳](https://github.com/dltmddbs100/The-3th-AI_Bookathon/blob/main/outputs/%EC%9D%B8%EC%97%B0(%E4%BA%BA%E7%84%B6).pdf)에서 확인하실 수 있습니다.
