import os
import openai
from dotenv import load_dotenv, find_dotenv

import tqdm
import json

import datasets

import time


def azure_openai_translate():
    # Load dataset
    ds = my_load_dataset()

    # Itarate over the dataset
    for idx, row in enumerate(tqdm.tqdm(ds)):
        try:
            row['text_eng'] = '\n'.join( translate(s) for s in row['text'].split('\n'))
            #row['text_eng'] = translate('Olá Mundo!')
            
            # create a new json file
            with open(f'response/{idx:>011}.json', 'w') as f:
                json.dump(row, f)
        except Exception as e:
            with open('response/error.log', 'a') as f:
                f.write(f"{idx:>011} - {e}\n{row['text']}\n\n")
            row['text_eng'] = row['text']
            continue
        
        # Verify if the limit of 3500 requests per minute was reached
        # if idx % 3500 == 0:
        #     time.sleep(65)
        if idx >= 5:
            break
    
def my_load_dataset():
    '''Load dataset'''
    ds = datasets.load_dataset('json',
                           data_files='/Volumes/DATA/cgu-translate-dataset/data/treinamento_v01_full.json',
                           split='train',
                           streaming=False)
    return ds

def translate(text):
    '''Translate text to English'''

    # Use Azure environment
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['AZURE_OPENAI_KEY']
    openai.api_base = os.environ['AZURE_OPENAI_ENDPOINT']
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'

    # Translate with Azure OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        engine='Teste',
        messages=[{"role": "user", "content": f"Translate to English: {text}"}]
        )

    return response.choices[0].message.content


if __name__ == '__main__':
    print('Starting...')
    azure_openai_translate()
    print('Done!')