#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import configurations
from train import train_process

if __name__ == '__main__':
    config = configurations()
    print('config : \n', vars(config))
    train_losses, val_losses, bleu_scores = train_process(config)
