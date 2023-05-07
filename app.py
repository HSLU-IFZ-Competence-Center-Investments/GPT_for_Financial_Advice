#from flask import Flask

## Create an instance of the Flask class that is the WSGI application.
## The first argument is the name of the application module or package,
## typically __name__ when using a single module.
#app = Flask(__name__)

## Flask route decorators map / and /hello to the hello function.
## To add other resources, create functions that generate the page contents
## and add decorators to define the appropriate resource locators for them.

#@app.route('/')
#@app.route('/hello')
#def hello():
#    # Render the page
#    return "Hello Python!"

#if __name__ == '__main__':
#    # Run the app server on localhost:4449
#    app.run('localhost', 4449)

from flask import Flask, render_template, request
from win32api import GenerateConsoleCtrlEvent
import nltk,os,openai,time

from utils import AdvisorGPT
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pandas as pd



app = Flask(__name__)
app.static_folder = 'static'

chat_limit = 100
openai.api_key = open("key.txt", "r").read().strip("\n")
advisor = AdvisorGPT(chat_limit=chat_limit)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response(user_input=None):
    user_input = request.args.get('msg') if user_input is None else user_input
    try:
        return advisor.respond(user_input)
    except openai.error.RateLimitError:
        pop_up('Rate limit exceeded. I will be back shortly, please wait for a minute.')
        time.sleep(60)
        get_bot_response(user_input)
    # AuthenticationError
    except openai.error.AuthenticationError as e:
        pop_up(e)
def stop():
    CTRL_C_EVENT = 0
    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)
    os._exit(0)

def pop_up(text1):
    return render_template("popup.html")

if __name__ == "__main__":
    app.run('localhost', 4449)
