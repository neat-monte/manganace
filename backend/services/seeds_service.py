from random import randint, sample
from pathlib import Path
from typing import List, Tuple


class SeedsService:
    SEEDS_DATA = Path.cwd() / "_seeds_data"
    GOOD_SEEDS_MALE = SEEDS_DATA / "good_seeds_males.txt"
    GOOD_SEEDS_FEMALE = SEEDS_DATA / "good_seeds_females.txt"

    def get_seeds(self, amount: int, overlap: int, equalize_gender: bool) -> List[int]:
        male_amount, male_overlap = self.get_male_amount_by_settings(amount, overlap, equalize_gender)
        male = self.pick_seeds(male_amount, male_overlap, self.GOOD_SEEDS_MALE)
        female = self.pick_seeds(amount - male_amount, overlap - male_overlap, self.GOOD_SEEDS_FEMALE)
        return male + female

    def complete_the_list(self, seeds: List[int], amount: int, overlap: int, equalize_gender: bool) -> List[int]:
        missing_male_seeds, missing_female_seeds = [], []
        male_seeds, female_seeds = self.split_by_gender(seeds, self.GOOD_SEEDS_MALE)
        if equalize_gender:
            male_amount, male_overlap = self.get_male_amount_by_settings(amount, overlap, equalize_gender)
            if len(male_seeds) < male_amount:
                amount = male_amount - len(male_seeds)
                missing_male_seeds = self.random_seeds(amount, male_overlap, self.GOOD_SEEDS_MALE, male_seeds)
            elif len(female_seeds) < amount - male_amount:
                amount = (amount - male_amount) - len(female_seeds)
                missing_female_seeds = self.random_seeds(amount, overlap - male_overlap, self.GOOD_SEEDS_FEMALE,
                                                         female_seeds)
            return missing_male_seeds + missing_female_seeds
        missing_amount = amount - len(seeds)
        missing_male_amount = randint(0, missing_amount)
        missing_male_seeds = self.random_seeds(missing_male_amount, 0, self.GOOD_SEEDS_MALE, male_seeds)
        missing_female_seeds = self.random_seeds(missing_amount - missing_male_amount, 0, self.GOOD_SEEDS_FEMALE,
                                                 female_seeds)
        return missing_male_seeds + missing_female_seeds

    @staticmethod
    def get_male_amount_by_settings(amount: int, overlap: int, equalize_gender: bool):
        if equalize_gender:
            male_amount = int(amount / 2)
            male_overlap = int(overlap / 2)
        else:
            male_amount = randint(0, amount)
            male_overlap = randint(0, overlap)
        return male_amount, male_overlap

    @staticmethod
    def split_by_gender(seeds: List[int], male_filename: Path) -> Tuple[List[int], List[int]]:
        with open(male_filename, "r") as m:
            male_seeds = list(map(int, m.read().split(",")))
            male = [seed for seed in seeds if seed in male_seeds]
            female = [seed for seed in seeds if seed not in male]
            return male, female

    @staticmethod
    def pick_seeds(amount: int, overlap: int, filename: Path) -> List[int]:
        with open(filename, "r") as file:
            all_seeds = list(map(int, file.read().split(",")))
            seeds = all_seeds[:overlap]
            seeds += sample(all_seeds[overlap:], k=amount - overlap)
            return seeds

    @staticmethod
    def random_seeds(amount: int, skip: int, filename: Path, exclude: List[int] = None) -> List[int]:
        with open(filename, "r") as file:
            all_seeds = list(map(int, file.read().split(",")))
            if exclude:
                seeds = sample(all_seeds[skip:], k=amount)
                while set(seeds).intersection(exclude):
                    seeds = sample(all_seeds[skip:], k=amount)
                return seeds
            else:
                return sample(all_seeds[skip:], k=amount)
