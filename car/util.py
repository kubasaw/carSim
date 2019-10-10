"""Car simulation utilities module
   ===============================
  
"""


def mpsToKmph(speed):
    """Meter per second to kilometer per hour unit converter

    Parameters
    ----------
    speed : multiplicable (float, numpy.array etc.)
        Speed in m/s

    Returns
    -------
    convertedSpeed : as *speed*
        Speed converted to km/h
    """
    convertedSpeed = speed*3.6
    return convertedSpeed
