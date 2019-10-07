import car
import numpy as np
import matplotlib.pyplot as plt

paks = car.motion()
data=np.zeros((1,4))


paks.setThrottle(1)
for i in range(20):
    row=np.append(paks.makeStep(),paks.getSimTime())
    data=np.vstack((data,row))
paks.setThrottle(0)
for i in range(200):
    row=np.append(paks.makeStep(),paks.getSimTime())
    data=np.vstack((data,row))

time=data[:,3]
position=data[:,0]
speed=data[:,1]
fuel=data[:,2]

fig,axs=plt.subplots(nrows=3,ncols=1)
axs[0].plot(time,car.util.mpsToKmph(speed))
axs[1].plot(time,position)
axs[2].plot(time,fuel)

fig.tight_layout()
plt.show()
    