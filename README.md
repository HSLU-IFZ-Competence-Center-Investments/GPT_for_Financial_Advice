# GPT for Financial Advice
## The combination of Large Language Models and Rule-Based Systems

### TODOs
- Make sure GPT does not recommend any portfolios before having all the variables.
    -  To accomplish this: 
        1. Have another GPT check the Advisor-GPT's answers for this type of behaviour. Then, the answer should be edited such that it is less specific, which can also be done by GPT's editing function.

- Try out different openings with Customer-GPT. Temperature for customer.

- Implement a hybrid conversation scenario, where both the user and gpt could be the customer, i.e. allow gpt to take over giving the user to skip answering.

- Make sure Advisor does not complete Costumer's answer if it is empty

- Overlapping age/income range should be questioned by Advisor

- Speed up sentiment analysis

- Sentiment analysis should only be performed for variables not general answers

- <s>Enable input of different user api keys for different users.</s> Handle the case if the given api key is not valid.

- Create function, which handles both cases GPT/GPT and GPT/Human