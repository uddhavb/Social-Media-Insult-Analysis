from nltk.tag import pos_tag
from nltk.corpus import stopwords

# import time

stopwords_set = set(stopwords.words("english"))
print(stopwords_set)

with open('train.csv', 'r') as file1:
    with open('new_train.csv', 'w') as file2:
        line = file1.readline()
        while line:
            line.replace('_', ' ')
            line.replace("\\n", ' ')
            line.replace("\n", ' ')
            line.replace("\\x", ' ')
            line.replace("\\xa0", ' ')
            line.replace("xa0", ' ')
            line.replace("\\xc2", ' ')
            line.replace("xa0", ' ')

            line = line.split()
            new_line = []
            for word in line:
                if word not in stopwords_set:
                    new_line.append(word)
            new_line = ' '.join(word for word in new_line)
            # print(new_line)
            # time.sleep(1)
            file2.write(new_line+"\n")
            line = file1.readline()

with open('test_with_solutions.csv', 'r') as file1:
    with open('new_test_with_solutions.csv', 'w') as file2:
        line = file1.readline()
        while line:
            line.replace('_', ' ')
            line.replace("\\n", ' ')
            line.replace("\n", ' ')
            line.replace("\\x", ' ')
            line.replace("\\xa0", ' ')
            line.replace("xa0", ' ')
            line.replace("\\xc2", ' ')
            line.replace("xa0", ' ')

            line = line.split()
            new_line = []
            for word in line:
                if word not in stopwords_set:
                    new_line.append(word)
            new_line = ' '.join(word for word in new_line)
            # print(new_line)
            # time.sleep(1)
            file2.write(new_line+"\n")
            line = file1.readline()
