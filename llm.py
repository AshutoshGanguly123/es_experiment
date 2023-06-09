import os
from datetime import datetime
from elasticsearch import Elasticsearch
from uuid import uuid4
import json

os.environ["OPENAI_API_KEY"] = "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"
from langchain.llms import OpenAI
llm = OpenAI(temperature=0.95)

promptPretext = '''Classify the intent from the sentence and utter a relevant response.
Extract any entities such as name, amount, date, duration, other that the user sentence contains. The context is that of a debt collection agency which has to strictly comply with US FDCPA. 
Avoid deferring this chat to a debt collection representative and offer solutions to the debtor that are helpful and compliant. 
The example intent categories can include: Wants to pay, needs more time, file a dispute, change payment plan, submit insurance, defiance etc. 
Give your output in this json format, use null where the entity is not present. 
{
    "intents": "needs more time",
    "entities": {
        "name": ,
        "amount": ,
        "phone_number": ,
        "duration": ,
        "other":
    },
    "response": ""
}

Sentence:'''

data = """Someone opened a credit card in my name without my consent.
I'm sorry to hear that. Please contact our customer support immediately, and they will assist you in investigating this issue and resolving it.

I never authorized this account to be opened.
We apologize for the inconvenience. Please reach out to our customer support, and they will help you resolve the issue and ensure your information is protected.

I did not make this purchase, it must be fraudulent.
We understand your concern. Please contact our fraud department as soon as possible to report the unauthorized transaction and secure your account.

This account was opened without my knowledge.
I apologize for the confusion. It's crucial to report this immediately to our customer support, who will help you investigate and resolve the issue.

I believe my identity was stolen.
We're sorry to hear that. Please get in touch with our customer support, and they will guide you through the steps to protect your information and resolve any unauthorized activities.

I have no knowledge of this debt.
We apologize for any confusion. It's important to contact our customer support for further investigation and assistance with this matter.

I suspect someone used my information to open this account.
We're sorry for the inconvenience. Please report this issue to our customer support as soon as possible so they can help you investigate and resolve it.

I did not receive any information about this account until now.
We apologize for the confusion. Please contact our customer support for assistance in investigating this issue and ensuring your information is secure.

This is not my debt, it must be a mistake.
We understand your concern. Please reach out to our customer support, and they will help you investigate the issue and rectify any errors.

I have never heard of this creditor before.
We apologize for any confusion. It's important to contact our customer support for further investigation and assistance regarding this matter.

Why is my balance so high?
There could be several reasons for a high balance, such as interest, fees, or recent transactions. I recommend reviewing your account statement to identify any discrepancies and contacting our customer support for further assistance.

I don't understand why I owe so much.
We understand your concern. Please check your account statement for a detailed breakdown of charges, and if you still have questions, our customer support team will be happy to help.

This balance seems unreasonable to me.
I apologize for any confusion. Please review your account statement to verify the charges, and if you find any discrepancies, contact our customer support for assistance.

How did my balance get this high?
A high balance can result from various factors, including interest rates, fees, and recent transactions. To understand the specific reasons for your balance, please review your account statement and contact our customer support if necessary.

I cannot afford to pay this balance.
We understand financial situations can be challenging. Please reach out to our customer support to discuss potential payment arrangements or options to help manage your balance.

This balance is more than I expected.
We apologize for any confusion. It's important to review your account statement to verify the charges and contact our customer support if you need further assistance or clarification.

How can I dispute this balance?
If you believe there is an error with your balance, please contact our customer support team. They will guide you through the process of disputing the balance and resolving any issues.
"""

# Split data into lines
lines = data.split('\n')

# Extract every alternate line starting from the first line (user text)
user_text = lines[::2]
for user_text in user_text:
    #userText = "I am Jordan and I suffered a job loss recently due to the banking crisis in the US. Can I start repaying my debt after ten months from ym credit card 400059940 associated with ohone number 9766271045?"
    text=promptPretext+user_text
    chat_bot_data = llm(text)
    # Correcting JSON format
    chat_bot_data = chat_bot_data.replace('\n', '').replace(': ', ':')
    # Load the JSON to a Python dictionary
    data = json.loads(chat_bot_data)

    # Extract relevant variables
    intents = data.get('intents')
    entities = data.get('entities')
    response = data.get('response')

    # Accessing entities
    name = entities.get('name')
    amount = entities.get('amount')
    phone_number = entities.get('phone_number')
    duration = entities.get('duration')
    other = entities.get('other')

    #elastic search
    es = Elasticsearch(
        ['https://localhost:9200'],
        http_auth=('elastic', 'CDYAZQqL5f=jN_u-Re+1'),
        verify_certs=False
    )

    # Define the Elasticsearch document
    doc = {
        'user_text': user_text,
        'intent': intents,
        'entities': entities,
        'bot_response': response,
        'name': name,
        'amount': amount,
        'phone_number': phone_number,
        'duration': duration,
        'timestamp': datetime.now(),
    }

    # Index the document (data)
    res = es.index(index="chat-index", id=str(uuid4()), body=doc)
    print(res)


