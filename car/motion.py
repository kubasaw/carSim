"""Car motion class
   ================
   This part of the module contains the vehicle motion simulator class.
"""

import numpy as np
from scipy.integrate import solve_ivp


class motion:
    """Car motion class
    """

    def __init__(self):

        # Simulation initial values
        self.state = np.zeros(3)
        self.time = 0
        self.throttle = 0

        # Simulation control
        self.timestep = 0.1

    def getSimTime(self):
        """Returns actual simulation time

        Returns
        -------
        float
            Actual simulation time in seconds
        """
        return self.time

    def getSimDistance(self):
        """Returns actual vehicle distance covered

        Returns
        -------
        float
            Actual distance in meters
        """
        return self.state[0]

    def getSimSpeed(self):
        """Returns actual vehicle speed

        Returns
        -------
        float
            Actual vehicle speed in meters per second
        """
        return self.state[1]

    def setThrottle(self, throttle):
        """Set actual throttle value for next simulation time steps

        Parameters
        ----------
        throttle : float
            Normalized [0-1] throttle value for next simulation timesteps

        Raises
        ------
        ValueError
            If *throttle* is not number or outside unit interval
        """
        try:
            temp = float(throttle)
            if (temp < 0 or temp > 1):
                raise ValueError
        except:
            raise ValueError(
                "Throttle value have to be choosen from unit interval [0-1]")
        self.throttle = temp

    def setTimestep(self, dt):
        """Sets simulator timestep

        Parameters
        ----------
        dt : float
            Timestep for simulator

        Raises
        ------
        ValueError
            If *dt* is not greater than 0
        """
        try:
            temp = float(dt)
            if (temp <= 0):
                raise ValueError
            self.timestep = temp
        except:
            raise ValueError("Timestep value have to be greater than 0")

    def makeStep(self, dt=None):
        """Perform a step of simulation

        Parameters
        ----------
        dt : float, optional
            Simulator timestep for actual and future simulation steps , by default None.
            If not specified, default or previous specified value is used

        Raises
        ------
        ValueError
            If *dt* is not greater than 0
        """
        def dy_dx(y, x):
            return np.cos(y)

        if dt is not None:
            try:
                self.setTimestep(dt)
            except:
                raise ValueError("Timestep value have to be greater than 0")

        t0 = self.time
        tf = self.time+self.timestep

        self.state = solve_ivp(dy_dx, (t0, tf), self.state, t_eval=[tf])['y']
        self.time = tf

        return self.state
