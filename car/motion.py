"""Car motion class
   ================
   This part of the module contains the vehicle motion simulator class.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import json
import struct


class motionParam(object):
    def __init__(self, value):
        self.__value = value

    @property
    def val(self):
        return self.__value

    @property
    def export(self):
        return (self.__class__.__name__, self.val)


class track(motionParam):

    def __init__(self, trackProfile):
        super().__init__(trackProfile)
        self.__length = max(pos[0] for pos in self.val)
        self.__interpolant = interp1d([pos[0] for pos in self.val], [
            pos[1] for pos in self.val], kind='linear', bounds_error=True, copy=False, assume_sorted=False)

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
        return ((self.getHeight(point+halfInterval)-self.getHeight(point-halfInterval))/positionInterval)

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
        return self.__interpolant(np.remainder(point, self.__length))


class constants():
    """Helper class holding problem specific constants
    """

    def __init__(self):
        self.__constDict = dict()

    def get(self, param):
        return self.__constDict[param].val

    def ret(self, param):
        return self.__constDict[param]

    def toJSON(self, file=None):
        if file != None:
            return json.dump(self.__constDict, file, default=lambda x: x.export, indent=4)
        else:
            return json.dumps(self.__constDict, default=lambda x: x.export, indent=4)

    def fromJSON(self, js):
        if isinstance(js, str):
            data = json.loads(js)
        else:
            data = json.load(js)

        temp = dict()
        for key, [valClass, val] in data.items():
            temp[key] = globals()[valClass](val)

        self.__constDict = temp


class motion:
    """Car motion class
    """

    def __init__(self, initialCondition=[0., 0., 0.]):

        # Simulation initial values
        self.__state = np.array(initialCondition)
        self.__time = 0
        self.__throttle = 0
        self.__switchingPoints = {0: 0.0}
        self.param = constants()

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

    def getCanBytes(self):
        distance = int(abs(self.getSimDistance()))
        speed = int(abs(self.getSimSpeed()*360))

        return speed.to_bytes(2, 'little')+distance.to_bytes(2, 'little')

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

    def getThrottle(self):
        """Returns consumed fuel

        Returns
        -------
        float
            Actual consumed fuel in mililiters
        """
        return self.__throttle

    def setSwitchingPoint(self, tup):
        self.__switchingPoints[tup[1]] = tup[0]

    def getNextSwitchingPoint(self):
        for i in sorted(self.__switchingPoints.keys()):
            if self.__switchingPoints[i] > self.__time:
                return self.__switchingPoints[i]

        return float("inf")

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

        if (self.__throttle <= 0 and temp >= 0):
            self.__state[2] += self.param.get("r0")

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
            xdot[1] = (self.param.get("p")[2]*throttle*throttle/self.param.get("m")-self.param.get("rho")*self.param.get("S")*self.param.get("cx")/2/self.param.get("m"))*x[1]*x[1] + \
                (self.param.get("p")[1]*throttle*throttle/self.param.get("m")-self.param.get("g")*self.param.get("f")[1]) * x[1] + \
                self.param.get("p")[0]*throttle*throttle/self.param.get("m")-self.param.get("g") * \
                self.param.get("f")[0] - self.param.get("g") * \
                self.param.ret("track").getSlopeSine(x[0])
            xdot[2] = (self.param.get("r")[2]*x[1]*x[1]+self.param.get("r")[1]
                       * x[1]+self.param.get("r")[0])*throttle

            return xdot

        if dt is not None:
            self.setTimestep(dt)

        t0 = self.__time
        tf = self.__time+self.__timestep

        __nextSwitch = self.getNextSwitchingPoint()

        if(t0 < __nextSwitch and tf > __nextSwitch):
            self.__state = solve_ivp(lambda t, x: carDynamics(t, x, self.__throttle), (t0, __nextSwitch),
                                     self.__state, t_eval=[__nextSwitch])['y'].flatten()
            if (self.__throttle <= 0):
                self.setThrottle(1)
            else:
                self.setThrottle(0)

            self.__state = solve_ivp(lambda t, x: carDynamics(t, x, self.__throttle), (__nextSwitch, tf),
                                     self.__state, t_eval=[tf])['y'].flatten()

        else:
            self.__state = solve_ivp(lambda t, x: carDynamics(t, x, self.__throttle), (t0, tf),
                                     self.__state, t_eval=[tf])['y'].flatten()
            if(__nextSwitch == tf):
                if (self.__throttle <= 0):
                    self.setThrottle(1)
                else:
                    self.setThrottle(0)

        self.__time = tf

        return self.__state
