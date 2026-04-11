#!/usr/bin/env python
import random

def sample_normal(mu, sigma):
    """
    Normal distribution (Gaussian Distribution)
    """
    return random.gauss(mu, sigma)

def sample_truncated_normal(mu, sigma ,lower, upper, max_iter = 100):
    """
    Sample from a normal distribution, rejecting samples outside
    [lower, upper]. Falls back to clipped mu if no valid sample
    is obtained within max_iter attempts.
    """
    for _ in range (max_iter):
        x = sample_normal(mu, sigma)
        if lower <= x <= upper:
            return x
    return max(lower, min(upper, mu))

def sample_capped_normal(mu, sigma, lower, upper):
    """
    Suitable for simulating markets with price limit systems,
    such as the A-share market.
    """
    x = sample_normal(mu, sigma)
    return max(lower, min(upper, x))