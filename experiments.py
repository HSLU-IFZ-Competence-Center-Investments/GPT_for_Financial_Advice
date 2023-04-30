import openai,re
import pandas as pd
from utils import ChatSession, update_investor_profile

def main():    

    # 2) Rule based system.

    ## 2.1) Read in rule based system.
    RuleBasedPortfolios = pd.read_excel('RuleBasedPortfolios.xlsx')
    RuleBasedPortfolios.columns = RuleBasedPortfolios.columns.map(lambda x: x.lower())
    assert 'portfolio' in RuleBasedPortfolios.columns

    RuleBasedPortfolios.age = RuleBasedPortfolios.age.apply(lambda x: 'yes' if x == '50 -' else 'no') # use .strip()
    RuleBasedPortfolios.income = RuleBasedPortfolios.income.apply(lambda x: 'yes' if x == '0 - 100' else 'no') # use .strip()
    RuleBasedPortfolios['risk appetite'] = RuleBasedPortfolios['risk appetite'].apply(lambda x: 'yes' if x == 'High' else 'no') # use .strip()

    ## 2.2) The attributes of the investor profile. They need to be consistent with the columns of RuleBasedPortfolios.
    investor_profile = {i:None for i in ['age','income','risk appetite']}

    ## 2.3) Questions need to be crafted, allowing SupervisorGPT to navigate through the rule based system and reach a portfolio recommendation.
    # questions = [
    #         'Is the Customer 51 years old or older? Answer by saying yes or no.',\
    #         'If the annual income of the Customer is not given as annual income, convert it to annual income. Is it less than 100K annually? Answer by saying yes or no.',\
    #         'Does the Customer have a high risk appetite? Answer by saying yes or no.'
    #     ]
    # questions = [
    #     'Is the Customer 51 years old or older? Start the sentence with a yes or no.',\
    #     'If the annual income of the Customer is not given as annual income, convert it to annual income. Is it less than 100K annually? Start the sentence with a yes or no.',\
    #     'Does the Customer have a high risk appetite? Start the sentence with a yes or no.'
    # ]
    # questions = [
    #         'Am I 51 years old or older? Say only yes or no.',\
    #         'If my annual income is not given as annual income, convert it to annual income. Is it less than 100K annually? Say only yes or no.',\
    #         'Do I have a high risk appetite? Say only yes or no.'
    #     ]
    # questions = [
    #         'Am I 51 years old or older? Say only yes or no.',\
    #         'Is my annual income less than 100K? Say only yes or no. *You should convert it to annual income to answer, if it is not given as annual income.*',\
    #         'Do I have a high risk appetite? Say only yes or no.'
    #     ]
    questions = [
            'Based on our conversation so far, am I 51 years old or older? Yes or no:',\
            'Based on our conversation so far, calculate my annual income. Is it less than 100K? Yes or no:',\
            'Based on our conversation so far, do I have a high risk appetite? Yes or no:'
        ]
    questions = {i:k for i,k in zip(investor_profile,questions)}



    # 3) Financial advisory session.

    ## 3.1) Initialize the AdvisorGPT.
    sessionAdvisor = ChatSession(gpt_name='Advisor')
    ## 3.2) Instruct GPT to become a financial advisor.
    sessionAdvisor.inject(line="You are a financial advisor at a bank. You must ask specifically what the customers' age, annual income and risk appetite is. Be subtle about asking for these information and\
                                do not ask at the very beginning of the conversation. Always prioritize answering the customers' questions\
                                over asking for these information. Do not recommend a specific portfolio before you gathered these information.\
                                I am a customer seeking financial advise from you. Say ok if you understand.",role="user")
    sessionAdvisor.inject(line="Ok.",role= "assistant")



    ## 3.3) Start the conversation.

    ### 3.3.1) user might or might not say anything at the beginning of the conversation.
    user_input = ''
    sessionAdvisor.chat(user_input=user_input,verbose=False)
    print('Advisor: ', sessionAdvisor.messages[-1].content)
    ### 3.3.2) The loop will end when the investor profile is completely obtained.

    ### 3.3.3) The loop will end upon reaching chat limit.
    limit = 100

    ### 3.3.4) Gather info from customer to obtain investor profile.
    while True:
        user_input = input("> ")
        while re.search('[\w?]+',user_input) is None:
            print('Advisor: I am sorry. I did not quite get that.')
            user_input = input("> ")
        sessionAdvisor.inject(line=user_input,role='user')
        # print(session.messages)
        update_investor_profile(session=sessionAdvisor,investor_profile=investor_profile,questions=questions,verbose=True)
        ask_for_these = [i for i in investor_profile if not investor_profile[i]]
        if limit <= 0:
            print('Chat limit exceeded. Session ended.')
            return
        limit -= 1
        if len(ask_for_these):
            print(ask_for_these)
            sessionAdvisor.inject(line=f"*I am still not sure what the customer's {', '.join(ask_for_these)} is. I must ask for these...*",role="assistant")
        else:
            break
        sessionAdvisor.chat(user_input='',verbose=False)
        print('Advisor: ', sessionAdvisor.messages[-1]['content'])
        
    ### 3.3.5) Get rule based portfolio by using ``investor_profile``
    portfolio = RuleBasedPortfolios.where(lambda x: x['age'].apply(lambda y: y in investor_profile['age'].lower())*\
                                x['income'].apply(lambda y: y in investor_profile['income'].lower())*\
                                    x['risk appetite'].apply(lambda y: y in investor_profile['risk appetite'].lower()))['portfolio'].dropna().values
    assert portfolio.size == 1
    portfolio = int(portfolio.item())

    ### 3.3.6) Tell GPT to recommend portfolio
    sessionAdvisor.inject(line=f"Then, I would recommend portfolio {portfolio}.",role= "assistant")
    sessionAdvisor(1)
    print('Session successfully ended.')

if __name__ == "__main__":

    # 1) load or set API key
    while True:
        try:
            openai.api_key = open("key.txt", "r").read().strip("\n")
            # if re.search('(^sk-)(\w{48})$',openai.api_key) is None:
            # if re.search('(^sk-)(.{48})$',openai.api_key) is None:
            # if key.txt is empty or if the file is  not found, ask for key as an input
            if re.search('^sk-',openai.api_key) is None:
                print('Invalid API key.')
                raise FileNotFoundError
            break
        except FileNotFoundError:
            with open("key.txt", "w") as f:
                f.write(input("Please enter your OpenAI API key: "))

    print('Connecting you to the financial advisor...')
    main()