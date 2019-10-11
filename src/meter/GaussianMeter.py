import logging
from datetime import datetime

import numpy as np

logger = logging.getLogger(__name__)


class GaussianMeter:
    """
    Implementation of the meter class, this particular meter returns values based on the normal distribution.
    What we do is we generate a series between -1 and 1, with the resolution (step) that is calculated in function of how many mock readings we make.
    Then for every value of that array we calculate the normal value, scale and offset it and return it as a mock kilowatt reading.
    Attributes
    ----------

    :name str: Name of the object.
    :mu float: This represents the mean of the distribution. See `~numpy.random.normal`.
    :sigma float: This represents the standard deviation of the distribution. See `~numpy.random.normal`.
    :scale int: This represents the max number of kiloWatts our meter can produce. We multiply this for every element we get from the normal so that it scales.
    :offset int: Similar to scale, this value is used to shift the values of the distribution upwards, so we get values closer to real life.
    :rate int: The rate at which mock readings are available, in milliseconds.
    :n int: This represents the number mock readings we want.
    :values array: This array holds all generated values between -1 and 1.
    :read_at datetime: The last time the meter made a reading.
    """

    def __init__(self, name, mu, sigma, scale, offset, rate, n=2000):
        """

        :param name: Name of the object.
        :param mu: This represents the mean of the distribution. See `~numpy.random.normal`.
        :param sigma: This represents the standard deviation of the distribution. See `~numpy.random.normal`.
        :param scale: This represents the max number of kiloWatts our meter can produce. We multiply this for every element we get from the normal so that it scales.
        :param offset: Similar to scale, this value is used to shift the values of the distribution upwards, so we get values closer to real life.
        :param rate: The rate at which mock readings are available, in milliseconds.
        :param n: This represents the number mock readings we want.
        """
        self.name = name
        self.mu = mu
        self.sigma = sigma
        self.scale = scale
        self.offset = offset
        self.rate = rate
        self.n = n
        self.values = self.init_values()
        self.read_at = datetime.now()
        self.index = 0  # This index is to keep track of the current value that is being fed by the meter.
        logger.debug(self.values)

    def init_values(self):
        return np.arange(-1, 1, float(2 / self.n))

    def normal(self, x):
        """
        This functions represents the normal function, we use it to generate our mock reading, so that it resembles more a real life one.
        :param x:
        :return:
        """
        return (2. * np.pi * self.sigma ** 2.) ** -.5 * np.exp(-.5 * (x - self.mu) ** 2. / self.sigma ** 2.)

    def get_reading(self):
        """
        This method is invoked every time a reading is requested. If the meter it ready, it returns a reading, other wise None.
        :return:
        """
        reading_time = datetime.now()
        delta_datetime = reading_time - self.read_at
        delta_time = delta_datetime.seconds * 1000 + delta_datetime.microseconds / 1000
        if delta_time <= self.rate:
            logger.info("Meter not ready.")
            logger.debug("Delta : {}".format(delta_time))
            return None
        self.read_at = reading_time
        read_value = (self.normal(self.values[self.index]) * self.scale + self.offset)
        self.index = self.index + 1
        if self.index >= len(self.values):
            self.index = 0
        reading = {
            "measured_value": read_value,
            "time": reading_time.isoformat()
        }
        return reading
