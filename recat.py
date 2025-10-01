import json
import prompts
from RecatGPT import RecatGPT


def go_deeper(response):
    new_prompt = prompts.GO_DEEPER_PROMPT + response
    answer = RecatGPT.ask_gpt(new_prompt)
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

        gpt_prompt = RecatGPT.get_love_language_prompt(user_input)
        love_prompt = RecatGPT.ask_gpt(gpt_prompt)
        print("Love Prompt: ", love_prompt)

        new_love_prompt = RecatGPT.rewrite_prompt(love_prompt)

        print("\n Rewrite Love Prompt: ", new_love_prompt)

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
