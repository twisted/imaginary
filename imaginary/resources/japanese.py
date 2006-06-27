"""
Japanese language data.

This module contains a dict named 'hiragana' which maps hiragana
unicode characters to romaji pronunciations, as well as a
'romajiToHiragana' dict which maps romaji pronunciation to *lists* of
hiragana characters. There are multiple hiragana characters with the
same pronunciation, thus the multiple values per romaji in the
romajiToHiragana dict.

"""


# Hiragana.
hiragana = {
    u'\u3042': 'A', u'\u3044': 'I', u'\u3046': 'U', u'\u3048': 'E',
    u'\u3081': 'ME', u'\u3080': 'MU', u'\u3082': 'MO', u'\u3084': 'YA',
    u'\u3086': 'YU', u'\u3089': 'RA', u'\u3088': 'YO', u'\u308b': 'RU',
    u'\u308a': 'RI', u'\u308d': 'RO', u'\u308c': 'RE', u'\u308f': 'WA',
    u'\u3091': 'WE', u'\u3090': 'WI', u'\u3093': 'N', u'\u3092': 'WO',
    u'\u304b': 'KA', u'\u304a': 'O', u'\u304d': 'KI', u'\u304c': 'GA',
    u'\u304f': 'KU', u'\u304e': 'GI', u'\u3051': 'KE', u'\u3050': 'GU',
    u'\u3053': 'KO', u'\u3052': 'GE', u'\u3055': 'SA', u'\u3054': 'GO',
    u'\u3057': 'SHI',u'\u3056': 'ZA', u'\u3059': 'SU', u'\u3058': 'JI',
    u'\u305b': 'SE', u'\u305a': 'ZU', u'\u305d': 'SO', u'\u305c': 'ZE',
    u'\u305f': 'TA', u'\u305e': 'ZO', u'\u3061': 'CHI', u'\u3060': 'DA',
    u'\u3062': 'JI', u'\u3065': 'ZU', u'\u3064': 'TSU', u'\u3067': 'DE',
    u'\u3066': 'TE', u'\u3069': 'DO', u'\u3068': 'TO', u'\u306b': 'NI',
    u'\u306a': 'NA', u'\u306d': 'NE', u'\u306c': 'NU', u'\u306f': 'HA',
    u'\u306e': 'NO', u'\u3071': 'PA', u'\u3070': 'BA', u'\u3073': 'BI',
    u'\u3072': 'HI', u'\u3075': 'FU', u'\u3074': 'PI', u'\u3077': 'PU',
    u'\u3076': 'BU', u'\u3079': 'BE', u'\u3078': 'HE', u'\u307b': 'HO',
    u'\u307a': 'PE', u'\u307d': 'PO', u'\u307c': 'BO', u'\u307f': 'MI',
    u'\u307e': 'MA'}


romajiToHiragana = {}
for k, v in hiragana.iteritems():
    romajiToHiragana.setdefault(v, []).append(k)

# Katakana.
# katakana = {
#     }
