import dataclasses
import random
from typing import Protocol, Iterable, TypeVar

__all__ = ["BlendingType", "BlendingConfig", "blend"]

T = TypeVar('T')


class BlendingAlgorithm(Protocol):
    def blend(self, *feeds: Iterable[T]) -> Iterable[T]:
        ...


class WeightedTdi(BlendingAlgorithm):
    """Team-draft interleaving algorithm implementation with weights"""
    def __init__(self, weights: list[float], random_seed=None):
        self.weights = weights
        assert len(self.weights) >= 1, "At least one weight must be provided"
        # if weight is 0, then feed is not active
        self.active_feeds = [True if self.weights[idx] > 0 else False for idx in range(len(self.weights))]
        random.seed(random_seed)

    def _choose_feed_index(self, available_feeds_idx: list[int]) -> int:

        # Probabilities are normalized to sum to 1
        probabilities = [self.weights[feed_idx] for feed_idx in available_feeds_idx]
        total_weight = sum(probabilities)
        probabilities = [weight / total_weight for weight in probabilities]
        chosen_index = random.choices(available_feeds_idx, probabilities)[0]

        return chosen_index

    def _get_available_feeds_indices(self, feeds) -> list[int]:
        """Get indexes of feeds that are still active, i.e. not all items have been consumed from those"""
        return [idx for idx, is_active in (zip(range(len(feeds)), self.active_feeds)) if is_active]

    def blend(self, *feeds):
        feed_iters = [iter(feed) for feed in feeds]

        while available_feeds_idx := self._get_available_feeds_indices(feeds):
            chosen_index = self._choose_feed_index(available_feeds_idx)

            try:
                yield next(feed_iters[chosen_index])
            except StopIteration:
                self.active_feeds[chosen_index] = False


@dataclasses.dataclass
class BlendingType:
    W_TDI: BlendingAlgorithm = WeightedTdi


@dataclasses.dataclass
class BlendingConfig:
    params: dict
    algorithm: BlendingAlgorithm = BlendingType.W_TDI


def blend(*feeds: Iterable[T], config: BlendingConfig) -> Iterable[T]:
    """Blend two or more iterables into one"""
    blending_algorithm = config.algorithm(**config.params)
    yield from blending_algorithm.blend(*feeds)
