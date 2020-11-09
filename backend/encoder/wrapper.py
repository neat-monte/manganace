import pickle
from pathlib import Path

import numpy as np
import tensorflow as tf
from sqlalchemy.orm import Session

import dnnlib
from .model import Generator

BASE_DIR = Path.cwd() / '_pickles'
PICKLED_GEN = BASE_DIR / 'stylegan2-ffhq-config-f.pkl'
PICKLED_EMOTIONS_VECTORS = BASE_DIR / 'emotion_directions_in_latent_space.pkl'


class GeneratorWrapper:
    multiplier_scale = 0.1

    def __init__(self, emotions_name_weight_by_id):
        # Initialize the tensorflow session
        dnnlib.tflib.init_tf()
        self.tf_session = tf.get_default_session()
        # Load networks from weights file
        with open(PICKLED_GEN, "rb") as file:
            _, _, self.Gs = pickle.load(file)
        # Load emotion vectors
        with open(PICKLED_EMOTIONS_VECTORS, "rb") as file:
            self.emotion_vectors = pickle.load(file)
        # Initialize the generator
        self.generator = Generator(self.Gs, batch_size=1, randomize_noise=False)
        self.emotions_name_weight_by_id = emotions_name_weight_by_id

    def _get_latent_state(self, seed, truncation_psi=0.5):
        """ Given a seed [0..2^31-1] produce a latent state point """
        random_state = np.random.RandomState(np.asarray(seed))
        latents = random_state.randn(1, self.Gs.input_shape[1])
        all_w = self.Gs.components.mapping.run(latents, None)
        average_latent = self.Gs.get_var("dlatent_avg")
        return average_latent + (all_w - average_latent) * truncation_psi

    def _apply_emotions(self, latent_state, emotions):
        """ Apply emotions with provided multipliers """
        latent_state = latent_state.reshape((1, 18 * 512))
        for emotion in emotions:
            (emo_name, emo_weight) = self.emotions_name_weight_by_id[emotion.id]
            multiplier = emotion.multiplier * self.multiplier_scale
            emotion_vector = self.emotion_vectors[f'neutral->{emo_name}']
            weighted_emotion_vector = emotion_vector * emo_weight
            scaled_emotion_vector = weighted_emotion_vector * multiplier
            latent_state += scaled_emotion_vector
        return latent_state.reshape((1, 18, 512))

    def _generate_image(self, latent_state):
        """ Generate image of the provided latent state """
        self.generator.set_dlatents(latent_state)
        img_array = self.generator.generate_images()[0]
        self.generator.reset_dlatents()
        return img_array

    def generate(self, seed: int, emotions=None):
        """ Generation pipeline, make latent state from a seed, apply emotion vectors, and generate an image """
        with self.tf_session.as_default():
            latent_state = self._get_latent_state(seed)
            if emotions:
                self._apply_emotions(latent_state, emotions)
            return self._generate_image(latent_state)
