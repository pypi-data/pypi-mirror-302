# File: tests/test_pyfcomb.py

import pytest
import numpy as np
import pandas as pd
from pyfcomb import RFrequency, r_get_combinations
from pyfcomb.reader import get_combinations


def test_rfrequency_creation():
    freq = RFrequency(1, 440.0, 0.5)
    assert freq.frequency_number == 1
    assert freq.frequency == 440.0
    assert freq.amplitude == 0.5


def test_r_get_combinations():
    frequencies = [
        RFrequency(1, 100.0, 1.0),
        RFrequency(2, 200.0, 0.5),
        RFrequency(3, 300.0, 0.3)
    ]
    combo_depth = 2
    accuracy = 0.01

    component_strings, independent_strings = r_get_combinations(frequencies, combo_depth, accuracy)

    assert isinstance(component_strings, list)
    assert isinstance(independent_strings, list)
    assert len(component_strings) + len(independent_strings) == len(frequencies)


def test_get_combinations():
    frequency_ids = [1, 2, 3]
    frequencies = [100.0, 200.0, 300.0]
    amplitudes = [1.0, 0.5, 0.3]
    combo_depth = 2
    accuracy = 0.01

    result = get_combinations(frequency_ids, frequencies, amplitudes, combo_depth, accuracy)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == len(frequency_ids)
    assert all(column in result.columns for column in
               ["Name", "ID", "Frequency", "Amplitude", "Solution", "Residual", "Independent", "Other_Solutions"])


def test_get_combinations_invalid_input():
    with pytest.raises(ValueError):
        get_combinations([1, 2], [100.0, 200.0, 300.0], [1.0, 0.5, 0.3])


def test_get_combinations_accuracy():
    frequency_ids = [1, 2, 3]
    frequencies = [100.0, 200.0, 300.0]
    amplitudes = [1.0, 0.5, 0.3]
    combo_depth = 2
    accuracy = 0.01

    result = get_combinations(frequency_ids, frequencies, amplitudes, combo_depth, accuracy)

    non_independent = result[~result['Independent']]
    assert all(non_independent['Residual'] <= accuracy)


def test_get_combinations_combo_depth():
    frequency_ids = [1, 2, 3, 4]
    frequencies = [100.0, 200.0, 300.0, 400.0]
    amplitudes = [1.0, 0.5, 0.3, 0.2]
    combo_depth = 2
    accuracy = 0.01

    result = get_combinations(frequency_ids, frequencies, amplitudes, combo_depth, accuracy)

    non_independent = result[~result['Independent']]
    for solution in non_independent['Solution']:
        # Subtract 1 from the count because the solution includes the target frequency
        assert solution.count('f') - 1 <= combo_depth

# Add more tests as needed for edge cases, error handling, etc.