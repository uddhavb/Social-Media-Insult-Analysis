import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.models import model_from_json
from keras.utils.np_utils import to_categorical
from nltk.corpus import stopwords
import re
import sys, os, re, csv, codecs, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model
from keras import initializers, regularizers, constraints, optimizers, layers
stopwords_set = set(stopwords.words("english"))
data = pd.read_csv('new_train.csv',header=0, encoding = "utf-8")
# print(data)
data = data[['Insult','Comment']]
data['Comment'] = data['Comment'].apply(lambda x: x.lower())
data['Comment'] = data['Comment'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))

print(data[ data['Insult'] == 1].size)
print(data[ data['Insult'] == 0].size)

max_features = 2000
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(data['Comment'].values)
X = tokenizer.texts_to_sequences(data['Comment'].values)
totalNumWords = [len(one_comment) for one_comment in X]
# import matplotlib.pyplot as plt
# plt.hist(totalNumWords,bins = np.arange(0,410,10))#[0,50,100,150,200,250,300,350,400])#,450,500,550,600,650,700,750,800,850,900])
# plt.show()
X = pad_sequences(X, maxlen=100)

print(X)

embed_dim = 128
lstm_out = 60

inp = input("Train model? Y/N : ")

if inp == "Y":
    # train LSTM
    print("learn")
    Y = data['Insult'].values
    print("Y:",Y)
    maxlen=100
    inp = Input(shape=(maxlen, )) #maxlen=200 as defined earlier
    x = Embedding(max_features, embed_dim)(inp)
    x = LSTM(60, return_sequences=True,name='lstm_layer')(x)
    x = GlobalMaxPool1D()(x)
    x = Dropout(0.1)(x)
    x = Dense(50, activation="relu")(x)
    x = Dropout(0.1)(x)
    x = Dense(1, activation="sigmoid")(x)
    model = Model(inputs=inp, outputs=x)
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    batch_size = 32
    model.fit(X,Y, batch_size=batch_size, epochs=20, validation_split=0.1)
    model.summary()
    model.save('model-new.h5')


else:
    from keras.models import load_model
    model = load_model('model-new.h5')
print(model.summary())


while(True):
    text = input("Enter the statement that you want to analyse for insults : ")
    text = text.lower()
    text = re.sub(r'[^a-zA-z0-9\s]','',text)
    print(text)
    tagged_sent = text.split()
    new_sent = []
    for word in tagged_sent:
        if word not in stopwords_set:
            new_sent.append(word)
    text = ' '.join(word for word in new_sent)
    if len(text) == 0:
        print("---------------Not an Insult")
    else:
        #vectorizing the tweet by the pre-fitted tokenizer instance
        text = tokenizer.texts_to_sequences(text)
        #padding the tweet to have exactly the same shape as `embedding_2` input
        text = pad_sequences(text, maxlen=100)
        # print(text)
        sentiment = model.predict(text,batch_size=32,verbose = 2)
        print(sentiment)
        sentiment = sentiment[0]
        print(np.argmax(sentiment))
        if(np.argmax(sentiment) == 1):
            print("Insult")
        elif (np.argmax(sentiment) == 0):
            print("Not an Insult")
