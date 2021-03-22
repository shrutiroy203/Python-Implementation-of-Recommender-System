# Launch with
## gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    return render_template('articles.html',articles=articles)


@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """

    #filenames = [a[0] for a in articles]
    #i = filenames.index(topic + '/' + filename)
    chosen_article=[x for x in articles if x[0]==str(topic+'/'+filename)]
    recommendations=recommended(chosen_article[0], articles, 5)
    return render_template('article.html',article=chosen_article[0],recommendations=recommendations)
     

# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)

