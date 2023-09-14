import torch
import datasets
from seamless_communication.models.inference import Translator
import tqdm
import json
import os
import time

class SeamlessTranslate():

    def __init__(self, 
                 model_name="seamlessM4T_large", 
                 device='cuda',
                 vocoder="vocoder_36langs"):
        self.model_name = model_name
        self.device = device
        self.vocoder = vocoder
        self.translator = Translator(model_name, vocoder, torch.device(device), torch.bfloat16)

    
    def load_my_dataset(self, dataset_path):
        '''Load dataset'''
        ds = datasets.load_dataset('json',
                            data_files=dataset_path,
                            split='train',
                            streaming=False)
        return ds
    
    def translate_seamlessm4t(self, txt, translator, src_language='por', tgt_language='eng'):
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
        ds = datasets.load_dataset('json', 
                                data_files=os.path.join(response_folder,'*.json'), 
                                split='train', 
                                streaming=False)
        ds.to_json(os.path.join(response_folder,'traducao_teste.json'), orient='records')

def main():

    # Create a instance of SeamlessTranslate and load the model
    translate = SeamlessTranslate()
    print(translate.model_name)

    # Load dataset
    data_folder = 'data'
    dataset_path = os.path.join(data_folder, 'treinamento_v01_full.json')

    ds = translate.load_my_dataset(dataset_path)
    print("Dataset loaded.")


    # Itarate over the dataset
    response_folder = 'response'
    log_folder = 'log'
    count_error = 0
    idx_start = 0
    for idx, row in enumerate(tqdm.tqdm(ds)):
        if idx >= idx_start:
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

            # Verify if the limit of 3500 requests per minute was reached
            # if idx % 3500 == 0:
            #     time.sleep(65)
            if idx >= 3:
                break

    # Count errors
    with open(os.path.join(log_folder,'error_count.log'), 'w') as f:
        f.write(f"Total of errors: {count_error}\n")
    
    print('Union responses...')
    translate.union_responses()
    print('Done!')

if __name__ == '__main__':
    main()