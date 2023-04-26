import openai,re
from utils import ChatSession,update_investor_profile
import pandas as pd

# load and set our key
try:
    openai.api_key = open("key.txt", "r").read().strip("\n")
except FileNotFoundError:
    openai.api_key = input("Please enter your OpenAI API key: ")
    with open("key.txt", "w") as f:
        f.write(openai.api_key)

RuleBasedPortfolios = pd.read_excel('RuleBasedPortfolios.xlsx')
RuleBasedPortfolios.columns = RuleBasedPortfolios.columns.map(lambda x: x.lower())
assert 'portfolio' in RuleBasedPortfolios.columns

RuleBasedPortfolios.age = RuleBasedPortfolios.age.apply(lambda x: 'yes' if x == '50 -' else 'no') # use .strip()
RuleBasedPortfolios.income = RuleBasedPortfolios.income.apply(lambda x: 'yes' if x == '0 - 100' else 'no') # use .strip()
RuleBasedPortfolios['risk appetite'] = RuleBasedPortfolios['risk appetite'].apply(lambda x: 'yes' if x == 'High' else 'no') # use .strip()

session1 = ChatSession(gpt_name='Advisor')

# user_input = input("> ")
user_input = ''
session1.inject(line="You are a financial advisor at a bank. You must ask specifically what the customers' age, annual income and risk appetite is. Be subtle about asking for these information and\
                            do not ask at the very beginning of the conversation. Always prioritize answering the customers' questions\
                            over asking for these information. Do not recommend a specific portfolio before you gathered these information.\
                            I am a customer seeking financial advise from you. Say ok if you understand.",role="user")
session1.inject(line="Ok.",role= "assistant")
investor_profile = {i:None for i in ['age','income','risk appetite']}
pattern = re.compile(r'[\w?]+')
while True:
    session1.chat(user_input=user_input,verbose=False)
    print('Advisor: ', session1.messages[-1].content)
    user_input = input("> ")
    print('Customer: ', user_input)
    if re.search(pattern,user_input.strip()) is not None:
        update_investor_profile(investor_profile=investor_profile,dialogue=f'{session1.gpt_name}: {session1.messages[-1].content}'+'\n'+f'Customer: {user_input}')
    if not len([i for i in investor_profile.values() if not i]):
        break
print(investor_profile)
# Rule based portfolio by using ``investor_profile``
portfolio = RuleBasedPortfolios.where(lambda x: x['age'].apply(lambda y: y in investor_profile['age'].lower())*\
                            x['income'].apply(lambda y: y in investor_profile['income'].lower())*\
                                x['risk appetite'].apply(lambda y: y in investor_profile['risk appetite'].lower()))['portfolio'].dropna().values
assert portfolio.size == 1
portfolio = int(portfolio.item())

# Tell GPT to recommend portfolio
session1.inject(line=f"Then, I would recommend portfolio {portfolio}.",role= "assistant")
session1(1)