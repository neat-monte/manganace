import pickle
from pathlib import Path
from typing import List, Tuple, Dict

import numpy as np
import tensorflow as tf

import dnnlib
from .model import Generator

BASE_DIR = Path.cwd() / '_pickles'
PICKLED_GEN = BASE_DIR / 'stylegan2-ffhq-config-f.pkl'
PICKLED_EMOTIONS_VECTORS = BASE_DIR / 'emotion_directions_in_latent_space.pkl'


class GeneratorWrapper:
    batch_size, random_noise, tf_session, Gs, generator, emotion_vectors, vectors \
        = None, None, None, None, None, None, None

    def __init__(self, batch_size: int, random_noise: bool, vectors: Dict[int, Tuple[str, float]]):
        self.batch_size = batch_size
        self.random_noise = random_noise
        # Initialize the tensorflow session
        dnnlib.tflib.init_tf()
        self.tf_session = tf.get_default_session()
        self.vectors = vectors
        self.__start_generator(batch_size, random_noise)

    def restart_generator(self, batch_size: int, random_noise: bool):
        self.batch_size = batch_size
        self.random_noise = random_noise
        # Close and reinitialize the tensorflow session
        # self.tf_session.close()
        # dnnlib.tflib.init_tf()
        # self.tf_session = tf.get_default_session()
        self.__start_generator(batch_size, random_noise)

    def __start_generator(self, batch_size: int, random_noise: bool):
        with self.tf_session.as_default():
            # Load networks from weights file
            with open(PICKLED_GEN, "rb") as file:
                _, _, self.Gs = pickle.load(file)
            # Load emotion vectors
            with open(PICKLED_EMOTIONS_VECTORS, "rb") as file:
                self.emotion_vectors = pickle.load(file)
            # Initialize the generator
            self.generator = Generator(self.Gs, batch_size, random_noise)

    def get_latent_state(self, seed: int, truncation_psi: float = 0.5):
        """ Given a seed in the [0, 2^31-1] interval, produce a latent state """
        random_state = np.random.RandomState(np.asarray(seed))
        latents = random_state.randn(1, self.Gs.input_shape[1])
        with self.tf_session.as_default():
            all_w = self.Gs.components.mapping.run(latents, None)
            average_latent = self.Gs.get_var("dlatent_avg")
        return average_latent + (all_w - average_latent) * truncation_psi

    def get_latent_states(self, seeds: List[int], truncation_psi: float = 0.5):
        """ Given an array of seeds in the [0, 2^31-1] interval, produce an array of latent states """
        random_state = np.random.RandomState(np.asarray(seeds[0]))
        latents = random_state.randn(1, self.Gs.input_shape[1])
        for seed in seeds[1:]:
            random_state.seed(seed)
            latent = random_state.randn(1, self.Gs.input_shape[1])
            latents = np.append(latents, latent, axis=0)
        with self.tf_session.as_default():
            all_w = self.Gs.components.mapping.run(latents, None)
            average_latent = self.Gs.get_var("dlatent_avg")
        return average_latent + (all_w - average_latent) * truncation_psi

    def apply_vectors_to_latent(self, latent_state, vectors: List[Tuple[int, float]]):
        """ Apply emotions with provided multipliers """
        latent_state = latent_state.reshape((latent_state.shape[0], 18 * 512))
        for (v_id, v_multiplier) in vectors:
            (v_effect, v_weight) = self.vectors[v_id]
            emotion_vector = self.emotion_vectors[f'neutral->{v_effect}']
            weighted_emotion_vector = emotion_vector * v_weight
            scaled_emotion_vector = weighted_emotion_vector * v_multiplier
            latent_state += scaled_emotion_vector
        return latent_state.reshape((latent_state.shape[0], 18, 512))

    def generate_from_latent(self, latent_state, add_padding: bool = True):
        """ Generate image of the provided latent state. Given that the latent state
        dimensions to not match batch size - a padding shall be added, and removed afterwards """
        assert (latent_state.shape[0] <= self.batch_size and latent_state.shape[1:] == (18, 512))
        diff = self.batch_size - latent_state.shape[0]
        # In case batch size does not match - add padding
        if 0 < diff and add_padding:
            latent_state = np.append(latent_state, np.empty((diff, 18, 512)), axis=0)
        with self.tf_session.as_default():
            self.generator.set_dlatents(latent_state)
            img_array = self.generator.generate_images()
            self.generator.reset_dlatents()
        # In case a padding was added - remove random images
        if 0 < diff and add_padding:
            img_array = img_array[:latent_state.shape[0] - diff]
        return img_array

    def generate(self, seed: int, vectors: List[Tuple[int, float]] = None):
        """ Generation pipeline, make latent state from a seed, apply emotion vectors, and generate an image """
        ls = self.get_latent_state(seed)
        if vectors:
            self.apply_vectors_to_latent(ls, vectors)
        return self.generate_from_latent(ls)
