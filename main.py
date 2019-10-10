import car
import numpy as np
import matplotlib.pyplot as plt

paks = car.motion()
trk = car.track()
data = np.zeros((1, 4))


paks.setThrottle(1)
for i in range(100):
    row = np.append(paks.makeStep(), paks.getSimTime())
    data = np.vstack((data, row))
paks.setThrottle(0)
for i in range(500):
    row = np.append(paks.makeStep(), paks.getSimTime())
    data = np.vstack((data, row))

time = data[:, 3]
position = data[:, 0]
speed = data[:, 1]
fuel = data[:, 2]

fig, axs = plt.subplots(nrows=4, ncols=1)
axs[0].plot(time, car.util.mpsToKmph(speed))
axs[1].plot(time, position)
axs[2].plot(time, fuel)
axs[3].plot(time, trk.getHeight(position))


fig.tight_layout()
plt.show()
