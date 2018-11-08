# Social Media Insult Analysis  
Analyzing people's posts and comments on whether they are insulting to other or not

## Progress  
For learning our model we are using the Kaggle dataset on social media comments and their classification as insulting or not insulting. The [data](https://www.kaggle.com/c/detecting-insults-in-social-commentary/data) used has substantial amount of entries for our learning needs.   

We are using the [Long Short-term Memory(LSTM)](https://en.wikipedia.org/wiki/Long_short-term_memory) network which is a form of recurrent neural networks. We chose this algorithm as it seems to give some of the best results in the field of Natural Language Processing and especially for our need of sentiment analysis.  

We are using Keras, a Python deep learning library that runs on top of Tensorflow and referred to this Kaggle [notebook](https://www.kaggle.com/ngyptr/lstm-sentiment-analysis-keras). The data is being read from a CSV and tokenized using Keras' tokenizer library and chossing only the most relevant words in the all of the texts for our further learning.   

Using this processed data we are passing it into the training algorithm to fit the model. We are currently working on tuning the parameters in the model to get the best results for our application. 
