from cmu_112_graphics import *

# Main Classes

class Satellite(object):
    def __init__(self, m, pos, v, a):
        self.pos = pos  # position as a vector
        self.v = v   # velocity as a vector
        self.a = a  # acceleration as a vector
        self.m = m  # mass - replace later with density and radius

class GravityWell(Satellite):
    def __init__(self, m, pos, v = [0, 0], a = [0, 0]):
        super().__init__(m, pos, v, a)

class SpaceTime(object):
    def __init__(self):
        self.G = 6.674 * 10**(-11)  # Gravitational constant
        self.t = 1  # timestep


    # calculating gravitational acceleration on "on" by "by" using a = Gm/r**2 in direction r^
    def a(self, on, by):
        r = (by.pos[0] - on.pos[0], by.pos[1] - on.pos[1])
        # debug: print(f"r = {r}")
        rsquared = r[0]**2 + r[1]**2
        Gm_by_rsq = (self.G * by.m)/rsquared
        a = (Gm_by_rsq * r[0]/(rsquared**0.5), Gm_by_rsq * r[1]/(rsquared**0.5))
        # debug: print(f"a = {a}")
        return a

    # calculating new position and velocity using acceleration
    def update(self, on, by):
        a = self.a(on, by)
        on.pos[0] += on.v[0] * self.t
        on.pos[1] += on.v[1] * self.t
        on.v[0] += a[0] * self.t
        on.v[1] += a[1] * self.t

# temp test code

def gravTest():
    print("gravTest")
    earthMass = 5.97 * 10**24
    earthRadius = 6400000
    spaceTime = SpaceTime()
    objMass = 1
    object = Satellite(objMass, [0, 100], [0, 0], [0, 0])
    earth = GravityWell(earthMass, [0, -earthRadius], [0, 0], [0, 0])

    while object.pos[1] >= 0 and object.pos[0] >= 0:
        spaceTime.update(object, earth)
        print(f"pos = {object.pos}")
        print(f"v = {object.v}")
        print()
        spaceTime.t += 1

# gravTest()

def orbitTest():
    print("orbitTest")
    earthMass = 5.97 * 10**24
    earthRadius = 6400000
    orbitalRadius = 10**7
    spaceTime = SpaceTime()
    objMass = 1
    orbitalVelocity = (spaceTime.G * earthMass/orbitalRadius)**0.5
    object = Satellite(objMass, [0, orbitalRadius], [orbitalVelocity, 0], [0, 0])
    earth = GravityWell(earthMass, [0, 0], [0, 0], [0, 0])

    while spaceTime.t < 100:
        spaceTime.update(object, earth)
        print(f"pos = {object.pos}")
        print(f"v = {object.v}")
        orbitalR = (object.pos[0]**2 + object.pos[1]**2)**0.5
        print(f"orbitalR = {orbitalR}")
        orbitalV = (object.v[0]**2 + object.v[1]**2)**0.5
        print(f"orbitalV = {orbitalV}")
        print()
        spaceTime.t += 1

# orbitTest()

# UI/UX
def appStarted(app):
    pass