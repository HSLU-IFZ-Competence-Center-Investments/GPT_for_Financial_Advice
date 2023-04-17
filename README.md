# GPT for Financial Advice
## The combination of Large Language Models and Rule-Based Systems

### TODOs
- Implement rule based system.
    - check_info function should return the investor profile. To accomplish this:
        1. Use GPT to extract the information, while limiting it to use one word only with the token argument ``n``.

- Make sure GPT does not recommend any portfolios before having all the variables.
    -  To accomplish this: 
        1. Have another GPT check the Advisor-GPT's answers for this type of behaviour. Then, the answer should be edited such that it is less specific, which can also be done by GPT's editing function.

- Try out different openings with Customer-GPT. Temperature for customer.

- Implement a hybrid conversation scenario, where both the user and gpt could be the customer.