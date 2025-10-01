from openai import OpenAI
import os
from dotenv import load_dotenv 
import json
import prompts
import love_language_starters

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

love_languages = {
    1: "Words of Affirmation",
    2: "Quality Time", 
    3: "Receiving Gifts",
    4: "Acts of Service",
    5: "Physical Touch"
}

class RecatGPT:
    client = OpenAI(api_key=OPENAI_API_KEY)

    @staticmethod
    def ask_gpt(prompt: str, model: str = "gpt-4o-mini") -> str:
        """Send a prompt to GPT and return the response."""
        response = RecatGPT.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    @staticmethod
    def get_love_language_prompt(love_language_type: int) -> str:
        if love_language_type not in love_languages:
            raise ValueError("Invalid love language type")
        
        existing_prompts = RecatGPT.get_existing_love_language_prompt(love_language_type)
        prompt = (
            prompts.LOVE_LANGUAGE_PROMPT + 
            love_languages[love_language_type] + 
            prompts.EXISTING_PROMPT +
            "\n".join(existing_prompts)
        )

        print(prompt)
        return prompt
    
    @staticmethod
    def get_existing_love_language_prompt(love_language_type):
        if love_language_type == 1:
            return love_language_starters.WORDS_OF_AFFIRMATION
        elif love_language_type == 2:
            return love_language_starters.QUALITY_TIME
        elif love_language_type == 3:
            return love_language_starters.RECEIVING_GIFTS
        elif love_language_type == 4:
            return love_language_starters.ACTS_OF_SERVICE
        elif love_language_type == 5:
            return love_language_starters.PHYSICAL_TOUCH
        else:
            return []
        
    @staticmethod
    def rewrite_prompt(prompt):
        print(prompts.REWRITE_PROMPT + prompt)
        new_prompt = RecatGPT.ask_gpt(prompts.REWRITE_PROMPT + prompt)
        return new_prompt
