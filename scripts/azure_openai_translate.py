import os
import openai
from dotenv import load_dotenv, find_dotenv

from langchain.llms import AzureOpenAI


def azure_openai_translate():
    # Use Azure environment
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['AZURE_OPENAI_KEY']
    openai.api_base = os.environ['AZURE_OPENAI_ENDPOINT']
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'

    text = '''Bom dia amiguinhos já estou aqui.
    Tenho tanta coisa para te divertir.
    Quero ouvir você contar até três.
    '''
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        engine='Teste',
        messages=[{"role": "user", "content": f"Translate to English: {text}"}]
        )

    print(response.choices[0].message.content)

if __name__ == '__main__':
    azure_openai_translate()