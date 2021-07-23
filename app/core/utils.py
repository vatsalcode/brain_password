from itertools import chain, islice
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from app.core.configuration import settings

import matplotlib.pyplot as plt
import numpy as np


SQRT2 = K.sqrt(K.constant(2.0))


def create_chunks(iterable, size=int(settings.figsize_width*100)):
  iterator = iter(iterable)
  for first in iterator:
    yield list(chain([first], islice(iterator, size - 1)))


def unflatten_spectrogram(spectrogram_1d):
  spectrogram_2d =  np.array(list(create_chunks(spectrogram_1d)))
  spectrogram_2d = np.reshape(spectrogram_2d, (spectrogram_2d.shape[0], spectrogram_2d.shape[1], 1))
  return spectrogram_2d


def contrastive_loss(y_true, y_pred):
  margin = settings.margin
  return K.mean((1.0 - y_true) * K.square(y_pred) + (y_true) * K.square(K.maximum(margin - y_pred, 0.0)))


def load_network(network_path):
  return load_model(network_path, custom_objects={"contrastive_loss": contrastive_loss, "SQRT2": SQRT2})