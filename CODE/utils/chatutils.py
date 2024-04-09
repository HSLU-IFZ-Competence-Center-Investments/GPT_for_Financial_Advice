# Author: Ahmet Ege Yilmaz
# Year: 2024

import openai,pickle,time,os,json,datetime
import numpy as np
import pandas as pd
from typing import Optional
from tqdm import tqdm

def ErrorHandler(f, *args, **kwargs):
    def wrapper(*args, **kwargs):
        while True:
            try:
                f(*args, **kwargs)
                break
            # AuthenticationError
            except openai.AuthenticationError as e:
                print(e)
                raise
            except Exception as e:
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
    
    def __init__(self,gpt_name='GPT',username = "User") -> None:
        
        # History of all messages in the chat.
        self.messages = []

        # History of completions by the model.
        self.history = []

        # The name of the model.
        self.gpt_name=gpt_name

        # The name of the user.
        self.username=username

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

    def _unpack_message(self,msg):
        message = msg['content']
        who = {'user':f'{self.username}: ','assistant':f'{self.gpt_name}: '}[msg['role']]
        return who + message.strip() + '\n'
    
    def __call__(self,k:Optional[int]=None):
        """ Display full chat log or last k messages. """

        k = len(self.messages) if k is None else k
        for msg in self.messages[-k:]:
            print(self._unpack_message(msg))



class AssistantSession(ChatSession):
    
    assistant = None

    def __init__(self,gpt_name='Assistant',model="",instructions:str="",tools:list[dict[str,str]]=[],file_paths:list[str]=[""],api_key:str="") -> None:
        
        assert model, "Please provide a model."
        
        super().__init__(gpt_name=gpt_name)

        assert len(file_paths)>0, "Please provide at least one file path."
        for file_path in file_paths:
            assert os.path.exists(file_path), f"File path {file_path} does not exist."

        self.client = openai.OpenAI(api_key=api_key)

        self.files = []
        failed_to_open = 0
        opening_errors = []
        print("Uploading files...")
        for file_path in tqdm(file_paths,total=len(file_paths)):
            try :
                file = self.client.files.create(file=open(file_path, 'rb'),
                                            purpose="assistants")
            except Exception as e:
                failed_to_open+=1
                opening_errors.append(e)
            else:
                self.files.append(file)

        print(f"Failed to open {failed_to_open} files out of {len(file_paths)}")
        if failed_to_open > 0:
            print(f"\n\n Errors when opening: {opening_errors}")

        self.model = model
        self.instructions = instructions
        self.tools = tools

        print("Creating assistant...")
        self.__make_assistant()

        assert self.assistant is not None, "Failed to create assistant."

        self.thread = self.client.beta.threads.create()

    def chat(self,user_input:Optional[dict|str]=None,verbose=True,*args,**kwargs):
        """ Say something to the model and get a reply. """
        

        user_input = self.__get_input(user_input=user_input)
        
        self.__get_reply(user_input=user_input,*args,**kwargs)

        if verbose:
            self.__call__(1)
    
    def save(self, company_foldername):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y%m%d_%H%M%S")
        file_name = f"chat_{formatted_time}.txt"
        folder_path = f"output/{company_foldername}"
        os.makedirs(folder_path, exist_ok=True)

        with open(os.path.join(folder_path, file_name), 'w', encoding='utf-8') as file:
            for exchange in self.history:
                for role, message in exchange.items():
                    file.write(f"{role}: {message}\n")
                file.write("\n")

    def __get_input(self,user_input):
        if user_input is None:
            user_input = input("> ")
        return user_input
    
    @ErrorHandler    
    def __get_reply(self,user_input,*args,**kwargs):
        """ Calls the model. """
        
        _length_before = len(self.messages)

        user_message = self.__create_message(role='user',content=user_input)
        _ = self.__create_run(user_message)
        
        while len(self.messages)<_length_before+2: time.sleep(4)
    
    @ErrorHandler
    def __make_assistant(self):
        """ Creates an assistant. """
        self.assistant = self.client.beta.assistants.create(
            name=self.gpt_name,
            instructions=self.instructions,
            tools=self.tools,
            model=self.model,
            file_ids=[file.id for file in self.files]
        )
    
    def __create_message(self,role,content):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content
        )
        return message
    
    def __create_run(self,message):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        
        return self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
    
    @property
    def messages(self):
        messages = self.client.beta.threads.messages.list(thread_id = self.thread.id)
        return [*reversed(messages.data)]
    
    @messages.setter
    def messages(self,_):return

    @property
    def history(self):
        hstry = []
        messages = self.client.beta.threads.messages.list(thread_id = self.thread.id)
        for msg in reversed(messages.data):
            hstry.append({msg.role:msg.content[0].text.value})
        return hstry
    
    @history.setter
    def history(self,_):return

    def _unpack_message(self,msg):
        message = msg.content[0].text.value
        who = {'user':f'{self.username}: ','assistant':f'{self.gpt_name}: '}[msg.role]
        return who + message + '\n'