# referred from https://www.kaggle.com/ngyptr/lstm-sentiment-analysis-keras

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re

data = pd.read_csv('train.csv',header=0, encoding = "utf-8")
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
X = pad_sequences(X)

print(X)

embed_dim = 128
lstm_out = 196

# train LSTM
model = Sequential()
model.add(Embedding(max_features, embed_dim,input_length = X.shape[1]))
model.add(SpatialDropout1D(0.4))
model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(2,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())

Y = pd.get_dummies(data['Insult']).values

batch_size = 32
model.fit(X, Y, epochs = 7, batch_size=batch_size, verbose = 2)

validation_data = pd.read_csv('test.csv',header=0, encoding = "utf-8")

# print(data)
validation_data = validation_data[['Insult','Comment']]
validation_data['Comment'] = validation_data['Comment'].apply(lambda x: x.lower())
validation_data['Comment'] = validation_data['Comment'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))

max_features = 2000
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(validation_data['Comment'].values)
X_validate = tokenizer.texts_to_sequences(validation_data['Comment'].values)
X_validate = pad_sequences(X_validate)
Y_validate = pd.get_dummies(validation_data['Insult']).values


score,acc = model.evaluate(X_validate, Y_validate, verbose = 2, batch_size = batch_size)
print("score: %.2f" % (score))
print("acc: %.2f" % (acc))
