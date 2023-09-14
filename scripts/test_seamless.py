from seamless_communication.models.inference import Translator
import torch

 

translator = Translator("seamlessM4T_large", "vocoder_36langs", torch.device("cpu"), torch.float32)

## abaixo uma satring que substitui quebra de linha por "[|]"
## para que o tradutor não quebre a frase em duas

txt = '7º Seminário Internacional sobre Análise de Dados na Administração Pública.\nEsse evento é organizado conjuntamente pelo TCU, pela Controladoria Geral da União e pela Escola Nacional de Administração Pública e tem por objetivo promover o compartilhamento de experiências e boas práticas relacionadas ao uso de técnicas de análise e mineração de dados, como instrumentos para a melhoria da gestão e do controle de entidades e políticas públicas.'

txt = txt.replace('\n', '[|]')

txt = str(translator.predict(
    txt,
    't2tt',
    'eng',
    'por',
    False,

)[0])

print(txt.replace('[|]', '\n'))