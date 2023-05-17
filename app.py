# Author: Ahmet Ege Yilmaz
# Year: 2023

import openai,pickle,re
import numpy as np
import pandas as pd
from typing import Optional

class ChatLimitError(Exception):
    pass

class ChatSession:
    
    """
        Important Note: If you ask for log probabilities, 
                        it uses the davinci model, which has a cost rate 10 times more than gpt-3.5.
                        Also, if you ask for the top 5 most probable words for a text with 10 words,
                        it charges for 50 words.
    """

    completions = {
            1:dict(
                completion=openai.ChatCompletion,model="gpt-3.5-turbo",text='message.content',prompt='messages'
            ),
            0:dict(
                completion=openai.Completion,model="text-davinci-003",text='text',prompt='prompt'
            )
        }
    
    def __init__(self,gpt_name='GPT') -> None:
        
        # History of all messages in the chat.
        self.messages = []

        # History of completions by the model.
        self.history = []

        # The name of the model.
        self.gpt_name=gpt_name

    def chat(self,user_input:None,verbose=True,*args,**kwargs):
        """ Say something to the model and get a reply. """
        
        completion_index = 0 if kwargs.get('logprobs',False) or kwargs.get('model')=='text-davinci-003' else 1
        
        completion = self.completions[completion_index]

        user_input = self.__get_input(user_input=user_input,log=True)
        user_input = self.messages if completion_index else self.messages[-1]['content']
        
        kwargs.update({completion['prompt']:user_input,\
                       'model':completion['model']})
        
        self.__get_reply(completion=completion['completion'],log=True,*args,**kwargs)

        self.history[-1].update({'completion_index':completion_index})
        
        if verbose:
            self.__call__(1)
    
    def display_probas(self,reply_index):
        """ Display probabilities of each word for the given reply by the model. """

        history = self.history[reply_index]
        assert not history.completion_index
        probas = history.logprobs.top_logprobs
        return pd.concat([
                pd.DataFrame(data=np.concatenate([[list(k.keys()), np.exp2(list(k.values())).round(2)]]).T, \
                                columns=[str(i),f'{i}_proba'], \
                                    index=[f'candidate_{j}' for j in range(len(probas[0]))] \
                            ) for i,k in enumerate(probas)],axis=1).T
    
    def inject(self,line,role):
        """ Inject lines into the chat. """

        self.__log(message={"role": role, "content": line})

    def clear(self,k=None):
        """ Clears session. If provided, last k messages are cleared. """
        if k:
            self.messages = self.messages[:-k]
            self.history = self.history[:-k]
        else:
            self.__init__()

    def save(self,filename):
        """ Saves the session to file. """

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def load(self,filename):
        """ Loads up the session. """

        with open(filename, 'rb') as f:
            temp = pickle.load(f)
            self.messages = temp.messages
            self.history = temp.history
    
    def merge(self,filename):
        """ Merges another session from file with this one. """

        with open(filename, 'rb') as f:
            temp = pickle.load(f)
            self.messages += temp.messages
            self.history += temp.history

    def __get_input(self,user_input,log:bool=False):
        """ Converts user input to desired format. """

        if user_input is None:
            user_input = input("> ")
        if not isinstance(user_input,dict): 
            user_input = {"role": 'user', "content": user_input}
        if log:
            self.__log(user_input)
        return user_input

    def __get_reply(self,completion,log:bool=False,*args,**kwargs):
        """ Calls the model. """
        reply = completion.create(*args,**kwargs).choices[0]
        if log:
            if hasattr(reply,'message'):
                self.__log(message=reply.message,history=reply)
            else:
                self.__log(message={"role": 'assistant', "content": reply.text},history=reply)
        return reply
    
    def __log(self,message:dict,history=None):
        self.messages.append(message)
        if history is not None:
            assert isinstance(history,dict)
            self.history.append(history)

    def __call__(self,k:Optional[int]=None):
        """ Display full chat log or last k messages. """

        k = len(self.messages) if k is None else k
        for msg in self.messages[-k:]:
            message = msg['content']
            who = {'user':'User: ','assistant':f'{self.gpt_name}: '}[msg['role']]
            print(who + message.strip() + '\n')



# 2) Rule based system.

## 2.1) Read in rule based system.
RuleBasedPortfolios = pd.DataFrame.from_dict({'age': {0: 'no',
  1: 'no',
  2: 'no',
  3: 'no',
  4: 'yes',
  5: 'yes',
  6: 'yes',
  7: 'yes'},
 'income': {0: 'yes',
  1: 'yes',
  2: 'no',
  3: 'no',
  4: 'yes',
  5: 'yes',
  6: 'no',
  7: 'no'},
 'risk appetite': {0: 'yes',
  1: 'no',
  2: 'yes',
  3: 'no',
  4: 'yes',
  5: 'no',
  6: 'yes',
  7: 'no'},
 'portfolio': {0: 1, 1: 2, 2: 1, 3: 1, 4: 2, 5: 2, 6: 1, 7: 2}})

