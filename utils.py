import openai,pickle
import numpy as np
import pandas as pd
from operator import attrgetter
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
    
    def __init__(self) -> None:

        self.messages = []
        self.history = []
    
    def chat(self,user_input:Optional[dict|str]=None,*args,**kwargs):
        """ Say something to the model and get a reply. """
        completion_index = 0 if kwargs.get('logprobs',False) else 1

        if user_input is None:
            user_input = input("> ")
        
        if isinstance(user_input,dict):
            assert completion_index, "Dictionary input style only supported for ChatCompletion and not Completion."
            self.messages.append(user_input)
            message = self.messages
        else:
            self.messages.append({"role": "user", "content": user_input})
            message = self.messages if completion_index else user_input

        completion = self.completions[completion_index]
        kwargs.update({completion['prompt']:message,'model':completion['model']})

        choice = completion['completion'].create(*args,**kwargs).choices[0]
        self.history.append(choice)
        self.history[-1].update({'completion_index':completion_index})
        self.messages.append({"role": "assistant", "content": attrgetter(completion['text'])(choice)})
    
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

    def __call__(self):
        """ Display full chat log. """
        for i,msg in enumerate(self.messages):
            message = msg['content']
            who = {'user':'User: ','assistant':'GPT: '}[msg['role']]
            print(who + message.strip() + '\n')