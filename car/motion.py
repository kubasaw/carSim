"""Car motion class
   ================
   This part of the module contains the vehicle motion simulator class.
"""

import numpy as np
from scipy.integrate import solve_ivp

STATESIZE = 3


class constants:
    """Helper class holding problem specific constants
    """
    def __init__(self):
        self.g = 9.80665  # m/s^2
        self.rho = 1.225  # kg/m^3
        self.S = 1.008  # m^2
        self.cx = 0.32  # -
        self.m = 192  # kg
        self.f = [0.000168, 0.00133]  # -
        self.p = [233.1, -18.15, 1.039]  # N,N/speed,N/speed^2
        self.r = [0.0458, 0.0198, 0.00074]  # mL/s,mL/s/speed,mL/s/speed^2


class motion:
    """Car motion class
    """

    def __init__(self):

        # Simulation initial values
        self.state = np.zeros(STATESIZE)
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
            Simulator timestep for actual and future simulation steps, by default None.
            If not specified, default or previous specified value is used

        Raises
        ------
        ValueError
            If *dt* is not greater than 0
        """

        def carDynamics(t, x, throttle):
            """Helper function computing derivative of actual car state. Used for ODE solving
            
            Parameters
            ----------
            t : float
                Simulation time
            x : numpy.array
                Actual car state
            throttle : float (0-1)
                Throttle position

            Returns
            -------
            xdot : numpy.array
                Actual car state derivative
            """
            const = constants()
            xdot = np.zeros(STATESIZE)

            # car specific dynamics
            xdot[0] = x[1]
            xdot[1] = (const.p[2]*throttle*throttle/const.m-const.rho*const.S*const.cx/2/const.m)*x[1]*x[1] + \
                (const.p[1]*throttle*throttle/const.m-const.g*const.f[1]) * x[1] + \
                const.p[0]*throttle*throttle/const.m+const.g * \
                const.f[0]  # - const.g*np.sin(alpha(x[0]))
            xdot[2] = (const.r[2]*x[1]*x[1]+const.r[1]
                       * x[1]+const.r[0])*throttle

            return xdot

        if dt is not None:
            try:
                self.setTimestep(dt)
            except:
                raise ValueError("Timestep value have to be greater than 0")

        t0 = self.time
        tf = self.time+self.timestep

        self.state = solve_ivp(lambda t, x: carDynamics(t, x, self.throttle), (t0, tf),
                               self.state, t_eval=[tf])['y'].flatten()
        self.time = tf

        return self.state
