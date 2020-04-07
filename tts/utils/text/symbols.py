""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. '''
from utils.text import cmudict

_pad = '_'
_punctuation = '!\'(),.:;? '
_special = '-'
_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
_ipa = 'ŋəɛɨʔʰ̩ⁿ'

_sooji = '0123456789'

# Export all symbols:
symbols = [_pad] + list(_special) + list(_punctuation) + list(_letters) + list(_ipa) + list(_sooji)

