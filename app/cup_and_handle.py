import numpy as np
from numpy.core.multiarray import ndarray
from scipy.signal import savgol_filter
import config


def smooth_data(prices, window_length=7, polyorder=3) -> ndarray:
    """
    Smooths the price data using Savitzky-Golay filter to reduce noise.
    
    Args:
        prices (ndarray): Array of price data points
        window_length (int, optional): The length of the filter window. Defaults to 7.
        polyorder (int, optional): The order of the polynomial. Defaults to 3.
    
    Returns:
        ndarray: Smoothed price data
    """
    return savgol_filter(prices, window_length, polyorder)


def check_cup_and_handle_pattern(prices_list) -> bool:
    """
    Analyzes price data to detect a cup and handle pattern.
    
    Args:
        prices_list (list): List of historical price data points
    
    Returns:
        bool: True if a cup and handle pattern is detected, False otherwise
    """
    if len(prices_list) < config.MINIMUM_DATA_POINTS:
        return False

    print(prices_list)

    # Smooth the data if we have enough samples
    if len(prices_list) >= 20:
        prices = smooth_data(np.array(prices_list))
    else:
        prices = prices_list

    print(prices)

    # Base case - if we want to check the first sample as well
    prices = [0] + prices

    # Find pattern points from the end
    n = len(prices) - 1
    handle_peak_idx = None
    cup_bottom_idx = None
    cup_peak_idx = None

    # Find handle peak (first peak from the end)
    while n > 0:
        if prices[n] > prices[n - 1]:
            handle_peak_idx = n
            n -= 1
            break
        n -= 1

    # Find cup bottom (lowest point before handle peak)
    while n > 0:
        if prices[n] < prices[n - 1]:
            cup_bottom_idx = n
            n -= 1
            break
        n -= 1

    # Find cup peak (highest point before cup bottom)
    while n > 0:
        if prices[n] > prices[n - 1] or prices[n] >= prices[handle_peak_idx]:
            cup_peak_idx = n
            break
        n -= 1

    if not all([handle_peak_idx, cup_bottom_idx, cup_peak_idx]):
        return False

    # check if the points make the cup and handle pattern
    return cup_and_handle_criteria(prices, handle_peak_idx, cup_bottom_idx, cup_peak_idx)


def cup_and_handle_criteria(prices, handle_peak_idx, cup_bottom_idx, cup_peak_idx) -> bool:
    """
    Evaluates if the identified points form a valid cup and handle pattern.
    
    Args:
        prices (list): List of price data points
        handle_peak_idx (int): Index of the handle peak in the prices list
        cup_bottom_idx (int): Index of the cup bottom in the prices list
        cup_peak_idx (int): Index of the cup peak in the prices list
    
    Returns:
        bool: True if the pattern meets all criteria, False otherwise
    """
    # Initializing endpoints
    handle_height = prices[handle_peak_idx]
    cup_bottom = prices[cup_bottom_idx]
    cup_peak = prices[cup_peak_idx]
    last_sample_idx = len(prices) - 1
    last_sample = prices[-1]

    # -----------Pattern criteria------------
    # Cup peak and handle peak should be at similar levels (within 10%)
    cup_peak_and_handle_criteria = abs(handle_height - cup_peak) <= 0.1 * cup_peak

    # Cup bottom should be significantly lower (10-50% below peaks)
    cup_bottom_criteria = (min(handle_height, cup_peak) * 0.9 >= cup_bottom >= min(handle_height, cup_peak) * 0.5)

    # U-shape criteria: cup_bottom should be roughly centered between the two peaks
    left_width = cup_bottom_idx - cup_peak_idx
    right_width = handle_peak_idx - cup_bottom_idx
    max_ratio = max(2, (len(prices) * 0.1))
    u_shape_criteria = (1 / max_ratio) <= (left_width / right_width) <= max_ratio  # allows for some asymmetry

    # Handle should be shorter than the cup
    short_handle_vs_cup = (last_sample_idx - handle_peak_idx) < (handle_peak_idx - cup_peak_idx)

    # The last sample should not drop below cup bottom
    min_point_criteria = last_sample > cup_bottom

    criteria = [cup_peak_and_handle_criteria, cup_bottom_criteria, min_point_criteria, u_shape_criteria,
                short_handle_vs_cup]

    return all(criteria)
