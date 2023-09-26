import torch
import datasets
from seamless_communication.models.inference import Translator
import tqdm
import json
import os
import time

import sys

class SeamlessTranslate():

    def __init__(self, 
                 model_name="seamlessM4T_large", 
                 device='cuda',
                 vocoder="vocoder_36langs"):
        self.model_name = model_name
        self.device = device
        self.vocoder = vocoder
        self.translator = Translator(model_name, vocoder, torch.device(device), torch.bfloat16)
        self.ds = None

    
    def load_my_dataset(self, dataset_path):
        '''Load dataset'''
        self.ds = datasets.load_dataset('json',
                            data_files=dataset_path,
                            split='train',
                            streaming=False)
        return self.ds
    
    def translate_seamlessm4t(self, txt, translator, src_language='por', tgt_language='eng'):
        '''Translate text using seamlessM4T model'''
        try:
            txt_translate = str(translator.predict(
                txt,
                't2tt',
                tgt_language,
                src_language,
                False,
            )[0])
            return txt_translate
        except KeyboardInterrupt:
            print("System interrupted by user.")
            raise
        except:
            return txt

    def union_responses(self):
        '''Union all json files in one'''
        response_folder = 'response'
        self.ds = datasets.load_dataset('json', 
                                data_files=os.path.join(response_folder,'*.json'), 
                                split='train', 
                                streaming=False)
        self.ds.to_json(os.path.join(response_folder,'traducao_teste.json'), orient='records')

def worker(translate, idx_start, idx_finish):
    # Itarate over the dataset
    response_folder = 'response'
    log_folder = 'log'
    count_error = 0

    for idx, row in enumerate(translate.ds):
        if idx < idx_start:
            continue  # Skip rows until idx_start is reached
        if idx >= idx_finish:
            break  # Exit the loop if idx_finish is reached

        print(f"Processing {idx} to {idx_finish} ...")
        row['text_eng'] = ''
        for s in row['text'].split('\n'):
            try: 
                row['text_eng'] += translate.translate_seamlessm4t(txt=s, translator=translate.translator) + '\n'

            except Exception as e:
                row['text_eng'] = row['text']
                # errors log
                with open(os.path.join(log_folder,'error.log'), 'a') as f:
                    f.write(f"{idx:>011} - {e}\n{s}\n\n")
                count_error += 1
                break
        
        # create a new json file
        with open(os.path.join(response_folder,f'{idx:>011}.json'), 'w') as f:
            json.dump(row, f)



    # Count errors
    with open(os.path.join(log_folder,'error_count.log'), 'w') as f:
        f.write(f"Total of errors: {count_error}\n")





def main():

    if len(sys.argv) != 3:
        print("Uso: python seu_script.py idx_start idx_finish")
        return
    
    idx_start = int(sys.argv[1])
    idx_finish = int(sys.argv[2])

    # Create a instance of SeamlessTranslate and load the model
    translate = SeamlessTranslate()
    print(translate.model_name)

    # Load dataset
    data_folder = 'data'
    dataset_path = os.path.join(data_folder, 'treinamento_v01_full.json')

    translate.ds = translate.load_my_dataset(dataset_path)
    print("Dataset loaded.")

    # Run worker
    worker(translate, idx_start, idx_finish)

    # Union responses
    # print('Union responses...')
    # translate.union_responses()
    # print('Done!')

if __name__ == '__main__':
    main()