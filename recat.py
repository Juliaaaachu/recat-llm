from openai import OpenAI
import os
from dotenv import load_dotenv 

load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PROMPT = """
You are to generate a prompt for couples to answer. 
These are the 5 love languages: Words of Affirmation, Quality Time, Receiving Gifts, Acts of Service, and Physical Touch.
Please generate a prompt for:

"""

GO_DEEPER_PROMPT = """
The user wishes to go deeper with the response.
Come up with a question that helps the user to write a deeper response.
Here is the user's response: 

"""

# Initialize the client
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt(prompt: str) -> str:
    """
    Send a prompt to GPT and return the response.
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # You can also use gpt-4.1, gpt-4o, etc.
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def get_prompt_for_gpt(love_language_type):

    if love_language_type == 1:
        love_language = "Words of Affirmation"
    elif love_language_type == 2:
        love_language = "Quality Time"
    elif love_language_type == 3:
        love_language = "Receiving Gifts"
    elif love_language_type == 4:
        love_language = "Acts of Service"
    elif love_language_type == 5:
        love_language = "Physical Touch"
    else:
        print("Choose a valid option.")
        return
    
    return PROMPT + love_language

def go_deeper(response):
    new_prompt = GO_DEEPER_PROMPT + response
    answer = ask_gpt(new_prompt)
    print("\n", answer)

if __name__ == "__main__":

    while (True):
        user_options = """
    Pick an Option

    1) Words of Affirmation
    2) Quality Time
    3) Physical Touch
    4) Acts of Service
    5) Receiving Gifts

    Option: """

        user_input = input(user_options)

        if user_input.isdigit():   # checks if input is only digits
            user_input = int(user_input)
        else:
            print("Please enter a valid number.")
            continue

        gpt_prompt = get_prompt_for_gpt(user_input)
        answer = ask_gpt(gpt_prompt)
        print("\n", answer)

        user_response = input("Type your response: ")
        user_responses = [user_response]
        
        while (True):
            user_go_deeper = input("Go Deeper? Y/N ")
            if user_go_deeper == "Y":
                go_deeper("\n".join(user_responses))
                user_response = input("Type your response: ")
                user_responses.append(user_response)
            else:
                break
        
        do_continue = input("Continue? Y/N")
        if do_continue == "Y":
            continue
        else:
            quit()
