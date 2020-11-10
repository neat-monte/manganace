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

    def __init__(self, vector_effect_weight_by_id):
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
        self.vector_effect_weight_by_id = vector_effect_weight_by_id

    def _get_latent_state(self, seed, truncation_psi=0.5):
        """ Given a seed [0..2^31-1] produce a latent state point """
        random_state = np.random.RandomState(np.asarray(seed))
        latents = random_state.randn(1, self.Gs.input_shape[1])
        all_w = self.Gs.components.mapping.run(latents, None)
        average_latent = self.Gs.get_var("dlatent_avg")
        return average_latent + (all_w - average_latent) * truncation_psi

    def _apply_vectors(self, latent_state, vectors):
        """ Apply emotions with provided multipliers """
        latent_state = latent_state.reshape((1, 18 * 512))
        for vector in vectors:
            (v_effect, v_weight) = self.vector_effect_weight_by_id[vector.id]
            multiplier = vector.multiplier * self.multiplier_scale
            emotion_vector = self.emotion_vectors[f'neutral->{v_effect}']
            weighted_emotion_vector = emotion_vector * v_weight
            scaled_emotion_vector = weighted_emotion_vector * multiplier
            latent_state += scaled_emotion_vector
        return latent_state.reshape((1, 18, 512))

    def _generate_image(self, latent_state):
        """ Generate image of the provided latent state """
        self.generator.set_dlatents(latent_state)
        img_array = self.generator.generate_images()[0]
        self.generator.reset_dlatents()
        return img_array

    def generate(self, seed: int, vectors=None):
        """ Generation pipeline, make latent state from a seed, apply emotion vectors, and generate an image """
        with self.tf_session.as_default():
            latent_state = self._get_latent_state(seed)
            if vectors:
                self._apply_vectors(latent_state, vectors)
            return self._generate_image(latent_state)
