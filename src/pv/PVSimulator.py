class PVSimulator:
    """
    This class represents a PhotoVoltaic simulator, it gets an energy reading and outputs a mock photovoltaic energy.
    The mock is represented by simply an efficiency value that we pass to it, multiplied by the input energy.
    """

    def __init__(self, efficiency):
        if efficiency > 1 or efficiency < 0:
            raise ValueError("The efficiency must be a value between 0 and 1: {}".format(efficiency))
        self.efficiency = efficiency

    def output(self, generated_value):
        produced_energy = generated_value * self.efficiency
        return produced_energy
