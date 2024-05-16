# GPT for Financial Advice
## The Combination of Large Language Models and Rule-Based Systems

 

![Cover.jpg](https://github.com/HSLU-IFZ-Competence-Center-Investments/GPT_for_Financial_Advice/blob/main/Images/Cover.jpg)


### Initial situation

The objective of study "GPT for Financial Advice" is to explore how LLMs and rule-based systems can be combined for investment advice.
In addition, the study aims to create a prototype that showcases the benefits of integrating these two concepts,
without, however, meeting all regulatory requirements (e.g. by the Banking Act or the Federal Data Protection Act) for
AI-based investment advice. Hence, the focus is on demonstrating the technical feasibility of using LLMs to support
deterministic investment recommendations, rather than discussing potential obstacles. The solution obtained shows
that the combination of probabilistic LLMs and rule-based systems is possible, while retaining the advantages of both
approaches, and that the prototype works well in most cases. The findings from this study and the prototype can be
used by the financial sector as a starting point for discussion and development of more sophisticated solutions

### Prototype description

The prototype is based on OpenAI’s pre-trained GPT-3.5-turbo model and uses its corresponding API for prompt engineering.
Furthermore, the proof-of-concept is performed using a simplified rule-based decision system for investment recommendation.

#### Rule based decision system: 

![Table_rules.JPG](https://github.com/HSLU-IFZ-Competence-Center-Investments/GPT_for_Financial_Advice/blob/main/Images/Table_rules.JPG)

The rule based decision system can be seen as a function that deterministically transforms the attributes age, wealth, and risk appetite
of a user, i.e., a bank client, to a specific model portfolio, but can in principle be used for other rule-sets.


### Testing the prototype 

The demo can be accessed locally by [forking the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo), installing the packages indicated in requirements.txt and running the file chat.py. If you have not worked with GitHub before, [set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git) first.

- In an existing environment you can install packages using the following terminal command: pip install -r requirements.txt
- Please consult this guide if you are unsure how to set up a [new environment](https://realpython.com/python-virtual-environments-a-primer/#create-it).

When starting chat.py, you will be asked to enter an [OpenAI API key](https://platform.openai.com/account/api-keys), since the prototype runs with the paid LLM ChatGPT-3.5-turbo. 

### Known issues of the prototype
- Phrases like "no income" or "zero income" are not interpreted correctly. The model does not understand that the user has no income.


### Video of the prototype

https://github.com/HSLU-IFZ-Competence-Center-Investments/GPT_for_Financial_Advice/assets/31382828/26cc011a-ba01-4976-aac8-fe106e344b46

You might enlarge the video to full screen for a better experience.

### Related report

The report was published on the [HSLU Retailbanking Blog](https://hub.hslu.ch/retailbanking/download/gpt-for-financial-advice/) and is available publicly. 
 
