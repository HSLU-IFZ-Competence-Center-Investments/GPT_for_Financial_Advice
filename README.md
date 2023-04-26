# GPT for Financial Advice
## The combination of Large Language Models and Rule-Based Systems

![Cover.jpg](https://github.com/HSLU-IFZ-Competence-Center-Investments/GPT_for_Financial_Advice/blob/main/Images/Cover.jpg)

The demo can be accessed by running chat.py

### TODOs

# PRIO 1
- <s>Enable input of different user api keys for different users.</s> Handle the case if the given api key is not valid. Handle empty key.txt
- Error handling: RateLimitError.
- Make sure Advisor does not complete Costumer's answer if it is empty
- Valid user imput: IF empty, GPT has to ask the same question again. Work on the implementation of the regular expression for the user input. 
- Limit Dialog / Catch *End of conversation*
- RateLimitError handling needs to cover the case where the error happens in update_investor_profile

# PRIO 2
- Overlapping age/income range should be questioned by Advisor
- Create function, which handles both cases GPT/GPT and GPT/Human. Implement a hybrid conversation scenario, where both the user and gpt could be the customer, i.e. allow gpt to take over giving the user to skip answering. 
- Make the implementation flexible in terms of varying investment profile attributes.

# PRIO 3
- Make sure GPT does not recommend any portfolios before having all the variables.
    -  To accomplish this: 
        1. Have another GPT check the Advisor-GPT's answers for this type of behaviour. Then, the answer should be edited such that it is less specific, which can also be done by GPT's editing function.
- Try out different openings with Customer-GPT. Temperature for customer.
- Sentiment analysis:
    - It should only be performed for variables not general answers












