import tensorflow as tf
from keras.models import Model, load_model
from keras import preprocessing
import gc

# 의도 분류 모델 모듈
class IntentModel:
    def __init__(self, model_name, preprocess, MAX_SEQ_LEN):

        # 의도 클래스별 레이블블
        self.labels = {0: "character", 1: "class", 2: "genre", 3: "material" , 4: "sent"}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 텍스트 전처리기
        self.p = preprocess

        self.MAX_SEQ_LEN = MAX_SEQ_LEN

    # 의도 클래스 예측
    def classify(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=self.MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)

        print('character:', predict[0][0])
        print('class:', predict[0][1])
        print('genre:', predict[0][2])
        print('material:', predict[0][3])
        print('sent:', predict[0][4])
        return predict

    def predict_class(self, predict):
        predict_class = tf.math.argmax(predict, axis=1)
        
        return predict_class.numpy()[0]
