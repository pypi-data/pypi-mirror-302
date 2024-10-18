# import 설정
import os
import urllib.request
from konlpy.tag import Komoran
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate
#from utils.Preprocess import Preprocess

#dict_character = []    # 인물 사전
#dict_class = []        # 클래스 사전
#dict_genre = []        # 장르 사전
#dict_material = []     # 소재 사전
#dict_sent = []         # 감정 사전

def read_dict(dict_filename):
    dictList = []

    dict_character = []    # 인물 사전
    dict_class = []        # 클래스 사전
    dict_genre = []        # 장르 사전
    dict_material = []     # 소재 사전
    dict_sent = []         # 감정 사전

    # 사용자 지정 사전 정보 저장
    for i in dict_filename:
        f = open(i.strip(), 'r')
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            if l[1].strip() == 'character':
                dict_character.append(l[0].strip())
            elif l[1].strip() == 'class':
                dict_class.append(l[0].strip())
            elif l[1].strip() == 'genre':
                dict_genre.append(l[0].strip())
            elif l[1].strip() == 'material':
                dict_material.append(l[0].strip())
            elif l[1].strip() == 'sent':
                dict_sent.append(l[0].strip())
        f.close()

    dictList.append(dict_character)
    dictList.append(dict_class)
    dictList.append(dict_genre)
    dictList.append(dict_material)
    dictList.append(dict_sent)
    
    return dictList

# 개체명 인식
def named_entity(query, dictList):
    NE = []
    for i in dictList[0]:
        if i in query:
            ne = {"word": i, "label": "character"}
            NE.append(ne)

    for i in dictList[1]:
        if i in query:
            ne = {"word": i, "label": "class"}
            NE.append(ne)

    for i in dictList[2]:
        if i in query:
            ne = {"word": i, "label": "genre"}
            NE.append(ne)

    for i in dictList[3]:
        if i in query:
            ne = {"word": i, "label": "material"}
            NE.append(ne)

    for i in dictList[4]:
        if i in query:
            ne = {"word": i, "label": "sent"}
            NE.append(ne)

    return NE

# 학습할 데이터 파일 다운로드
# urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="ratings_train.txt")
# urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="ratings_test.txt")

# 데이터 파일에서 내용 추출

# 데이터 파일 형태
# id document label

# 해당 파일에서 document 부분만 추출

def data_extraction(input_files):
    all_data = []

#    filelist = input_files.split(',')

    for i in input_files:
        f = open(i.strip(), 'r')
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            all_data.append(l[1])
        f.close()

    return all_data

# 문장을 사전 정보 별로 분류
# 분류한 문장들에 대하여 레이블을 붙이기

def labeling(input_data, dictList):
    character_data = []   # 인물 정보가 포함된 문장
    class_data = []       # 클래스 정보가 포함된 문장
    genre_data = []       # 장르 정보가 포함된 문장
    material_data = []    # 소재 정보가 포함된 문장
    sent_data = []        # 감정 정보가 포함된 문장

    character_label = []
    class_label = []
    genre_label = []
    material_label = []
    sent_label = []

    for i in input_data:
        for j in dictList[0]:
            if i.find(j) != -1:
                character_data.append(i)
                break
        for j in dictList[1]:
            if i.find(j) != -1:
                class_data.append(i)
                break
        for j in dictList[2]:
            if i.find(j) != -1:
                genre_data.append(i)
                break
        for j in dictList[3]:
            if i.find(j) != -1:
                material_data.append(i)
                break
        for j in dictList[4]:
            if i.find(j) != -1:
                sent_data.append(i)
                break

    for _ in range(len(character_data)):
        character_label.append(0)
    print("인물 레이블 수: ", len(character_label))

    for _ in range(len(class_data)):
        class_label.append(1)
    print("클래스 레이블 수: ", len(class_label))

    for _ in range(len(genre_data)):
        genre_label.append(2)
    print("장르 레이블 수: ", len(genre_label))

    for _ in range(len(material_data)):
        material_label.append(3)
    print("소재 레이블 수: ", len(material_label))

    for _ in range(len(sent_data)):
        sent_label.append(4)
    print("감정 레이블 수: ", len(sent_label))

    train_df = pd.DataFrame({'text':character_data + class_data + genre_data + material_data + sent_data,
                             'label':character_label + class_label + genre_label + material_label + sent_label})

    print(train_df.head())
    print(train_df.tail())

    # 분류한 문장들을 저장
#    train_df.to_csv(output_data, index=False)
    return train_df


def token_length_calc(data):
    # 분류한 문장 호출
