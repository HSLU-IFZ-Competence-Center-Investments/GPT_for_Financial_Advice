# Author: Ahmet Ege Yilmaz
# Year: 2023

import openai,pickle,time
import numpy as np
import pandas as pd
from typing import Optional

def ErrorHandler(f, *args, **kwargs):
    def wrapper(*args, **kwargs):
        while True:
            try:
                f(*args, **kwargs)
                break
            # RateLimitError
            except openai.error.RateLimitError:
                print('Rate limit exceeded. I will be back shortly, please wait for a minute.')
                time.sleep(60)
            # AuthenticationError
            except openai.error.AuthenticationError as e:
                print(e)
                raise
    return wrapper

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

    @ErrorHandler    
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

@ErrorHandler
def update_investor_profile(session,investor_profile:dict,questions:list[str],verbose:bool=False):

    ask_for_these = [i for i in investor_profile if not investor_profile[i]]
    n_limit = 20
    temp_reply = openai.ChatCompletion.create(messages=session.messages.copy(),model='gpt-3.5-turbo').choices[0].message.content
    for info_type in ask_for_these:
        choices = [*map(lambda x:x.message.content,openai.ChatCompletion.create(messages=
                                            session.messages+\
                                            # [{"role": "assistant", "content":'Understood.'}]+\
                                            [{"role": "assistant", "content":temp_reply}]+\
                                            [{"role": "user", "content": f'Do you know my {info_type} based on our conversation so far? Yes or no:'}],\
                                            model='gpt-3.5-turbo',n=n_limit,max_tokens=1).choices)]
        if verbose:
            print('1:')
            print({i:round(choices.count(i)/len(choices),2) for i in pd.unique(choices)})
        if np.any([*map(lambda x: 'yes' in x.lower(),choices)]):
            choices = [*map(lambda x:x.message.content,openai.ChatCompletion.create(messages=\
                                        session.messages+\
                                        # [{"role": "assistant", "content": 'Understood.'}]+\
                                        [{"role": "assistant", "content":temp_reply}]+\
                                        [{"role": "user", "content": questions[info_type]}],\
                                        model='gpt-3.5-turbo',n=n_limit,max_tokens=1).choices)]
            if verbose:
                print('2:')
                print({i:round(choices.count(i)/len(choices),2) for i in pd.unique(choices)})
            if np.any([*map(lambda x: 'yes' in x.lower(),choices)]):
                investor_profile[info_type] = 'yes'
            elif np.any([*map(lambda x: 'no' in x.lower(),choices)]):
                investor_profile[info_type] = 'no'


# @ErrorHandler
# def update_investor_profile(session,investor_profile:dict,questions:list[str],verbose:bool=False):

#     ask_for_these = [i for i in investor_profile if not investor_profile[i]]
    
#     for info_type in ask_for_these:
#         sentiment = None
#         limit = 20
#         while sentiment is None:
#             session.chat(f'Do you know my {info_type}? Say only yes or no.',max_tokens=1,verbose=False)
#             if verbose:
#                 print('1',session.messages[-1].content)
#             if 'yes' in session.messages[-1].content.lower():
#                 sentiment = 'positive'
#             elif 'no' in session.messages[-1].content.lower():
#                 sentiment = 'negative'
#             elif limit <= 0:
#                 raise Exception('Something went wrong. Please try again.')
#             session.clear(2)
#             limit -= 1
#         if sentiment == 'positive': 
#             sentiment = None
#             limit = 20    
#             while sentiment is None:
#                 session.chat(questions[info_type],max_tokens=1,verbose=False)
#                 if verbose:
#                     print('2',session.messages[-1].content)
#                 if 'yes' in session.messages[-1].content.lower():
#                     sentiment = 'positive'
#                 elif 'no' in session.messages[-1].content.lower():
#                     sentiment = 'negative'
#                 elif limit <= 0:
#                     break
#                 session.clear(2)
#                 limit -= 1
#             if sentiment is not None:
#                 investor_profile[info_type] = 'yes' if sentiment == 'positive' else 'no'
