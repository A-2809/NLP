# -*- coding: utf-8 -*-
"""NLP_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17lY2saWDiPM67qN-_Y2Nn7euaDhBS5cJ

# Project 6: Consumer Complaint Classification

Name of team members: Akansha Singh
                      Archana Yadav
                      Yashika Patil
"""

#mount the drive
from google.colab import drive
drive.mount('/content/drive')

#importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn

#importing the training dataset (My Drive -> NLP_Project_Data(Folder) -> training_data/test_data)

train = pd.read_csv (r'/content/drive/MyDrive/NLP_Project_Data/training_data.csv', names=['Complaint', 'Category'])
test = pd.read_csv (r'/content/drive/MyDrive/NLP_Project_Data/test_data.csv')
train

"""## Data Cleaning"""

#number of unique category

train['Category'].unique()

#Checking for NaN values

train.isnull().sum()

#removing the NaN/NULL value

train.dropna(how='any',axis=0, inplace = True) 
train

"""## Exploratory Data Analysis"""

grouped_by_class = train.groupby('Category').count()
grouped_by_class

category = ['retail_banking', 'credit_reporting', 'mortgages_and_loans','debt_collection', 'credit_card']
complaint = [15177, 88892, 22569, 18515, 13197]

# creating the bar plot

fig = plt.figure(figsize = (9, 4))
plt.bar(category, complaint, width=0.4)
plt.xlabel("Category")
plt.ylabel("Frequency")
plt.title("Label Frequency")
plt.show()

# creating the pie chart

fig = plt.figure(figsize = (7, 6))
plt.pie(complaint,labels=category, startangle=90, shadow=True,explode=(0.1, 0.1, 0.1, 0.1,0.1), autopct='%1.2f%%')
plt.title("Label Frequency")
plt.axis('equal')
plt.show()

# making word cloud

for product_name in train['Category'].unique():
    print(" \n Category: ", product_name)
    print("\n")

    all_words = ' '.join([text for text in train.loc[train['Category'].str.contains(product_name),'Complaint']])

    from wordcloud import WordCloud
    wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

"""# 1. Text Pre-processing Techniques:"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize, TreebankWordTokenizer, TweetTokenizer, MWETokenizer
from nltk.corpus import stopwords
from nltk import ngrams
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

"""### 1.1. Punctuation Removal"""

import string

#defining the function to remove punctuation
def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

#storing the puntuation free text
train['Cleaned_Text']= train['Complaint'].apply(lambda x:remove_punctuation(x))

train

"""### 1.2. Lowercase"""

train['Lowercase_Text']= train['Cleaned_Text'].apply(lambda x: x.lower())

train

"""###1.3. Tokenisation"""

#defining function for tokenization
def tokenization(text):
    #tokens = re.split('W+',text)
    tokens = TreebankWordTokenizer().tokenize(text)
    return tokens

#applying function to the column
train['Tokenised_Text']= train['Lowercase_Text'].apply(lambda x: tokenization(x))

train.head()

"""###1.4. Stopword Removal"""

nltk.download('stopwords')

#Stop words present in the library
stopwords = nltk.corpus.stopwords.words('english')

#defining the function to remove stopwords from tokenized text
def remove_stopwords(text):
    output= [i for i in text if i not in stopwords]
    return output

#applying the function
train['No_Stopwords']= train['Tokenised_Text'].apply(lambda x:remove_stopwords(x))

train

"""###1.5. Stemming"""

# from sklearn.base import TransformerMixin
# importing the Stemming function from nltk library
from nltk.stem.porter import PorterStemmer

porter_stemmer = PorterStemmer()

# defining a function for stemming
def stemming(text):
    stem_text = [porter_stemmer.stem(word) for word in text]
    return stem_text

# applying the function
train['Stemmed_Text']=train['No_Stopwords'].apply(lambda x: stemming(x))

train

"""###1.6.Lemmatization"""

nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

#defining the object for Lemmatization
wordnet_lemmatizer = WordNetLemmatizer()

#defining the function for lemmatization
def lemmatizer(text):
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text

