# GPT for Financial Advice
## The combination of Large Language Models and Rule-Based Systems

![Cover.jpg](https://github.com/HSLU-IFZ-Competence-Center-Investments/GPT_for_Financial_Advice/blob/main/Images/Cover.jpg)

The demo can be accessed by running chat.py

### TODOs

# PRIO 1

- Implementation of looking for the word yes or no is not robust enough. Firstly, if a word has yes or no in it we get True. On the other hand, we are already limiting it with max token=1. Secondly, np.any returns True even when we have one reply with yes (no) and majority of the replies are not yes (no). Use percentage for Yes / No, take highest.
- <s>AdvisorGPT seems to be more aware of the collected data than SupervisorGPT. Maybe, just consult to AdvisorGPT about the investor profile rather than SupervisorGPT.</s>Done.
- Catch *End of conversation*
- Smooth Ending sentence
- Reasoning for investment advice


# PRIO 2
- Create function, which handles both cases GPT/GPT and GPT/Human. Implement a hybrid conversation scenario, where both the user and gpt could be the customer, i.e. allow gpt to take over and the user to skip answering. 

# PRIO 3
- Make sure GPT does not recommend any portfolios before having all the variables.
    -  To accomplish this: 
        1. Have another GPT check the Advisor-GPT's answers for this type of behaviour. Then, the answer should be edited such that it is less specific, which can also be done by GPT's editing function.
- Try out different openings with Customer-GPT. Temperature for customer.
- Sentiment analysis:
    - It should only be performed for variables not general answers
- Implement the rest of the conversation after recommending the portfolio. For this, we would need information on the content of the portfolios.
- Possibility to chat longer after recommendation would be great. 
- Portfolio should be possible to be updated with new costumer information
- Make the implementation flexible in terms of varying investment profile attributes.


# Not Part of the prototype
- How much chatter should it be able to deal with / confusion with mortgage/leasing (limited use case)
- Moderate risk preference (depends on rule set)
- Catch "As a language model AI..." / "consult a financial advisor" 
- Overlapping age/income range should be questioned by Advisor.











