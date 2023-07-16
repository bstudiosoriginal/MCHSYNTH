class Measurement(object):

    def __init__(self, unit):
        """
        Measurement class object for describing physical quantity amounts
        ie.
        displacement, time, velocity and all.
        """
        self._unit = unit

    def get_unit(self):
        """
        Function to get measured unit
        """
        return self._unit

    def _set_unit(self, unit):
        """
        Function to set a unit to a measurement
        """
        self._unit = unit