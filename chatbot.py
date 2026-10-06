import os
import ollama


def load_all_knowledge():

    data_folder = "data"
    knowledge = []

    if not os.path.exists(data_folder):
        return ""

    for filename in os.listdir(data_folder):

        if filename.endswith(".txt"):

            filepath = os.path.join(
                data_folder,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                knowledge.append(
                    file.read()
                )

    return "\n\n".join(knowledge)


def get_answer(question):

    knowledge = load_all_knowledge()

    prompt = f"""
You are Nova AI, an AI customer support assistant.

You can answer questions from these customer-support
topics ONLY:

FOOD:
Delivery, cancellation, missing food, damaged food,
refunds, payments and complaints.

SHOPPING:
Products, price, availability, delivery, returns,
exchanges, damaged products, wrong products and refunds.

PAYMENT:
UPI, cards, failed payments, money deducted,
duplicate payments, payment status and refunds.

TRAVEL:
Bookings, cancellation, booking changes, refunds,
payments and travel schedules.

GENERAL CUSTOMER SUPPORT:
Orders, tracking, delivery, cancellation, returns,
refunds, accounts, passwords, products and general
customer issues.

IMPORTANT:

Understand the meaning of the customer's question.

The customer does NOT need to use the exact words
present in the knowledge base.

For example:

"My pizza hasn't arrived"
means FOOD DELIVERY.

"I got the wrong shirt"
means SHOPPING / WRONG PRODUCT.

"Google Pay deducted my money"
means PAYMENT.

"I don't want to go on my trip"
means TRAVEL / CANCELLATION.

"I forgot my login password"
means GENERAL / ACCOUNT.

Answer using the relevant information from the
knowledge base.

Do NOT say "I don't have information" simply because
the exact sentence is not present.

Do NOT invent policies or facts that are not supported
by the knowledge.

If the question is completely unrelated to customer
support, say:

"I'm Nova AI, a customer support assistant. I can help
with food, shopping, payments, travel and general
customer-support questions."

Never ask for passwords, OTPs, PINs, CVV or complete
card numbers.

CUSTOMER SUPPORT KNOWLEDGE:

{knowledge}

CUSTOMER QUESTION:

{question}

Give a simple, clear and helpful answer.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]