## 2.3) Questions need to be crafted, allowing SupervisorGPT to navigate through the rule based system and reach a portfolio recommendation.
investor_profile = {i:None for i in ['age','income','risk appetite']}
questions = [
        'Based on our conversation so far, am I 51 years old or older? Yes or no:',\
        'Based on our conversation so far, calculate my annual income. Is it less than 100K? Yes or no:',\
        'Based on our conversation so far, do I have a high risk appetite? Yes or no:'
    ]
questions = {i:k for i,k in zip(investor_profile,questions)}

class AdvisorGPT(ChatSession):
    def __init__(self, chat_limit, gpt_name='Advisor') -> None:
        ## 3.1) Initialize the AdvisorGPT.
        super().__init__(gpt_name)


        ## 2.2) The attributes of the investor profile. They need to be consistent with the columns of RuleBasedPortfolios.
        self.investor_profile = investor_profile.copy()
        self.ask_for_these = [i for i in self.investor_profile if not self.investor_profile[i]]

        self.loop_no=0
        self.threshold = chat_limit
        
        ## 3.2) Instruct GPT to become a financial advisor.
        self.inject(line="You are a financial advisor at a bank. You must ask specifically what the customers' age, annual income and risk appetite is. Be subtle about asking for these information and\
                                do not ask at the very beginning of the conversation. Always prioritize answering the customers' questions\
                                over asking for these information. Do not recommend a specific portfolio before you gathered these information.\
                                I am a customer seeking financial advise from you. Say ok if you understand.",role="user")
        self.inject(line="Ok.",role= "assistant")

        self.session_completed = False

    def respond(self,user_input):
        if self.loop_no >= self.threshold:
            raise ChatLimitError('Chat limit exceeded. Session ended.')
        if re.search('[\w?]+',user_input) is None and self.loop_no>0:
            return 'I am sorry. I did not quite get that.'
        self.inject(line=user_input,role='user')
        self.update_investor_profile(verbose=False)
        self.loop_no += 1
        if len(self.ask_for_these):
            # self.inject(line=f"*I must ask about the customer's {', '.join(ask_for_these)}...*",role="assistant")
            if self.loop_no > 5:
                self.inject(line=f"*I am still not sure what the customer's {', '.join(self.ask_for_these)} is. I must ask for these...*",role="assistant")
        else:
            self.session_completed = True
            ### 3.3.5) Get rule based portfolio by using ``investor_profile``
            portfolio = RuleBasedPortfolios.where(lambda x: x['age'].apply(lambda y: y in self.investor_profile['age'].lower())*\
                                        x['income'].apply(lambda y: y in self.investor_profile['income'].lower())*\
                                            x['risk appetite'].apply(lambda y: y in self.investor_profile['risk appetite'].lower()))['portfolio'].dropna().values
            assert portfolio.size == 1
            portfolio = int(portfolio.item())

            ### 3.3.6) Tell GPT to recommend portfolio
            self.inject(line=f"Then, I would recommend portfolio {portfolio}.",role= "assistant")
            return self.messages[-1]['content']

        self.chat(user_input='',verbose=False)
        return self.messages[-1]['content']

   
    def update_investor_profile(self,verbose:bool=False):

        self.ask_for_these = [i for i in self.investor_profile if not self.investor_profile[i]]
        n_limit = 20
        temp_reply = openai.ChatCompletion.create(messages=self.messages.copy(),model='gpt-3.5-turbo').choices[0].message.content
        for info_type in self.ask_for_these:
            choices = [*map(lambda x:x.message.content,openai.ChatCompletion.create(messages=
                                                self.messages+\
                                                # [{"role": "assistant", "content":'Understood.'}]+\
                                                [{"role": "assistant", "content":temp_reply}]+\
                                                [{"role": "user", "content": f'Do you know my {info_type} based on our conversation so far? Yes or no:'}],\
                                                model='gpt-3.5-turbo',n=n_limit,max_tokens=1).choices)]
            if verbose:
                print('1:')
                print({i:round(choices.count(i)/len(choices),2) for i in pd.unique(choices)})
            if np.any([*map(lambda x: 'yes' in x.lower(),choices)]):
                choices = [*map(lambda x:x.message.content,openai.ChatCompletion.create(messages=\
                                            self.messages+\
                                            # [{"role": "assistant", "content": 'Understood.'}]+\
                                            [{"role": "assistant", "content":temp_reply}]+\
                                            [{"role": "user", "content": questions[info_type]}],\
                                            model='gpt-3.5-turbo',n=n_limit,max_tokens=1).choices)]
                if verbose:
                    print('2:')
                    print({i:round(choices.count(i)/len(choices),2) for i in pd.unique(choices)})
                if np.any([*map(lambda x: 'yes' in x.lower(),choices)]):
                    self.investor_profile[info_type] = 'yes'
                elif np.any([*map(lambda x: 'no' in x.lower(),choices)]):
                    self.investor_profile[info_type] = 'no'
        self.ask_for_these = [i for i in self.investor_profile if not self.investor_profile[i]]

from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

chat_limit = 20


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
    openai.api_key = None
    return "Chat started."


@app.route("/key")
def set_key():
    openai.api_key = request.args.get('key')
    return "Key set."

if __name__ == "__main__":
    # app.run('localhost', 4449)
    app.run()