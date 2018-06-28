from pprint import pprint
import tempfile
import os
import zipfile
import requests
import json
import pandas
import numpy as np
import optparse
from keras.models import Sequential, load_model, model_from_json
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
import os
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

MODEL_PATH = os.getenv('CSIRTGSDK_TM_PATH', os.getcwd())


class Threatmodel(object):
    """
    Represents a ThreatModel Object
    """
    def __init__(self, client):
        self.client = client

    @staticmethod
    def predict(i, path):
        tokenizer = Tokenizer(filters='\t\n', char_level=True)
        word_dict_file = os.path.join(path, 'word-dict.json')

        with open(word_dict_file) as F:
            txt = F.read()

        txt = json.loads(txt)
        tokenizer.word_index = txt

        seq = tokenizer.texts_to_sequences(i)
        max_log_length = 255
        i_processed = sequence.pad_sequences(seq, maxlen=max_log_length)

        model = load_model(os.path.join(path, 'model.h5'))
        model.load_weights(os.path.join(path, 'weights.h5'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        prediction = model.predict(i_processed)
        return prediction

    @staticmethod
    def _get_model(url, path):
        s = requests.session()
        resp = s.get(url)
        path2 = os.path.join(path, 'model.zip')
        with open(path2, 'wb') as F:
            F.write(resp.content)

        with zipfile.ZipFile(path2) as zipref:
            zipref.extractall(path)

    def show(self, user, name, i, path=MODEL_PATH):
        path = os.path.join(path, '_'.join([user, name]))

        if not os.path.isdir(path):
            os.mkdir(path)

        if not os.path.isfile(os.path.join(path, 'model.h5')):
            uri = self.client.remote + '/users/{0}/threatmodels/{1}'.format(user, name)
            m = self.client.get(uri, params={})

            # download model
            self._get_model(m['model']['url'], path)

        return self.predict(i, path)
