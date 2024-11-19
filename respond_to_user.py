from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import json
import os

def understand_category(user_input):
    # Define your prompt template
    prompt_template = PromptTemplate.from_template(
        """
        You are a bank assistant chatbot. You are given the following user's query.
        {query}
        Your only task is to understand the category of user request.

        You know of 7 categories, and no matter what the user's query you will respond 
        with one of these seven. Do not add anythign else. Just one of these 7 categories.

        Category 1. **Balance Inquiries**
        Category 2. **Transactions**
        Category 3: **Payments**
        Category 4: **Deposit and Withdrawal Queries**
        Category 5: **Spending Limits and Budgeting
        Category 6: General Account Information
        Category 7: Assistance and Help

        Here are several example queries under each category:
        - "What's my current balance?"
        - "How much money do I have in my account?"
        - "Do I have enough funds for a transfer?"
        Your response: 1. **Balance Inquiries**

        - "What are the last three transactions?"
        - "Show me my recent transactions."
        Your response: 2. **Transactions**

        - "Send 500 rupees to XYZ."
        - "Transfer 1000 rupees to my friend."
        - "Pay my phone bill."
        - "Can I send money today?"
        - "When will my money reach XYZ?"
        - "Has my payment been sent?"
        - "Did I receive any deposits?"
        - "When can I expect my salary?"
        Your response: 3. **Payments**

        - "Did I get any new deposits?"
        - "Has the cheque I deposited cleared?"
        - "Is there a way to withdraw money today?"
        Your response: 4. **Deposit and Withdrawal Queries**

        - "Do I have more than 200 rupees?"
        - "Can I spend 500 rupees today?"
        - "Is my monthly limit exceeded?"
       Your response:  5. **Spending Limits and Budgeting**

        
        - "Can I see my account details?"
        - "When is my next bill due?"
        Your response: 6. **General Account Information**


        - "Can you help me with my account?"
        - "I need assistance with a payment."
        Your response: 7. **Assistance and Help**
        """
    )

    # Use RunnableSequence to chain the prompt and LLM together
    chain = prompt_template | llm
    # Generate the response
    response = chain.invoke({"query": user_input})
    return response


load_dotenv()


llm = ChatGroq(
# model="mixtral-8x7b-32768",
model = "llama-3.1-70b-versatile",
temperature=0,
max_tokens=None,
timeout=None,
max_retries=2)

# 1. Define Prompt Templates
# Each template corresponds to a common banking query or intent.

balance_template = PromptTemplate(
    input_variables=["user_input"],
    template="""The user wants to check their balance. Respond appropriately
    in 10 words or less. Do not make up a balance. Reassure them.
    {user_input}
    """
)

payments_template = PromptTemplate(
    input_variables=["user_input"],
    template="The user wants to transfer money. Respond in a secure, friendly manner: {user_input}"
)

transaction_history_template = PromptTemplate(
    input_variables=["user_input"],
    template="The user wants to know recent transactions. Respond accordingly: {user_input}"
)

unclear_template = PromptTemplate(
    input_variables=["user_input"],
    template="The user query isn't recognized. Ask them to clarify: {user_input}"
)

account_template = PromptTemplate(
    input_variables=["user_input"],
    template="The user is asking about their account. respond reassuringly: {user_input}"
)

# add tons more templates...
def process_template_response(template, llm, user_input):
    """
    Process a template response with the given LLM and user input.
    Returns the response and prints follow-up message.
    """
    chain = template | llm
    response = chain.invoke({"user_input": user_input})
    print(response.content)
    print('Can I help with something else?')
    return response

def main():
    # Define template mappings
    template_map = {
        "balance": balance_template,
        "payments": payments_template,
        "transactions": transaction_history_template,
        "general account": account_template,
        "help": unclear_template
    }
    
    print("Welcome to the Bank Chatbot! How can I assist you today?")
    
    while True:
        user_input = input("You: ")
        
        # Check for exit condition
        if user_input.lower() in ["quit", "exit", 'x', 'q']:
            print("Thank you for using the Bank Chatbot. Goodbye!")
            break
        
        # First, understand the category
        response = understand_category(user_input)
        print(f"Invoking: {response.content} Tree")
        
        # Find matching template and process it
        response_lower = response.content.lower()
        for keyword, template in template_map.items():
            if keyword in response_lower:
                process_template_response(template, llm, user_input)
                break
        
        # Continue to next iteration
        continue

if __name__ == "__main__":
    main()


