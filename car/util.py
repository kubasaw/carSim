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
    as *speed*
    Speed converted to km/h
        
    """
    return speed*3.6