import os
import subprocess
import requests
import json
from subprocess import PIPE, STDOUT
import pathlib


class TranslationAPI():
    def __init__(self, model):
        self.model = model
        self.this_path = pathlib.Path(__file__).parent.absolute()
        self.model_dir = os.path.join(self.this_path, 'model')
        
    def start_allen_server(self):
        if self.model == 'transformer':
            model_name = 'bert_transformer'
            model_path = os.path.join(self.model_dir, f'{model_name}.tar.gz')
        
        cmd = f'allennlp serve --archive-path {model_path} --predictor seq2seq --field-name source'
        #self.proc = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT,
        #                        universal_newlines=True, 
        #                        shell=True)
        self.proc = subprocess.Popen(cmd, shell=True)        
    def translate(self, txt):
        url = "http://127.0.0.1:8000/predict"
        req_data = {"source":txt}
        req_headers = {'Content-Type':'application/json'}
        
        rsp = requests.post(url, headers=req_headers, json=req_data)
        translated_tokens =  eval(rsp.content.decode())['predicted_tokens']
        return ' '.join(translated_tokens)

    def shut_down_server(self):
        self.proc.kill()
        
if __name__ == '__main__':
    API = TranslationAPI('transformer')
    API.start_allen_server()
    
    
    
    # print(proc.stdout.read().split('\n')[-2])
    # OSError: [Errno 98] Address already in use: ('127.0.0.1', 8000)
    # if running, no return