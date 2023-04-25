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

- Sentiment analysis:
    - Check if correctly implemented. 
    - Speed it up.
    - It should only be performed for variables not general answers

- <s>Enable input of different user api keys for different users.</s> Handle the case if the given api key is not valid.

- Create function, which handles both cases GPT/GPT and GPT/Human

- Work on the implementation of the regular expression for the user input.

- Make the implementation flexible in terms of varying investment profile attributes.

- Encountered the following error: RateLimitError: That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists. (Please include the request ID 678a66aeab515c0bb4d2bf392bee1385 in your message.)

- Adjust RuleBased Portfolio Age bands to make them exclusive 
