import torch
from models.wavernn import WaveRNN
from models.tacotron2 import Tacotron2
from utils import hparams as hp
from utils.text.symbols import symbols
from utils.paths import Paths

import argparse
from utils.text import text_to_sequence
from utils.display import save_attention, simple_table
from utils.dsp import reconstruct_waveform, save_wav
import numpy as np

def gen_samples(tts_model, sample_set, paths, vocoder='griffinlim'):
    tts_model.eval()
    tts_k = tts_model.get_step() // 1000

    for i, batch in enumerate(sample_set, 1):
        text, mel, item_id = batch
        text = text.long().cuda()

        mel_outputs, mel_outputs_postnet, _, alignments = tts_model.inference(text)

        if vocoder == 'griffinlim':
            m = torch.squeeze(mel_outputs_postnet).detach().cpu().numpy()
            wav = reconstruct_waveform(m, n_iter=32)
            save_path = paths.tts_samples/f'{i}_griffinlim_{tts_k}k.wav'
            save_wav(wav, save_path)
        
    tts_model.train()


if __name__ == "__main__":

    # Parse Arguments
    parser = argparse.ArgumentParser(description='TTS Generator')
    parser.add_argument('--input_text', '-i', type=str, help='[string] Type in something here and TTS will generate it!')
    parser.add_argument('--tts_weights', type=str, help='[string/path] Load in different Tacotron weights')
    parser.add_argument('--save_attention', '-a', dest='save_attn', action='store_true', help='Save Attention Plots')
    parser.add_argument('--force_cpu', '-c', action='store_true', help='Forces CPU-only training, even when in CUDA capable environment')
    parser.add_argument('--hp_file', metavar='FILE', default='hparams.py', help='The file to use for the hyperparameters')

    parser.set_defaults(input_text=None)
    parser.set_defaults(weights_path=None)

    # name of subcommand goes to args.vocoder
    subparsers = parser.add_subparsers(required=True, dest='vocoder')

    wr_parser = subparsers.add_parser('wavernn', aliases=['wr'])
    wr_parser.add_argument('--batched', '-b', dest='batched', action='store_true', help='Fast Batched Generation')
    wr_parser.add_argument('--unbatched', '-u', dest='batched', action='store_false', help='Slow Unbatched Generation')
    wr_parser.add_argument('--overlap', '-o', type=int, help='[int] number of crossover samples')
    wr_parser.add_argument('--target', '-t', type=int, help='[int] number of samples in each batch index')
    wr_parser.add_argument('--voc_weights', type=str, help='[string/path] Load in different WaveRNN weights')
    wr_parser.set_defaults(batched=None)

    gl_parser = subparsers.add_parser('griffinlim', aliases=['gl'])
    gl_parser.add_argument('--iters', type=int, default=32, help='[int] number of griffinlim iterations')

    args = parser.parse_args()

    if args.vocoder in ['griffinlim', 'gl']:
        args.vocoder = 'griffinlim'
    elif args.vocoder in ['wavernn', 'wr']:
        args.vocoder = 'wavernn'
    else:
        raise argparse.ArgumentError('Must provide a valid vocoder type!')

    hp.configure(args.hp_file)  # Load hparams from file
    # set defaults for any arguments that depend on hparams
    if args.vocoder == 'wavernn':
        if args.target is None:
            args.target = hp.voc_target
        if args.overlap is None:
            args.overlap = hp.voc_overlap
        if args.batched is None:
            args.batched = hp.voc_gen_batched

        batched = args.batched
        target = args.target
        overlap = args.overlap

    input_text = args.input_text
    tts_weights = args.tts_weights
    save_attn = args.save_attn

    paths = Paths(hp.data_path, hp.voc_model_id, hp.tts_model_id)

    if not args.force_cpu and torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    print('Using device:', device)


    # === WaveRNN === #
    if args.vocoder == 'wavernn':
        print('\nInitialising WaveRNN Model...\n')
        # Instantiate WaveRNN Model
        voc_model = WaveRNN(rnn_dims=hp.voc_rnn_dims,
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

        voc_load_path = args.voc_weights if args.voc_weights else paths.voc_latest_weights
        voc_model.load(voc_load_path)

    print('\nInitialising Tacotron Model...\n')

    # === Tacotron2 === #
    # Instantiate Tacotron Model
    tts_model = Tacotron2().to(device)
    tts_load_path = tts_weights if tts_weights else paths.tts_latest_weights
    tts_model.load(tts_load_path)

    # === Text === #
    if input_text:
        inputs = [text_to_sequence(input_text.strip(), hp.text_cleaners)]
    else:
        with open('sentences.txt') as f:
            inputs = [text_to_sequence(l.strip(), hp.text_cleaners) for l in f]

    # === Infomation === #
    if args.vocoder == 'wavernn':
        voc_k = voc_model.get_step() // 1000
        tts_k = tts_model.get_step() // 1000

        simple_table([('Tacotron2', str(tts_k) + 'k'),
                    ('Vocoder Type', 'WaveRNN'),
                    ('WaveRNN', str(voc_k) + 'k'),
                    ('Generation Mode', 'Batched' if batched else 'Unbatched'),
                    ('Target Samples', target if batched else 'N/A'),
                    ('Overlap Samples', overlap if batched else 'N/A')])

    elif args.vocoder == 'griffinlim':
        tts_k = tts_model.get_step() // 1000
        simple_table([('Tacotron2', str(tts_k) + 'k'),
                    ('Vocoder Type', 'Griffin-Lim'),
                    ('GL Iters', args.iters)])

    # === Generate === #
    for i, x in enumerate(inputs, 1):
        print(f'\n| Generating {i}/{len(inputs)}')
        print(x)

        x = np.array(x)[None, :]
        x = torch.autograd.Variable(torch.from_numpy(x)).cuda().long()
        
        tts_model.eval()
        mel_outputs, mel_outputs_postnet, _, alignments = tts_model.inference(x)
        if args.vocoder == 'griffinlim':
            v_type = args.vocoder
        elif args.vocoder == 'wavernn' and args.batched:
            v_type = 'wavernn_batched'
        else:
            v_type = 'wavernn_unbatched'

        if input_text:
            save_path = paths.tts_output/f'__input_{input_text[:10]}_{v_type}_{tts_k}k.wav'
        else:
            save_path = paths.tts_output/f'{i}_{v_type}_{tts_k}k.wav'

        if save_attn: save_attention(attention, save_path)

        if args.vocoder == 'wavernn':
            m = mel_outputs_postnet
            voc_model.generate(m, save_path, batched, hp.voc_target, hp.voc_overlap, hp.mu_law)
        elif args.vocoder == 'griffinlim':
            m = torch.squeeze(mel_outputs_postnet).detach().cpu().numpy()
            wav = reconstruct_waveform(m, n_iter=args.iters)
            save_wav(wav, save_path)

    print('\n\nDone.\n')
