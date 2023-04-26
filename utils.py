# Author: Ahmet Ege Yilmaz
# Year: 2023

import openai,pickle
import numpy as np
import pandas as pd
from typing import Optional

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

        self.gpt_name=gpt_name

    def chat(self,user_input:Optional[dict|str]=None,verbose=True,*args,**kwargs):
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


    def clear(self):
        """ Clears session. """

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

def update_investor_profile(investor_profile:dict,dialogue:str):

    ask_for_these = [i for i in investor_profile if not investor_profile[i]]

    questions = [
        'Is the Customer 51 years old or older? Answer by saying yes or no.',\
        'If the annual income of the Customer is not given as annual income, convert it to annual income. Is it less than 100K annually? Answer by saying yes or no.',\
        'Does the Customer have a high risk appetite? Answer by saying yes or no.'
    ]

    questions = {i:k for i,k in zip(investor_profile,questions)}

    for info_type in ask_for_these:
        sentiment = None
        messages = []
        messages.append({"role": "user", "content": f"Tell me whether the customer specifies his {info_type} in the following dialogue by saying yes or no:" + dialogue})
        limit = 20
        while sentiment is None:
            messages.append(openai.ChatCompletion.create(\
                                messages=messages,\
                                    model="gpt-3.5-turbo",max_tokens=1).choices[0].message)
            # print('1',messages[-1].content)
            if 'yes' in messages[-1].content.lower():
                sentiment = 'positive'
            elif 'no' in messages[-1].content.lower():
                sentiment = 'negative'
            elif limit <= 0:
                raise Exception('Something went wrong. Please try again.')
            else:
                messages.pop(-1)
            limit -= 1
        if sentiment == 'positive': 
            messages.append({"role": "user", "content": questions[info_type]})
            sentiment = None
            limit = 20    
            while sentiment is None:
                messages.append(openai.ChatCompletion.create(\
                                    messages=messages,\
                                        model="gpt-3.5-turbo",\
                                            max_tokens=1,\
                                            # temperature=0\
                                                ).choices[0].message)
                # print('2',messages[-1].content)
                if 'yes' in messages[-1].content.lower():
                    sentiment = 'positive'
                elif 'no' in messages[-1].content.lower():
                    sentiment = 'negative'
                elif limit <= 0:
                    break
                else:
                    messages.pop(-1)
                limit -= 1
            if sentiment is not None:
                investor_profile[info_type] = 'yes' if sentiment == 'positive' else 'no'
