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
import re

data = pd.read_csv('train.csv',header=0, encoding = "utf-8")
# print(data)
data = data[['Insult','Comment']]
data['Comment'] = data['Comment'].apply(lambda x: x.lower())
data['Comment'] = data['Comment'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))
from nltk.tag import pos_tag
for index,sentence in enumerate(data['Comment']):
    tagged_sent = pos_tag(sentence.split())
    new_sent = []
    for word in tagged_sent:
        if word[1] != "DT":
            new_sent.append(word[0])
    data['Comment'][index] = ' '.join(word for word in new_sent)

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

inp = input("Train model? Y/N")

if inp == "Y":
    # train LSTM
    print("learn")
    model = Sequential()
    model.add(Embedding(max_features, embed_dim,input_length = X.shape[1]))
    model.add(SpatialDropout1D(0.4))
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(2,activation='softmax'))
    Y = pd.get_dummies(data['Insult']).values

    batch_size = 32
    model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
    model.fit(X, Y, epochs = 7, batch_size=batch_size, verbose = 2)
    model.save_weights('model_weights.h5')
    with open('model_architecture.json', 'w') as f:
        f.write(model.to_json())

    print("test the model")
    validation_data = pd.read_csv('test_with_solutions.csv',header=0, encoding = "utf-8")

    # print(data)
    validation_data = validation_data[['Insult','Comment']]
    validation_data['Comment'] = validation_data['Comment'].apply(lambda x: x.lower())
    validation_data['Comment'] = validation_data['Comment'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))
    for index,sentence in enumerate(validation_data['Comment']):
        tagged_sent = pos_tag(sentence.split())
        new_sent = []
        for word in tagged_sent:
            if word[1] != "DT":
                new_sent.append(word[0])
        validation_data['Comment'][index] = ' '.join(word for word in new_sent)

    max_features = 2000
    tokenizer = Tokenizer(num_words=max_features, split=' ')
    tokenizer.fit_on_texts(validation_data['Comment'].values)
    X_validate = tokenizer.texts_to_sequences(validation_data['Comment'].values)
    X_validate = pad_sequences(X_validate, maxlen=1689)
    Y_validate = pd.get_dummies(validation_data['Insult']).values
    score,acc = model.evaluate(X_validate, Y_validate, verbose = 2, batch_size = batch_size)
    print("score: %.2f" % (score))
    print("acc: %.2f" % (acc))

else:
    with open('model_architecture.json', 'r') as f:
        model = model_from_json(f.read())
    # Load weights into the new model
    model.load_weights('model_weights.h5')



print(model.summary())


while(True):
    twt = input("Enter the statement that you want to analyse for insults")
    tagged_sent = pos_tag(twt.split())
    new_sent = []
    for word in tagged_sent:
        if word[1] != "DT":
            new_sent.append(word[0])
    twt = ' '.join(word for word in new_sent)
    #vectorizing the tweet by the pre-fitted tokenizer instance
    twt = tokenizer.texts_to_sequences(twt)
    #padding the tweet to have exactly the same shape as `embedding_2` input
    twt = pad_sequences(twt, maxlen=1689, dtype='int32', value=0)
    print(twt)
    sentiment = model.predict(twt,batch_size=1,verbose = 2)[0]
    if(np.argmax(sentiment) == 1):
        print("Insult")
    elif (np.argmax(sentiment) == 0):
        print("Not an Insult")
