# 단어 사전 파일 생성 코드입니다.
# 챗봇에 사용하는 사전 파일

import sys, os
import argparse
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils.Preprocess import Preprocess
from keras import preprocessing
import pickle
import pandas as pd

def create_dict(input_files, output_file, user_dic_file):

    # 말뭉치 데이터 읽어오기
    corpus_data = []

#    filelist = input_files.split(',')

    for i in input_files:
        f = open(i.strip(), 'r')
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            corpus_data.append(l[1])
        f.close()

    # 말뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성
    p = Preprocess(word2index_dic="", userdic = user_dic_file)
    dict = []
    for c in corpus_data:
        pos = p.pos(c)
        for k in pos:
            dict.append(k[0])

    # 사전에 사용될 word2index 생성
    # 사전의 첫 번째 인덱스에는 OOV 사용
    tokenizer = preprocessing.text.Tokenizer(oov_token='OOV', num_words=100000)
    tokenizer.fit_on_texts(dict)
    word_index = tokenizer.word_index
    print(len(word_index))

    # 사전 파일 생성
    f = open(output_file, "wb")
    try:
        pickle.dump(word_index, f)
    except Exception as e:
        print(e)
    finally:
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='create_dict')

    parser.add_argument('-i', '--inputfile', nargs='+')
    parser.add_argument('-o', '--outputfile')
    parser.add_argument('-u', '--userdic')
    args = parser.parse_args()

#    input_files = sys.argv[1]
#    output_file = sys.argv[2]

    create_dict(args.inputfile, args.outputfile, args.userdic)

