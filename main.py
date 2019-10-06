import car

paks = car.motion()
paks.setThrottle(1)
for i in range(10):
    print(paks.makeStep())