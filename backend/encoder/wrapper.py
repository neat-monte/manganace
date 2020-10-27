import pickle
from pathlib import Path

import tensorflow as tf
import numpy as np

import dnnlib
from .model import Generator

PICKLED_GEN = 'stylegan2-ffhq-config-f.pkl'


class GeneratorWrapper:
    def __init__(self):
        # Initialize the tensorflow session
        dnnlib.tflib.init_tf()
        self.tf_session = tf.get_default_session()
        # Load networks from weights file
        pickled = Path.cwd() / 'weights' / PICKLED_GEN
        with open(pickled, "rb") as file:
            _, _, self.Gs = pickle.load(file)
        # Initialize the generator
        self.generator = Generator(self.Gs, batch_size=1, randomize_noise=True)

    def generate_image_from_seed(self, seed, truncation_psi=0.5, return_latent=False):
        with self.tf_session.as_default():
            w_avg = self.Gs.get_var("dlatent_avg")
            seed = np.asarray(seed)
            rnd = np.random.RandomState(seed)

            src_latents = rnd.randn(1, self.Gs.input_shape[1])
            all_w = self.Gs.components.mapping.run(src_latents, None)
            src_dlatents = w_avg + (all_w - w_avg) * truncation_psi
            src_dlatents = src_dlatents.reshape((1, 18, 512))

            self.generator.set_dlatents(src_dlatents)
            img_array = self.generator.generate_images()[0]
            self.generator.reset_dlatents()

            if return_latent:
                return img_array, src_dlatents
            else:
                return img_array
