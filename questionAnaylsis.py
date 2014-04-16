import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.preprocessing import LabelBinarizer
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv("trainingData.csv")
#data = data[0:1000]

# print data
questionValues = data["Question"].values
text = data["Text"].values


print "Extracting TFIDF features"
featureExtractor = TfidfVectorizer()
featureExtractor.fit_transform(list(data["Text"]))

textTFIDF = featureExtractor.transform(list(data["Text"]))

train_categories, test_categories, train_questions, test_questions = train_test_split(
    textTFIDF, questionValues)

print train_questions.mean()
print test_questions.mean()

model = LogisticRegression(C=1)

print "Fitting the Model"

model.fit(train_categories, train_questions)
output = model.predict(test_categories)
print output
textFeaturesPerf = accuracy_score(test_questions, output)

print textFeaturesPerf
