# GPT for Financial Advice
## The combination of Large Language Models and Rule-Based Systems

 

![Cover.jpg](https://github.com/HSLU-IFZ-Competence-Center-Investments/GPT_for_Financial_Advice/blob/main/Images/Cover.jpg)

 

The demo can be accessed by running chat.py


# Known issues
- Phrases like "no income" or "zero income" are not interpreted correctly. The model does not understand that the user has no income.


# Not Part of the prototype
- How much chatter should it be able to deal with / confusion with mortgage/leasing (limited use case)
- Moderate risk preference (depends on rule set)
- Catch "As a language model AI..." / "consult a financial advisor" 
- Overlapping age/income range should be questioned by Advisor.
- Reasoning for investment advice
- Possibility to chat longer after recommendation would be great.
- Portfolio should be possible to be updated with new costumer information
- Make the implementation flexible in terms of varying investment profile attributes.
- Implementation of looking for the word yes or no is not robust enough. Firstly, if a word has yes or no in it we get True. On the other hand, we are already limiting it with max token=1. Secondly, np.any returns True even when we have one reply with yes (no) and majority of the replies are not yes (no). Use percentage for Yes / No, take highest.
- Create function, which handles both cases GPT/GPT and GPT/Human. Implement a hybrid conversation scenario, where both the user and gpt could be the customer, i.e. allow gpt to take over and the user to skip answering

### Layout new
- Describe initial situation
- Rule based tabel / brief example
- Link to website / GIF with video
- Main branch clean up / app.py / chat.py

 

### TODOs
- Web hosting 
- API key on website; disclaimer
- Pop up when conversation ended / possiblity to close pop up / scrole through conversation
- Chat icons (gender neutral)