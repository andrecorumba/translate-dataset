import os
import openai
from dotenv import load_dotenv, find_dotenv

def openai_translate():
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']

    text = '''Na minha terra te palmeiras onde canta o sabiá. 
    As aves que aqui gorjeiam não gorjeiam como lá. 
    Nosso céu tem mais estrelas, nossas várzeas tem mais flores.
    '''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=[{"role": "user", "content": f"Translate to English: {text}"}]
        )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    openai_translate()