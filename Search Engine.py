from flask import Flask, render_template, request
import os
import re

app = Flask(__name__)

doclist = []
doc_dir = "docs"
filelist = os.listdir(doc_dir)
stopwords = open('dutch.txt', "r").read().split('\n')

for filename in filelist:
    with open(os.path.join(doc_dir, filename), "r") as file:
        doc_content = file.read()
        querywords = doc_content.split()
        resultwords = [word for word in querywords if word.lower() not in stopwords]
        cleaned_text = ' '.join(resultwords).lower()
        doclist.append(cleaned_text)

def search(query):
    query_words = set(re.split(r'\W+', query.lower()))
    results = []
    for doc, text in zip(filelist, doclist):
        word_counts = text.split()
        match_score = sum(word_counts.count(word) for word in query_words)
        if match_score > 0:
            results.append((doc, match_score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('query', '')
    results = search(query) if query else []
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
