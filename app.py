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
#from win32api import GenerateConsoleCtrlEvent
import nltk,openai

from utils import AdvisorGPT,ChatLimitError
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()



app = Flask(__name__)
app.static_folder = 'static'

chat_limit = 20
try:
    openai.api_key = open("key.txt", "r").read().strip("\n")
except:
    pass

advisor = AdvisorGPT(chat_limit=chat_limit)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    try:
        return advisor.respond(user_input)
    except openai.error.RateLimitError:
        return 'Error1: Rate limit exceeded, please wait for a minute.'
    except openai.error.AuthenticationError:
        return "Error2: Authentication error. Please enter your API key."
    except ChatLimitError:
        return 'Error3: Chat limit exceeded.'
    except Exception as e:
        return "Error: " + 'Connection failed. Please start a new chat.'

@app.route("/start")
def start():
    advisor.__init__(chat_limit=chat_limit)
    return "Chat started."

#@app.route("/stop")
#def stop():
#    CTRL_C_EVENT = 0
#    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)
#    os._exit(0)

@app.route("/key")
def set_key():
    openai.api_key = request.args.get('key')
    return "Key set."

if __name__ == "__main__":
    app.run('localhost', 4449)
