# coding: utf-8
from __future__ import unicode_literals

import re

from .regexp import build_good_phrase, build_bad_phrase


bad_words = [
    build_bad_phrase('п еи з д'),
    build_bad_phrase('х у йёуяию'),
    build_bad_phrase('о х у е втл'),
    build_bad_phrase('п и д оеа р'),
    build_bad_phrase('п и д р'),
    build_bad_phrase('её б а нклт'),
    build_bad_phrase('у её б оа нтк'),
    build_bad_phrase('её б л аои'),
    build_bad_phrase('в ы её б'),
    build_bad_phrase('е б ё т'),
    build_bad_phrase('св ъь еёи б'),
    build_bad_phrase('б л я'),
    build_bad_phrase('г оаo в н'),
    build_bad_phrase('м у д а к'),
    build_bad_phrase('г ао н д о н'),
    build_bad_phrase('ч м оы'),
    build_bad_phrase('д е р ь м'),
    build_bad_phrase('ш л ю х'),
    build_bad_phrase('з ао л у п'),
    build_bad_phrase('с у ч а р'),
    build_bad_phrase('д ао л б ао её б'),
    build_bad_phrase('п р ао её б'),
    build_bad_phrase('с у к а'),
    build_bad_phrase('д р оа ч'),
    build_bad_phrase('х у е с о с'),
    build_bad_phrase('х у йя'),
    build_bad_phrase('е б ать'),
    build_bad_phrase('м а н д а'),
    build_bad_phrase('м у д л оае'),
]
bad_words_re = re.compile('|'.join(bad_words), re.IGNORECASE | re.UNICODE)

good_words = [
    build_good_phrase('х л е б а л оа'),
    build_good_phrase('с к и п и д а р'),
    build_good_phrase('к о л е б а н и яей'),
    build_good_phrase('к о м а н д а'),
    build_good_phrase('з ао к оа л е б а лт'),
    build_good_phrase('р у б л я'),
    build_good_phrase('с т е б е л ь'),
    build_good_phrase('с т р а х о в к ауи'),
    build_good_phrase('в с е м у д а ч и'),
    build_good_phrase('к н и г а'),
    build_good_phrase('м а р к с у'),
    build_good_phrase('р а с х о ж д е н'),
    build_good_phrase('н е б л а г о п р и я т'),
    r'([о][с][к][о][Р][б][л][я]([т][ь])*([л])*([е][ш][ь])*)',
    r'([в][л][ю][б][л][я](([т][ь])([с][я])*)*(([е][ш][ь])([с][я])*)*)',
    r'((([п][о][д])*([з][а])*([п][е][р][е])*)*[с][т][р][а][х][у]([й])*([с][я])*([е][ш][ь])*([е][т])*)',
    r'([м][е][б][е][л][ь]([н][ы][й])*)',
    r'([Уу][Пп][Оо][Тт][Рр][Ее][Бб][Лл][Яя]([Тт][Ьь])*([Ее][Шш][Ьь])*([Яя])*([Лл])*)',
    r'([Ии][Сс][Тт][Рр][Ее][Бб][Лл][Яя]([Тт][Ьь])*([Ее][Шш][Ьь])*([Яя])*([Лл])*)',
    r'([Сс][Тт][Рр][Аа][Хх]([Аа])*)',
]
good_words_re = re.compile('|'.join(good_words), re.IGNORECASE | re.UNICODE)
