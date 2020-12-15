
# Here are the input and output data paths (Note: you can override wav_path in preprocess.py)
wav_path = '/Home/kaiwei/TaiwaneseSpeech/SuiSiann-0.2/0.2'
data_path = './data/'

# model ids are separate - that way you can use a new tts with an old wavernn and vice versa
# NB: expect undefined behaviour if models were trained on different DSP settings
voc_model = 'wavernn'
tts_model = 'tacotron2'

voc_model_id = voc_model
tts_model_id = tts_model

# temp
if tts_model == 'tacotron2':
    old_input_style = False
elif tts_model == 'tacotron':
    old_input_style = True
    
#=== Bogi === #
is_cuda=True
pin_mem = True
p = 10 # mel spec loss penalty
sch=True
sch_step = 4000
lr = 2e-3
betas = (0.9, 0.999)
eps = 1e-6
weight_decay=1e-6
batch_size =32
max_step=300e3
# DSP --------------------------------------------------------------------------------------------------------------#

# Settings for all models
sample_rate = 22050
n_fft = 1024
fft_bins = n_fft // 2 + 1
num_mels = 80
hop_length = 275
win_length = 1024
fmin = 40          #
min_level_db = -100# wavernn config
ref_level_db = 20  #
mu_law = True      # 
peak_norm = False  # 


################################
#  WAVERNN / VOCODER           #
################################

# Model Hparams
# 2020.12.06: guess: for small dataset, don't use MOL. It's hard to converge.
if voc_model == 'wavernn':
    voc_mode = 'RAW'                    # either 'RAW' (softmax on raw bits) or 'MOL' (sample from mixture of logistics)
    voc_upsample_factors = (5, 5, 11)   # NB - this needs to correctly factorise hop_length
    voc_rnn_dims = 512
    voc_fc_dims = 512
    voc_compute_dims = 128
    voc_res_out_dims = 128
    voc_res_blocks = 10

    if voc_mode == 'MOL':
        bits = 16
    else:
        bits = 9

    # Training
    voc_batch_size = 32
    voc_lr = 1e-4
    voc_checkpoint_every = 25_000
    voc_gen_at_checkpoint = 5           # number of samples to generate at each checkpoint
    voc_total_steps = 1_000_000         # Total number of training steps
    voc_test_samples = 50               # How many unseen samples to put aside for testing
    voc_pad = 2                         # this will pad the input so that the resnet can 'see' wider than input length
    voc_seq_len = hop_length * 5        # must be a multiple of hop_length
    voc_clip_grad_norm = 4              # set to None if no gradient clipping needed

    # Generating / Synthesizing
    voc_gen_batched = True              # very fast (realtime+) single utterance batched generation
    voc_target = 11_000                 # target number of samples to be generated in each batch entry
    voc_overlap = 550                   # number of samples for crossfading between batches


    # TACOTRON/TTS -----------------------------------------------------------------------------------------------------#
    ignore_tts = False


# !!! TTS !!! #
tts_max_mel_len = 1250              # if you have a couple of extremely long spectrograms you might want to use this
tts_bin_lengths = True              # bins the spectrogram lengths before sampling in data loader - speeds up training
tts_clip_grad_norm = 1.0            # clips the gradient norm to prevent explosion - set to None if not needed
tts_checkpoint_every = 10000        # checkpoints the model every X steps

################################
# Tacotron 2  Config           #
################################
if tts_model == 'tacotron2':
    n_mel_channels = num_mels
    fp16_run=False
    mask_padding=True
    distributed_run=False
    cudnn_enabled=True
    cudnn_benchmark=False
    ignore_layers=['embedding.weight']
    dynamic_loss_scaling=True
    iters_per_checkpoint=1000


    from utils.text import symbols
    n_symbols=len(symbols)  #in model config
    #symbols_embedding_dim=512  
    symbols_embedding_dim=256
    # === Encoder === #
    encoder_kernel_size=5
    encoder_n_convolutions=3
    encoder_embedding_dim=256
    #encoder_embedding_dim=512

    # === Decoder === #
    n_frames_per_step=3  # currently only 1 is supported
    decoder_rnn_dim=512  # 1024
    prenet_dim=64        # 256
    max_decoder_steps=1000
    gate_threshold=0.5
    p_attention_dropout=0.1
    p_decoder_dropout=0.1

    # === Attention === #
    attention_rnn_dim=512 # 1024
    attention_dim=128
    # Location Layer parameters
    attention_location_n_filters=32
    attention_location_kernel_size=31

    # === Postnet === #
    # Mel-post processing network parameters
    postnet_embedding_dim=512
    postnet_kernel_size=5
    postnet_n_convolutions=5
    
    tts_schedule = [(1e-3,  10_000,  16),   # progressive training schedule
                    (1e-3, 100_000,  16),   # (lr, step, batch_size)
                    (1e-4, 180_000,  16),
                    (1e-4, 350_000,  8)]
    #weight_decay=1e-6

    text_cleaners = ['basic_cleaners']

################################
# Tacotron 1  Config           #
################################
elif tts_model == 'tacotron':
    tts_embed_dims = 256                # embedding dimension for the graphemes/phoneme inputs
    tts_encoder_dims = 128
    tts_decoder_dims = 256
    tts_postnet_dims = 128
    tts_encoder_K = 16
    tts_lstm_dims = 512
    tts_postnet_K = 8
    tts_num_highways = 4
    tts_dropout = 0.5
    tts_cleaner_names = ['basic_cleaners']
    tts_stop_threshold = -3.4           # Value below which audio generation ends.
                                        # For example, for a range of [-4, 4], this
                                        # will terminate the sequence at the first
                                        # frame that has all values < -3.4
    # Training
    tts_schedule = [(7,  1e-3,  10_000,  32),   # progressive training schedule
                    (5,  1e-4, 100_000,  32),   # (r, lr, step, batch_size)
                    (2,  1e-4, 180_000,  16),
                    (2,  1e-4, 350_000,  8)]
    # TODO: tts_phoneme_prob = 0.0              # [0 <-> 1] probability for feeding model phonemes vrs graphemes


# ------------------------------------------------------------------------------------------------------------------#