#    data = pd.read_csv(input_data)

    # 토크나이저 설정
    tokenizer = Komoran()


    # 형태소 분석 진행
    data_tokenized = [[token+"/"+POS for token, POS in tokenizer.pos(text_)] for text_ in data['text']]

    exclusion_tags = [
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', # 주격조사, 보격조사, 관형격조사, 목적격조사, 부사격조사, 호격조사, 인용격조사
            'JX', 'JC',                                      # 보조사, 접속조사
            'SF', 'SP', 'SS', 'SE', 'SO',                    # 마침표,물음표,느낌표(SF), 쉼표,가운뎃점,콜론,빗금(SP), 따옴표,괄호표,줄표(SS), 줄임표(SE), 붙임표(물결,숨김,빠짐)(SO)
            'EP', 'EF', 'EC', 'ETN', 'ETM',                  # 선어말어미, 종결어미, 연결어미, 명사형전성어미, 관형형전성어미
            'XSN', 'XSV', 'XSA'                              # 명사파생접미사, 동사파생접미사, 형용사파생접미사
    ]

    f = lambda x: x in exclusion_tags

    # 제외 태그에 포함된 내용을 제외한 뒤 저장
    data_list = []
    for i in range(len(data_tokenized)):
        temp = []
        for j in range(len(data_tokenized[i])):
            if f(data_tokenized[i][j].split('/')[1]) is False:
                temp.append(data_tokenized[i][j].split('/')[0])
        data_list.append(temp)


    # 토큰 평균값, 최댓값, 표준편차 계산
    num_tokens = [len(tokens) for tokens in data_list]
    num_tokens = np.array(num_tokens)

    print(f"토큰 길이 평균: {np.mean(num_tokens)}")
    print(f"토큰 길이 최대: {np.max(num_tokens)}")
    print(f"토큰 길이 표준편차: {np.std(num_tokens)}")

    return data_list

# 샘플 길이 비율
def below_threshold_len(nested_list):
    max_len = 0

    while 1:
        cnt = 0
        for s in nested_list:
            if(len(s) <= max_len):
                cnt = cnt + 1

        if (cnt / len(nested_list)) > 0.995:
            break
        else:
            max_len = max_len + 1

    print('전체 샘플 중 샘플이 99.5% 이상 포함되는 최소 길이는 {}'.format(max_len))

    return max_len

def intent_classification_using_CNN(data, word2index_dic, userdic, MAX_SEQ_LEN, output_model_name):
    from utils.Preprocess import Preprocess
    # 데이터 불러오기
#    data = pd.read_csv(input_data)
    text = data['text'].tolist()
    label = data['label'].tolist()

    # preprocessor 호출
    p = Preprocess(word2index_dic=word2index_dic, userdic=userdic)

    # 전처리 작업
    sequences = []
    for sentence in text:
        pos = p.pos(sentence)
        keywords = p.get_keywords(pos, without_tag=True)
        seq = p.get_wordidx_sequence(keywords)
        sequences.append(seq)

    # 시퀀스 벡터 패딩 처리
    padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

    # tensor 객체 생성
    ds = tf.data.Dataset.from_tensor_slices((padded_seqs, label))
    ds = ds.shuffle(len(text))

    # train & validation & test 사이즈 설정
    train_size = int(len(padded_seqs) * 0.7)
    val_size = int(len(padded_seqs) * 0.2)
    test_size = int(len(padded_seqs) * 0.1)

    train_ds = ds.take(train_size).batch(100)
    val_ds = ds.take(train_size).take(val_size).batch(100)
    test_ds = ds.take(train_size + val_size).take(test_size).batch(100)

    # Hyperparameter 설정
    dropout_prob = 0.5
    EMB_SIZE = 128
    VOCAB_SIZE = len(p.word_index) + 1

    # CNN model 선언
    input_layer = Input(shape=(MAX_SEQ_LEN, ))
    embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
    dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)

    # CNN (3-gram)
    conv1 = Conv1D(
        filters=128,
        kernel_size=3,
        padding='valid',
        activation=tf.nn.relu)(dropout_emb)
    pool1 = GlobalMaxPool1D()(conv1)

    # CNN (4-gram)
    conv2 = Conv1D(
        filters=128,
        kernel_size=4,
        padding='valid',
        activation=tf.nn.relu)(dropout_emb)
    pool2 = GlobalMaxPool1D()(conv2)

    # CNN (5-gram)
    conv3 = Conv1D(
        filters=128,
        kernel_size=5,
        padding='valid',
        activation=tf.nn.relu)(dropout_emb)
    pool3 = GlobalMaxPool1D()(conv3)

    # 3,4,5-gram 합치기
    concat = concatenate([pool1, pool2, pool3])

    hidden = Dense(128, activation=tf.nn.relu)(concat)
    dropout_hidden = Dropout(rate=dropout_prob)(hidden)       # dropout 설정
    logits = Dense(5, name='logits')(dropout_hidden)          # 의도 클래스 분류를 위한 Dense 계층 생성
    predictions = Dense(5, activation=tf.nn.softmax)(logits)  # 확률 계산


    # CNN model 생성
    model = Model(inputs=input_layer, outputs=predictions)
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])


    # model 학습
    EPOCH = 10
    model.fit(train_ds, validation_data=val_ds, epochs=EPOCH, verbose=1)


    # model 평가
    loss, accuracy = model.evaluate(test_ds, verbose=1)
    print("Accuracy: %f" % (accuracy * 100))
    print("loss : %f" % (loss))

    # save model
    model.save(output_model_name)

if __name__ == '__main__':
    dictList = read_dict('dict/data/dict_character.txt', 'dict/data/dict_class.txt', 'dict/data/dict_genre.txt', 'dict/data/dict_material.txt', 'dict/data/dict_sent.txt')

    input_files = ['data/ratings_train.txt','data/ratings_test.txt']

    data = data_extraction(input_files)

    train_df = labeling(data, dictList)

    data_list = token_length_calc(train_df)

    length = below_threshold_len(data_list)
    print(length)

    intent_classification_using_CNN(train_df, 'train_tools/data/chatbot_dict.bin', 'dict/data/user_dic.txt', length, 'intent_model_241017.keras')

