"""Utility functions for dataset operations."""

import datetime
import random
from typing import Any, Iterable

from src.dataset.models.employee import Generation


# Set a fixed seed for reproducibility
random.seed(1993)


def get_birth_date(generation: Generation) -> datetime.date:
    """Generate a realistic birth date for the specified generational cohort.

    Creates a random birth date within the standard year ranges for each
    generation, ensuring demographic accuracy in synthetic data generation.
    Uses a fixed random seed for reproducible results.

    Args:
        generation (Generation): The target generational cohort

    Returns:
        datetime.date: A randomly generated birth date within the appropriate
                      year range for the specified generation

    Raises:
        ValueError: If an invalid or unrecognized generation is provided

    Note:
        Generation year ranges:
        - Baby Boomer: 1946-1964
        - Generation X: 1965-1980
        - Millennial: 1981-1996
        - Generation Z: 1997-2012
    """
    if generation == Generation.BABY_BOOMER:
        start_year, end_year = 1946, 1964
    elif generation == Generation.GEN_X:
        start_year, end_year = 1965, 1980
    elif generation == Generation.MILLENNIAL:
        start_year, end_year = 1981, 1996
    elif generation == Generation.GEN_Z:
        start_year, end_year = 1997, 2012
    else:
        raise ValueError(f'Invalid generation: {generation}')

    # Generate a random birth date within the range
    birth_date = datetime.date(
        year=random.randint(start_year, end_year),  # nosec B311
        month=random.randint(1, 12),  # nosec B311
        day=random.randint(1, 28),  # nosec B311
    )

    return birth_date


def weighted_random_choice(choices: dict[Any, float]) -> Any:
    """Select an item from a weighted distribution using random sampling.

    Implements weighted random selection where each choice has a probability
    proportional to its weight. Uses cumulative distribution for efficient
    selection, ensuring proper statistical distribution in synthetic data.

    Args:
        choices (dict[Any, float]): Dictionary mapping items to their weights.
                                  Weights should be positive numbers and
                                  don't need to sum to 1.0

    Returns:
        Any: The randomly selected item based on weighted probabilities

    Example:
        >>> choices = {'A': 0.7, 'B': 0.2, 'C': 0.1}
        >>> result = weighted_random_choice(choices)
        >>> # 'A' has 70% chance, 'B' has 20% chance, 'C' has 10% chance

    Note:
        Uses a fixed random seed (1993) for reproducible results across runs.
        If weights don't sum exactly due to floating-point precision,
        returns the last choice as fallback.
    """
    total = sum(choices.values())
    r = random.uniform(0, total)  # nosec B311
    for item, weight in choices.items():
        if r < weight:
            return item
        r -= weight
    return list(choices.keys())[-1]  # Fallback


def batch_iterator(dataset: list[Any], batch_size: int = 20) -> Iterable[list[Any]]:
    """Yield successive batches from the dataset.

    Args:
        dataset (list[Any]): The complete dataset to be divided into batches.
        batch_size (int, optional): The number of items per batch.
    """
    for i in range(0, len(dataset), batch_size):
        yield dataset[i : i + batch_size]
