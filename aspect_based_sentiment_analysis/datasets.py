from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable
from typing import Iterator
from typing import List

import numpy as np

from .data_types import Example


@dataclass
class TrainBatch:
    """ """


class Dataset(ABC):

    @abstractmethod
    def __iter__(self) -> Iterable[TrainBatch]:
        """ We use datasets in our custom routines, where is a simple for loop,
        therefore exclusively an iterable object is required. """

    @abstractmethod
    def preprocess_batch(self, batch_examples: List[Example]) -> TrainBatch:
        """ """


class InMemoryDataset(Dataset):
    examples: List
    batch_size: int

    def __iter__(self) -> Iterator[TrainBatch]:
        """ The method shuffles examples for next epoch, and returns the full
        batches in each iteration. """
        order = np.random.permutation(len(self.examples))
        batch_examples = []
        for index in order:
            example = self.examples[index]
            batch_examples.append(example)
            if len(batch_examples) == self.batch_size:
                batch = self.preprocess_batch(batch_examples)
                yield batch
                batch_examples = []

    @abstractmethod
    def preprocess_batch(self, batch_examples: List[Example]) -> TrainBatch:
        """ """


class StreamDataset(Dataset):
    batch_size: int

    def __iter__(self) -> Iterator[TrainBatch]:
        """ """
        examples = self.examples_generator()
        batch_examples = []
        for example in examples:
            batch_examples.append(example)
            if len(batch_examples) == self.batch_size:
                batch_input = self.preprocess_batch(batch_examples)
                yield batch_input
                batch_examples = []

    @abstractmethod
    def examples_generator(self) -> Iterable[Example]:
        """ """
