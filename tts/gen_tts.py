import numpy as np
import torch
import os 
import argparse
import re
from models.tacotron2 import Tacotron2
from models.tacotron import Tacotron
from models.wavernn import WaveRNN

from utils.text.symbols import symbols
from utils.paths import Paths

from utils.text import text_to_sequence
from utils.display import save_attention, simple_table
from utils.dsp import reconstruct_waveform, save_wav


from utils import hparams as hp
#import hparams as hp

class TaiwaneseTacotron():
    def __init__(self):
        # Parse Arguments
        parser = argparse.ArgumentParser(description='TTS')
        self.args = parser.parse_args()
        self.args.vocoder = 'wavernn'
        self.args.hp_file = 'hparams.py'
        self.args.voc_weights = False
        self.args.tts_weights = False
        self.args.save_attn = False
        self.args.batched = True
        self.args.target = None
        self.args.overlap = None
        self.args.force_cpu = False
        #================ vocoder ================#
        if self.args.vocoder in ['griffinlim', 'gl']:
            self.args.vocoder = 'griffinlim'
        elif self.args.vocoder in ['wavernn', 'wr']:
            self.args.vocoder = 'wavernn'
        else:
            raise argparse.ArgumentError('Must provide a valid vocoder type!')
            
        hp.configure(self.args.hp_file)  # Load hparams from file
        
        # set defaults for any arguments that depend on hparams
        if self.args.vocoder == 'wavernn':
            if self.args.target is None:
                self.args.target = hp.voc_target
            if self.args.overlap is None:
                self.args.overlap = hp.voc_overlap
            if self.args.batched is None:
                self.args.batched = hp.voc_gen_batched
        
        #================ others ================#
        paths = Paths(hp.data_path, hp.voc_model_id, hp.tts_model_id)
        print("hello")
        print(paths.base)
        if not self.args.force_cpu and torch.cuda.is_available():
            device = torch.device('cuda')
        else:
            device = torch.device('cpu')
        print('Using device:', device)
    
    
        # === Wavernn === #
        if self.args.vocoder == 'wavernn':
            print('\nInitialising WaveRNN Model...\n')
            self.voc_model = WaveRNN(rnn_dims=hp.voc_rnn_dims,
                                fc_dims=hp.voc_fc_dims,
                                bits=hp.bits,
                                pad=hp.voc_pad,
                                upsample_factors=hp.voc_upsample_factors,
                                feat_dims=hp.num_mels,
                                compute_dims=hp.voc_compute_dims,
                                res_out_dims=hp.voc_res_out_dims,
                                res_blocks=hp.voc_res_blocks,
                                hop_length=hp.hop_length,
                                sample_rate=hp.sample_rate,
                                mode=hp.voc_mode).to(device)
    
            voc_load_path = self.args.voc_weights if self.args.voc_weights else paths.voc_latest_weights
            #print(paths.voc_latest_weights)
            self.voc_model.load(voc_load_path)
    
        # === Tacotron === #
        if hp.tts_model == 'tacotron':
            print('\nInitialising Tacotron Model...\n')
            self.tts_model = Tacotron(embed_dims=hp.tts_embed_dims,
                                num_chars=len(symbols),
                                encoder_dims=hp.tts_encoder_dims,
                                decoder_dims=hp.tts_decoder_dims,
                                n_mels=hp.num_mels,
                                fft_bins=hp.num_mels,
                                postnet_dims=hp.tts_postnet_dims,
                                encoder_K=hp.tts_encoder_K,
                                lstm_dims=hp.tts_lstm_dims,
                                postnet_K=hp.tts_postnet_K,
                                num_highways=hp.tts_num_highways,
                                dropout=hp.tts_dropout,
                                stop_threshold=hp.tts_stop_threshold).to(device)
        
            tts_load_path = self.args.tts_weights if self.args.tts_weights else paths.tts_latest_weights
            self.tts_model.load(tts_load_path)

        # === Tacotron2 === #
        elif hp.tts_model == 'tacotron2':
            print('\nInitializing Tacotron2 Model...\n')
            self.tts_model = Tacotron2().to(device)
            tts_load_path = self.args.tts_weights if self.args.tts_weights else paths.tts_latest_weights
            self.tts_model.load(tts_load_path)      


        # === Infomation === #
        if hp.tts_model == 'tacotron':
            if self.args.vocoder == 'wavernn':
                voc_k = self.voc_model.get_step() // 1000
                tts_k = self.tts_model.get_step() // 1000
        
                simple_table([('Tacotron', str(tts_k) + 'k'),
                            ('r', self.tts_model.r),
                            ('Vocoder Type', 'WaveRNN'),
                            ('WaveRNN', str(voc_k) + 'k'),
                            ('Generation Mode', 'Batched' if self.args.batched else 'Unbatched'),
                            ('Target Samples', self.args.target if self.args.batched else 'N/A'),
                            ('Overlap Samples', self.args.overlap if self.args.batched else 'N/A')])
        
            elif self.args.vocoder == 'griffinlim':
                tts_k = self.tts_model.get_step() // 1000
                simple_table([('Tacotron', str(tts_k) + 'k'),
                            ('r', self.tts_model.r),
                            ('Vocoder Type', 'Griffin-Lim'),
                            ('GL Iters', self.args.iters)])

        elif hp.tts_model == 'tacotron2':
            if self.args.vocoder == 'wavernn':
                voc_k = self.voc_model.get_step() // 1000
                tts_k = self.tts_model.get_step() // 1000

                simple_table([('Tacotron2', str(tts_k) + 'k'),
                            ('Vocoder Type', 'WaveRNN'),
                            ('WaveRNN', str(voc_k) + 'k'),
                            ('Generation Mode', 'Batched' if self.args.batched else 'Unbatched'),
                            ('Target Samples', self.args.target if self.args.batched else 'N/A'),
                            ('Overlap Samples', self.args.overlap if self.args.batched else 'N/A')])

            elif self.args.vocoder == 'griffinlim':
                tts_k = self.tts_model.get_step() // 1000
                simple_table([('Tacotron2', str(tts_k) + 'k'),
                            ('Vocoder Type', 'Griffin-Lim'),
                            ('GL Iters', self.args.iters)])
        
    def generate(self, 華, input_text):
        inputs = [text_to_sequence(input_text.strip(), ['basic_cleaners'])]
        if hp.tts_model == 'tacotron2':
            self.gen_tacotron2(華, inputs)

        elif hp.tts_model == 'tacotron':
            self.gen_tacotron(華, inputs)

        else:
            print(f"Wrong tts model type {{{tts_model_type}}}")

        print('\n\nDone.\n')

    # custom function
    def gen_tacotron2(self, 華, inputs):
        for i, x in enumerate(inputs, 1):
            print(f'\n| Generating {i}/{len(inputs)}')
            print(x)

            x = np.array(x)[None, :]
            x = torch.autograd.Variable(torch.from_numpy(x)).cuda().long()
            
            self.tts_model.eval()
            mel_outputs, mel_outputs_postnet, _, alignments = self.tts_model.inference(x)
            if self.args.vocoder == 'griffinlim':
                v_type = self.args.vocoder
            elif self.args.vocoder == 'wavernn' and self.args.batched:
                v_type = 'wavernn_batched'
            else:
                v_type = 'wavernn_unbatched'

            # == define output name == #
            if len(華) == 0:
                output_name = re.split(r'\,|\.|\!|\?| ', input_text)[0]
            elif 1 <= len(華) <= 9:
                output_name = 華[:-1]
            elif 9 < len(華):
                output_name = 華[:8]
            print(output_name)            
            save_path = "output/{}.wav".format(output_name)
            ## 

            if self.args.vocoder == 'wavernn':
                m = mel_outputs_postnet
                self.voc_model.generate(m, save_path, self.args.batched, hp.voc_target, hp.voc_overlap, hp.mu_law)

            elif self.args.vocoder == 'griffinlim':
                m = torch.squeeze(mel_outputs_postnet).detach().cpu().numpy()
                wav = reconstruct_waveform(m, n_iter=self.args.iters)
                save_wav(wav, save_path)

    # custom function
    def gen_tacotron(self, 華, inputs):
        for i, x in enumerate(inputs, 1):
            print(f'\n| Generating {i}/{len(inputs)}')
            _, m, attention = self.tts_model.generate(x)
            # Fix mel spectrogram scaling to be from 0 to 1
            m = (m + 4) / 8
            np.clip(m, 0, 1, out=m)
    
            if self.args.vocoder == 'griffinlim':
                v_type = self.args.vocoder
            elif self.args.vocoder == 'wavernn' and self.args.batched:
                v_type = 'wavernn_batched'
            else:
                v_type = 'wavernn_unbatched'
            # == define output name == #
            if len(華) == 0:
                output_name = re.split(r'\,|\.|\!|\?| ', input_text)[0]
            elif 1 <= len(華) <= 9:
                output_name = 華[:-1]
            elif 9 < len(華):
                output_name = 華[:8]
            print(output_name)            
            save_path = "output/{}.wav".format(output_name)
            ## 
            if self.args.vocoder == 'wavernn':
                m = torch.tensor(m).unsqueeze(0)
                self.voc_model.generate(m, save_path, self.args.batched, hp.voc_target, hp.voc_overlap, hp.mu_law)
                
            elif self.args.vocoder == 'griffinlim':
                wav = reconstruct_waveform(m, n_iter=self.args.iters)
                save_wav(wav, save_path)

