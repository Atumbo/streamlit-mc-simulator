import numpy as np


class ProcessStep:
    """
    Represents a single step in a process

    Attributes:
        name (str): Name of the process.
        next (ProcessStep or None): Next step in the process.

    Args:
        name (str): Name of the process
    """

    def __init__(self, name: str):
        assert isinstance(name, str), f"Name must be a string, but got {type(name)}"

        self.name = name
        self.next = None


class UniformStep(ProcessStep):
    """
    Represents a process step with a uniform distribution.

    Attributes:
        low (float): Lower bound of the distribution.
        high (float): Upper bound of the distribution.

    Inheritance:
        ProcessStep: Base class.

    Args:
        name (str): Name of the step,
        low (float): Lower bound of the distribution.
        high (float): Upper bound of the distribution.

    """

    def __init__(self, name: str, low: float, high: float):
        super().__init__(name)

        assert isinstance(
            low, (int, float)
        ), f"Lower bound must be a number, but got {type(low)}"
        assert isinstance(
            high, (int, float)
        ), f"Higher bound must be a number, but got {type(high)}"
        assert low <= high, "Lower bound must be  less than or equal to upper bound"

        self.low = low
        self.high = high

    def simulate(self, n_simulations: int) -> np.ndarray:
        """
        Draws n samples from a uniform distribution.

        Args:
            n_simulations (int): number of samples to draw.

        Returns:
            samples (np.ndarray): An array of drawn samples.

        """
        return np.random.uniform(low=self.low, high=self.high, size=n_simulations)


class NormalStep(ProcessStep):
    """
    Represents a process step with a normal distribution.

    Attributes:
        mean (type): Mean values of the distribution.
        stdev (type): Standard deviation of the distribution.

    Inheritance:
        ProcessStep: Base class

    Args:
        name (str): Name of the process step.
        mean (float): Mean valuesof the distribution.
        stdev (float): Standard deviation of the distribution.

    """

    def __init__(self, name: str, mean: float, stdev: float):
        super().__init__(name)

        assert isinstance(
            mean, (int, float)
        ), f"Mean must be a number, but got {type(mean)}"
        assert isinstance(
            stdev, (int, float)
        ), f"stdev must be a number, but got {type(stdev)}"
        assert mean >= 0, f"Mean must be a non-negative number, but got {mean}"
        assert stdev >= 0, f"Stdev must be a non-negative number, but got {stdev}"

        self.mean = mean
        self.stdev = stdev

    def simulate(self, n_simulations: int) -> np.ndarray:
        """
        Draws n samples from a normal distribution.

        Args:
            n_simulations (int): number of samples to draw.

        Returns:
            samples (np.ndarray): An array of drawn samples.

        """
        return np.random.normal(loc=self.mean, scale=self.stdev, size=n_simulations)


class ExponentialStep(ProcessStep):
    """
    Represents a process step with a exponential distribution.

    Attributes:
        rate (type): rate (lambda) of the distribution

    Inheritance:
        ProcessStep: Base class

    Args:
        name (str): Name of the process step.
        rate (float): Rate (lambda) of the exponential distribution. Must be a positive number.

    """

    def __init__(self, name: str, rate: float):
        super().__init__(name)
        assert isinstance(
            rate, (float, int)
        ), f"Rate must be a number, but got {type(rate)}"
        assert rate > 0, f"Rate must be a positive number, but got {rate}"

        self.rate = rate

    def simulate(self, n_simulations: int) -> np.ndarray:
        """
        Draws n samples from a exponential distribution.

        Args:
            n_simulations (int): number of samples to draw.

        Returns:
            samples (np.ndarray): An array of drawn samples.
        """
        return np.random.exponential(1 / self.rate, size=n_simulations)