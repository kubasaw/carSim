"""Car motion class
   ================
   This part of the module contains the vehicle motion simulator class.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d


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


class track:
    """Helper class for local track slope estimation
    """

    def __init__(self):
        self.__verticalProfile = [[0, 9.529],
                                  [50, 9.870],
                                  [100, 10.04],
                                  [150, 10.22],
                                  [155, 10.182],
                                  [200, 9.471],
                                  [250, 8.576],
                                  [255, 8.476],
                                  [280, 7.885],
                                  [300, 7.392],
                                  [315, 7.118],
                                  [345, 6.675],
                                  [350, 6.650],
                                  [375, 6.300],
                                  [400, 6.070],
                                  [415, 5.878],
                                  [450, 5.707],
                                  [455, 5.722],
                                  [500, 5.670],
                                  [540, 5.572],
                                  [550, 5.570],
                                  [590, 5.627],
                                  [600, 5.626],
                                  [625, 5.651],
                                  [650, 5.658],
                                  [655, 5.603],
                                  [680, 5.953],
                                  [700, 6.130],
                                  [750, 6.070],
                                  [785, 6.026],
                                  [800, 5.818],
                                  [813, 5.755],
                                  [836, 5.577],
                                  [850, 5.509],
                                  [870, 5.494],
                                  [900, 5.282],
                                  [930, 5.235],
                                  [950, 5.030],
                                  [975, 4.883],
                                  [1000, 4.786],
                                  [1025, 4.647],
                                  [1050, 4.482],
                                  [1100, 4.276],
                                  [1150, 4.038],
                                  [1165, 3.946],
                                  [1200, 3.697],
                                  [1220, 3.539],
                                  [1250, 3.369],
                                  [1270, 3.761],
                                  [1300, 4.975],
                                  [1335, 6.691],
                                  [1350, 7.451],
                                  [1395, 9.695],
                                  [1400, 9.945],
                                  [1450, 12.069],
                                  [1455, 12.17],
                                  [1500, 11.903],
                                  [1505, 11.739],
                                  [1550, 9.721],
                                  [1553, 9.621],
                                  [1580, 9.515],
                                  [1600, 9.508],
                                  [1630, 9.438],
                                  [1650, 9.466],
                                  [1659, 9.529]]
        self.__trackLength = max(pos[0] for pos in self.__verticalProfile)
        self.__interpolantFunction = interp1d([pos[0] for pos in self.__verticalProfile], [
                                              pos[1] for pos in self.__verticalProfile], kind='cubic', bounds_error=True, copy=False, assume_sorted=True)

    def getSlopeSine(self, point, positionInterval=2):
        """Compute track slope sine

        Parameters
        ----------
        point : float
            Position coordinate for computing track slope sine
        positionInterval : float, optional
            Slope finite difference interval in meters, by default 2

        Returns
        -------
        slopeSine : float
            Track slope sine at 'point'
        """

        halfInterval = positionInterval/2
        return (np.diff(self.__interpolantFunction(np.remainder([point-halfInterval, point+halfInterval], self.__trackLength)), axis=0)/positionInterval).flatten()

    def getSlope(self, point, positionInterval=2):
        """Compute track slope

        Parameters
        ----------
        point : float
            Position coordinate for computing track slope
        positionInterval : float, optional
            Slope finite difference interval in meters, by default 2

        Returns
        -------
        slope : float
            Track slope at 'point' in radians
        """
        return np.arcsin(self.getSlopeSine(point, positionInterval=positionInterval))

    def getHeight(self, point):
        """Returns interpolated track elevation

        Parameters
        ----------
        point : float
            Position coordinate for computing track elevation interpolation

        Returns
        -------
        height : float
            Track elevation at 'point' in meters above sea level
        """
        return self.__interpolantFunction(np.remainder(point, self.__trackLength))

    def getTrackProfile(self):
        """Returns vertical road profile

        Returns
        -------

        profile : array of 2-element tuples
            Road profile points coordinates
        """
        return self.__verticalProfile

class motion:
    """Car motion class
    """

    def __init__(self, initialCondition=[0., 0., 0.]):

        # Simulation initial values
        self.__state = np.array(initialCondition)
        self.__time = 0
        self.__throttle = 0
        self.__constants = constants()
        self.track = track()

        # Simulation control
        self.__timestep = 0.1

    def getSimTime(self):
        """Returns actual simulation time

        Returns
        -------
        float
            Actual simulation time in seconds
        """
        return self.__time

    def getSimDistance(self):
        """Returns actual vehicle distance covered

        Returns
        -------
        float
            Actual distance in meters
        """
        return self.__state[0]

    def getSimSpeed(self):
        """Returns actual vehicle speed

        Returns
        -------
        float
            Actual vehicle speed in meters per second
        """
        return self.__state[1]

    def getSimFuel(self):
        """Returns consumed fuel

        Returns
        -------
        float
            Actual consumed fuel in mililiters
        """
        return self.__state[2]

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
                raise ValueError()
        except:
            raise ValueError(
                "Throttle value have to be choosen from unit interval [0-1]")
        self.__throttle = temp

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
        temp = float(dt)
        if (temp <= 0):
            raise ValueError("Timestep value have to be greater than 0")
        self.__timestep = temp

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
                throttle position

            Returns
            -------
            xdot : numpy.array
                Actual car state derivative
            """
            xdot = np.copy(self.__state)

            # car specific dynamics
            xdot[0] = x[1]
            xdot[1] = (self.__constants.p[2]*throttle*throttle/self.__constants.m-self.__constants.rho*self.__constants.S*self.__constants.cx/2/self.__constants.m)*x[1]*x[1] + \
                (self.__constants.p[1]*throttle*throttle/self.__constants.m-self.__constants.g*self.__constants.f[1]) * x[1] + \
                self.__constants.p[0]*throttle*throttle/self.__constants.m-self.__constants.g * \
                self.__constants.f[0] - self.__constants.g * \
                self.track.getSlopeSine(x[0])
            xdot[2] = (self.__constants.r[2]*x[1]*x[1]+self.__constants.r[1]
                       * x[1]+self.__constants.r[0])*throttle

            return xdot

        if dt is not None:
            self.setTimestep(dt)

        t0 = self.__time
        tf = self.__time+self.__timestep

        self.__state = solve_ivp(lambda t, x: carDynamics(t, x, self.__throttle), (t0, tf),
                                 self.__state, t_eval=[tf])['y'].flatten()
        self.__time = tf

        return self.__state