#applying the function
train['Lemmatized_Text']=train['Stemmed_Text'].apply(lambda x:lemmatizer(x))

train

"""### 1.7. Bag of Words

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
# Create sample set of documents
docs = train

# Fit the bag-of-words model
bag = vectorizer.fit_transform(docs)

# Get unique words / tokens found in all the documents. The unique words / tokens represents the features
print(vectorizer.get_feature_names())

# Associate the indices with each unique word
print(vectorizer.vocabulary_)

# Print the numerical feature vector
print(bag.toarray())
"""

import gensim
from gensim.models import Word2Vec
data = train['Lemmatized_Text']
# Create CBOW model
model1 = gensim.models.Word2Vec(data, min_count = 1, window = 5)
 
# Print results
print("Cosine similarity between 'credit' " +
               "and 'letter' - CBOW : ",
    model1.wv.similarity('credit', 'letter'))

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
 
vectorizer = CountVectorizer()

# Create sample set of documents
docs = train['Lemmatized_Text']

# Fit the bag-of-words model
bag = vectorizer.fit_transform(docs)

# Get unique words / tokens found in all the documents. The unique words / tokens represent the features
print(vectorizer.get_feature_names())

# Associate the indices with each unique word
print(vectorizer.vocabulary_)

# Print the numerical feature vector
print(bag.toarray())

"""from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(train['Lowercase_Text'])

#create dataframe
cv_dataframe=pd.DataFrame(X.toarray(),columns=vectorizer.get_feature_names())
print(cv_dataframe)"""

# Term Frequency
CountVec = CountVectorizer(stop_words='english',ngram_range=(1,3))

# Transform
Count_data = CountVec.fit_transform([data])
print(CountVec.get_feature_names())

#create dataframe
cv_dataframe=pd.DataFrame(Count_data.toarray(),columns=CountVec.get_feature_names())
print(cv_dataframe)

"""## 2. Text Classification"""

import csv
import sys
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV 
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn import svm 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_selection import SelectKBest,chi2

"""### 2.1 Without using NLP

### 2.2 Without parameter tuning

### 2.3. With parameter tuning
"""

from sklearn.model_selection import train_test_split

data = train['Lemmatized_Text']
labels = train['Category']
train_data, test_data, train_cat, test_cat = train_test_split(data, labels, test_size=0.20, random_state=42,stratify=labels)

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

model_params = {
    
    'naive_bayes_gaussian': {
        'model': GaussianNB(),
        'params': {
            'var_smoothing' : [1e-15, 1e-13, 1e-11, 1e-9, 1e-7, 1e-5, 1e-3]
        }
    },

    'logistic_regression' : {
        'model': LogisticRegression(),
        'params': {
            'C': [1e-2, 1e-1, 1 ,5 ,10],
            'solver': ['liblinear','netwon-cg', 'lbfgs']
        }
    },

    'knn_classifier': {
        'model': KNeighborsClassifier(),
        'params': {
            'n_neighbors': [1, 3, 5, 7, 9],
            'weights': ['uniform', 'distance'],
            'metric': ['minkowski', 'manhattan']
        }
    }     
}

scores = []
labels = train['Lemmatized_Text']

for model_name, mp in model_params.items():
    clf =  GridSearchCV(mp['model'], mp['params'], cv=5, return_train_score=False)
    clf.fit(data, labels)
    scores.append({
        'model': model_name,
        'best_score': clf.best_score_,
        'best_params': clf.best_params_
    })
    
df = pd.DataFrame(scores,columns=['model','best_score','best_params'])
df

predicted = clf.predict(test)

# Evaluation
print('\n Total documents in the training set: '+str(len(data))+'\n')    
print('\n Total documents in the test set: '+str(len(test))+'\n')
print ('\n Confusion Matrix \n')  
print (confusion_matrix(test, predicted))  

pr=precision_score(test, predicted, average='binary') 
print ('\n Precision:'+str(pr)) 

rl=recall_score(test, predicted, average='binary') 
print ('\n Recall:'+str(rl))

fm=f1_score(test, predicted, average='binary') 
print ('\n Micro Averaged F1-Score:'+str(fm))
