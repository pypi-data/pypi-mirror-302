#model_traning.py
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

# Assuming you have code-comment pairs
X_train, X_test, y_train, y_test = train_test_split(code_texts, comments, test_size=0.2)

vectorizer = TfidfVectorizer()
X_train_vect = vectorizer.fit_transform(X_train)

model = LogisticRegression()
model.fit(X_train_vect, y_train)

# Make predictions
X_test_vect = vectorizer.transform(X_test)
print(model.score(X_test_vect, y_test))
