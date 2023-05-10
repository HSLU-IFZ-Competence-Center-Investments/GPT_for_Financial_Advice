# GPT for Financial Advice
## The combination of Large Language Models and Rule-Based Systems

 

![Cover.jpg](https://github.com/HSLU-IFZ-Competence-Center-Investments/GPT_for_Financial_Advice/blob/main/Images/Cover.jpg)


### Initial situation

The objective of study GPT for Financial Advice is to explore how LLMs and rule-based systems can be combined for investment advice.
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


### Testing the Prototype 

The demo can be accessed locally by forking the repository, installing the packages indicated in requirements.txt and running chat.py.


### Known issues of the prototype
- Phrases like "no income" or "zero income" are not interpreted correctly. The model does not understand that the user has no income.





### Additional: 
- Link to website / GIF with video
- Main branch clean up / app.py / chat.py

 
