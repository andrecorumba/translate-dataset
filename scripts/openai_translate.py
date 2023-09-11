import os
import openai
from dotenv import load_dotenv, find_dotenv

def openai_translate():
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']

    text = '''Bom dia amiguinhos já estou aqui.
    Tenho tanta coisa para te divertir.
    Quero ouvir você contar até três.
    '''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=[{"role": "user", "content": f"Translate to English: {text}"}]
        )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    openai_translate()