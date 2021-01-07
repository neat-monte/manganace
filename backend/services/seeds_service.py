from random import randint, sample
from pathlib import Path
from typing import List


class SeedsService:
    SEEDS_DATA = Path.cwd() / "_seeds_data"
    GOOD_SEEDS_MALE = SEEDS_DATA / "good_seeds_males.txt"
    GOOD_SEEDS_FEMALE = SEEDS_DATA / "good_seeds_females.txt"

    def get_seeds(self, amount: int, overlap: int, equalize_gender: bool) -> List[int]:
        if equalize_gender:
            male_amount = int(amount / 2)
            male_overlap = int(overlap / 2)
        else:
            male_amount = randint(0, amount)
            male_overlap = randint(0, overlap)
        male = self.pick_seeds(male_amount, male_overlap, self.GOOD_SEEDS_MALE)
        female = self.pick_seeds(amount - male_amount, overlap - male_overlap, self.GOOD_SEEDS_FEMALE)
        return male + female

    @staticmethod
    def pick_seeds(amount: int, overlap: int, filename: Path) -> List[int]:
        with open(filename, "r") as file:
            all_seeds = list(map(int, file.read().split(",")))
            seeds = all_seeds[:overlap]
            seeds += sample(all_seeds[overlap:], k=amount - overlap)
            return seeds
