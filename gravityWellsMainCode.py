from cmu_112_graphics import *
import random

def appStarted(app):
    #temp code
    earthMass = 5.97 * 10**24
    earthRadius = 6400000
    orbitalRadius = 10**7
    universe = SpaceTime()
    objMass = 1
    orbitalVelocity = (universe.G * earthMass/orbitalRadius)**0.5

    app.positionScale = 10**(-5)   # scaling position (which uses realistic scaling) such that it fits on canvas

    # converting starting positions on canvas to 'real' scale for initial position arguments
    scaledcx = (app.width//2)/app.positionScale
    scaledcy = (app.height//2)/app.positionScale

    app.player = Player(objMass, [scaledcx, scaledcy-orbitalRadius], [orbitalVelocity, 0], [0, 0])
    app.planets = []
    app.gravityWell = GravityWell(earthMass, [scaledcx, scaledcy])
    app.timerDelay = 100
    app.universe = SpaceTime()

# Main Classes

# all objects on board (planets, player, gravity wells) are instances of class Satellite
class Satellite(object):
    def __init__(self, m, pos, v, a):
        self.pos = pos  # position as a vector
        self.v = v   # velocity as a vector
        self.a = a  # acceleration as a vector
        self.aPrev = a
        self.m = m  # mass 
        self.r = random.randint(5, 25)
        self.colour = 'cyan'

    def draw(self, app, canvas):
        scaledPos = [self.pos[0]*app.positionScale, self.pos[1]*app.positionScale]
        print(self.colour, scaledPos)
        x0, y0 = scaledPos[0]-self.r, scaledPos[1]-self.r
        x1, y1 = scaledPos[0]+self.r, scaledPos[1]+self.r
        canvas.create_oval(x0, y0, x1, y1, fill=self.colour)

class GravityWell(Satellite):
    def __init__(self, m, pos, v = [0, 0], a = [0, 0]):
        super().__init__(m, pos, v, a)
        self.r = random.randint(25, 100)
        self.colour = 'black'

class Player(Satellite):
    def __init__(self, m, pos, v, a):
        super().__init__(m, pos, v, a)
        self.r = 10
        self.colour = 'orange'

# class SpaceTime contains implementation of gravity
class SpaceTime(object):
    def __init__(self):
        self.G = 6.6743 * 10**(-11)  # Gravitational constant
        self.time = 0
        self.dt = 100  # timestep

    def updatePos(self, on):
        # updating position for vector components individually
        for i in range(2):
            on.pos[i] += on.v[i]*self.dt + 0.5*on.a[i]*(self.dt**2)

    # calculating gravitational acceleration on "on" by "by" using a = Gm/r**2 in direction r^
    def updateAcceleration(self, on, by):
        on.aPrev = on.a
        r = (by.pos[0] - on.pos[0], by.pos[1] - on.pos[1])
        # debug: print(f"r = {r}")
        rsquared = r[0]**2 + r[1]**2
        Gm_by_rsq = (self.G * by.m)/rsquared
        a = (Gm_by_rsq * r[0]/(rsquared**0.5), Gm_by_rsq * r[1]/(rsquared**0.5))
        # debug: print(f"a = {a}")
        on.a = a

    def updateVelocity(self, on):
        # updating velocity for vector components individually
            for i in range(2):
                on.v[i] += 0.5*(on.aPrev[i] + on.a[i])*self.dt

    def updateTime(self):
        self.time += self.dt

    # implements Verlet Integration (second order integrator method) to 
    # update position, velocity, and acceleration
    # Mathematical reference: 
    # https://www.physics.udel.edu/~bnikolic/teaching/phys660/numerical_ode/node5.html
    def updateAll(self, on, by):
        self.updatePos(on)
        self.updateAcceleration(on, by)
        self.updateVelocity(on)
        self.updateTime()

def timerFired(app):
    app.universe.updateAll(app.player, app.gravityWell)

def redrawAll(app, canvas):
    app.player.draw(app, canvas)
    for planet in app.planets:
        planet.draw(app, canvas)
    app.gravityWell.draw(app, canvas)

def playGravityWells():
    runApp(width = 600, height = 600)

playGravityWells()


# Tests

# def gravNumericTest():
#     print("gravTest")
#     earthMass = 5.97 * 10**24
#     earthRadius = 6400000
#     universe = SpaceTime()
#     objMass = 1
#     object = Satellite(objMass, [0, 100], [0, 0], [0, 0])
#     earth = GravityWell(earthMass, [0, -earthRadius], [0, 0], [0, 0])

#     while object.pos[1] >= 0 and object.pos[0] >= 0:
#         universe.updateAll(object, earth)
#         print(f"pos = {object.pos}")
#         print(f"v = {object.v}")
#         print()

# def orbitNumericTest():
#     print("orbitTest")
#     earthMass = 5.97 * 10**24
#     earthRadius = 6400000
#     orbitalRadius = 10**7
#     universe2 = SpaceTime()
#     objMass = 1
#     orbitalVelocity = (universe2.G * earthMass/orbitalRadius)**0.5
#     object = Satellite(objMass, [0, orbitalRadius], [orbitalVelocity, 0], [0, 0])
#     earth = GravityWell(earthMass, [0, 0], [0, 0], [0, 0])

#     while universe2.time < 100:
#         universe2.updateAll(object, earth)
#         print(f"pos = {object.pos}")
#         print(f"v = {object.v}")
#         orbitalR = (object.pos[0]**2 + object.pos[1]**2)**0.5
#         print(f"orbitalR = {orbitalR}")
#         orbitalV = (object.v[0]**2 + object.v[1]**2)**0.5
#         print(f"orbitalV = {orbitalV}")
#         print()

# gravNumericTest()
# orbitNumericTest()
