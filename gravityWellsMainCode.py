from cmu_112_graphics import *
import random
import math

### Game mode

def gameMode_mousePressed(app, event):
    app.player.mousePressed(app, event)

def gameMode_mouseReleased(app, event):
    app.player.mouseReleased(app, event)

def gameMode_mouseDragged(app, event):
    app.player.mouseDragged(app, event)

def gameMode_timerFired(app):
    if checkLose(app) == True:
        app.mode = 'endMode'
    if checkWin(app) == True:
        app.mode = 'winMode'
    updateAll(app)
    bounce(app)

def gameMode_redrawAll(app, canvas):
    app.player.draw(app, canvas)
    app.player.drawLine(app, canvas)
    for planet in app.planets:
        planet.draw(app, canvas)
    for gravityWell in app.gravityWells:
        gravityWell.draw(app, canvas)
    app.portal.draw(canvas, app)

### End mode

def endMode_redrawAll(app, canvas):
    drawLose(app, canvas)

def endMode_keyPressed(app, canvas):
    app.mode = 'gameMode'
    appStarted(app)

### Win mode

def winMode_redrawAll(app, canvas):
    drawWin(app, canvas)

def winMode_keyPressed(app, canvas):
    app.mode = 'gameMode'
    appStarted(app)

###

def appStarted(app):
    #temp code
    earthMass =  5.97 * 10**24
    orbitalRadius = 10**7
    universe = SpaceTime()
    objMass = 4
    orbitalVelocity = (universe.G * earthMass/orbitalRadius)**0.5

    app.positionScale = 10**(-5)   # scaling position (which uses realistic scaling) such that it fits on canvas

    # converting centre position on canvas to 'real' scale for reference in initial position arguments
    scaledcx = (app.width//2)/app.positionScale
    scaledcy = (app.height//2)/app.positionScale

    # Player initial parameters
    app.playerMass = 5
    app.playerScaledInitx = (app.width//2)/app.positionScale
    app.playerScaledInity = (app.height//6)/app.positionScale
    app.playerRadius = app.playerScaledInity

    # game initial conditions
    app.timerDelay = 25
    app.numPlanets = random.randint(1, 6)
    app.mode = 'gameMode'

    # initialising game objects
    app.player = Player(app.playerMass, [app.playerScaledInitx, app.playerScaledInity])
    planet1 = Satellite(objMass, [scaledcx//2, scaledcy//2-orbitalRadius], [orbitalVelocity, 0], [0, 0])
    app.planets = [planet1]
    app.gravityWells = [GravityWell(earthMass, [scaledcx//2, scaledcy//2]), GravityWell(earthMass, [3*scaledcx//2, 3*scaledcy//2])]
    app.universe = SpaceTime()
    portalPosition = random.randint(1, 3)
    app.portal = Portal(portalPosition)

    # initialise planet positions
    makePlanets(app)

# generates random planet obstacle positions in orbit with gravity wells such that no generated orbits overlap with each other or gravity wells
def makePlanets(app):
    for i in range(app.numPlanets):
        # calculate random radius
        r = random.randint(5, 10)
        # calculate mass based on radius
        # exaggerated (exponential) as opposed to proportional to r**3 to exaggerate mass difference based on size
        mass = 10**r  
        # Find a legal radius to place the planet at
        legal = False
        # select random gravity well to place planet with
        wellNumber = random.randint(0, len(app.gravityWells)-1)
        # get lower and upper bounds for orbit
        # orbit should be outside the gravity well it orbits:
        lowerBound = app.gravityWells[wellNumber].r + r 
        # max orbit radius before planet overlaps with starting player position/is out of bounds:
        upperBound = min(app.width//2 - r, app.playerRadius - r)   
        tested = 0    
        # limit of tests set so if a certain gravityWell makes it very difficult to place a planet, 
        # the program doesn't have significant lag, it simply moves past
        # while not legal and tested < 30: 
        #     orbitr = random.randint(lowerBound, upperBound)
        #     # legality check
        #     legal = legalityCheck(app, orbitr)
        #     tested += 1
            
    # see if radius is legal
    # to randomly place at position relative to gravity well
    pass

# def legalityCheck(app, orbitr):
#     for planet in app.planets:
#         radius = 
#         if planet.

### Main Classes

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
        self.captured = False   # Whether the satellite has been 'captured' by a gravity well and hence must be removed from the gameboard

    def draw(self, app, canvas):
        scaledPos = [self.pos[0]*app.positionScale, self.pos[1]*app.positionScale]
        # debug: print(self.colour, scaledPos)
        x0, y0 = scaledPos[0]-self.r, scaledPos[1]-self.r
        x1, y1 = scaledPos[0]+self.r, scaledPos[1]+self.r
        canvas.create_oval(x0, y0, x1, y1, fill=self.colour)

class GravityWell(Satellite):
    def __init__(self, m, pos):
        v = [0, 0]
        a = [0, 0]
        super().__init__(m, pos, v, a)
        self.r = random.randint(20, 50)
        self.colour = 'black'

class Player(Satellite):
    def __init__(self, m, pos):
        v = [0, 0]
        a = [0, 0]
        super().__init__(m, pos, v, a)
        self.r = 10
        self.colour = 'orange'
        self.released = False  # Whether the player has been released at least once (start of game/level)
        self.clicked = False  # Whether the player is currently being clicked
        self.clicks = 0  # Number of times the player has been clicked
        self.changeFactor = 30 # factor by which acceleration is changed in slingshot launch mechanism
        self.forceLineLen = 10 # factor affecting length of the line representing force of initial launch
        self.lineCoords = (0, 0, 0, 0)  # The coordinates for drawing the direction of launch line

    # defines whether the player has been clicked
    def mousePressed(self, app, event):
        scaledPos = [self.pos[0]*app.positionScale, self.pos[1]*app.positionScale]
        if scaledPos[0]-self.r < event.x < scaledPos[0]+self.r and \
            scaledPos[1]-self.r < event.y < scaledPos[1]+self.r:
            self.clicked = True
            self.clicks += 1

    # slingshot mechanism:
    # implements the adjustment of acceleration based on how far back the player drags from the ball
    # logarithm used to make good, playable dynamics:
    # i.e. larger range of slingshot pullback that lead to player object orbiting as opposed to being too slow or shooting off stage
    def mouseReleased(self, app, event):
        if self.clicked:
            scaledPos = [self.pos[0]*app.positionScale, self.pos[1]*app.positionScale]
            signx = 0
            signy = 0
            if (scaledPos[0]-event.x) != 0 and (scaledPos[0]-event.x) != 0:
                signx = (scaledPos[0]-event.x)/abs(scaledPos[0]-event.x)
                signy = (scaledPos[1]-event.y)/abs(scaledPos[1]-event.y)
            changeVector = [signx*math.log(abs(scaledPos[0]-event.x)), \
                signy*math.log(abs(scaledPos[1]-event.y))]
            accelerationChange = [changeVector[0]*self.changeFactor, \
                changeVector[1]*self.changeFactor]
            self.a = [self.a[0]+accelerationChange[0], self.a[1]+accelerationChange[1]]
            self.released = True
        self.clicked = False

    # represent force due to initial player launch
    def mouseDragged(self, app, event):
        # same code as mouseReleased to determine force, except in real time for dragging, not for release
        if self.clicked:
            scaledPos = [self.pos[0]*app.positionScale, self.pos[1]*app.positionScale]
            # necessary computation for log
            signx = 0
            signy = 0
            if (scaledPos[0]-event.x) != 0 and (scaledPos[0]-event.y) != 0:
                signx = (scaledPos[0]-event.x)/abs(scaledPos[0]-event.x)
                signy = (scaledPos[1]-event.y)/abs(scaledPos[1]-event.y)
                changeVector = [signx*math.log(abs(scaledPos[0]-event.x)), signy*math.log(abs(scaledPos[1]-event.y))]
            else:
                changeVector = [0, 0]
            self.lineCoords = (scaledPos[0], scaledPos[1], scaledPos[0] + self.forceLineLen*changeVector[0], scaledPos[1] + self.forceLineLen*changeVector[1])

    def drawLine(self, app, canvas):
        if self.clicked:
            (x0, y0, x1, y1) = self.lineCoords
            canvas.create_line(x0, y0, x1, y1)
    
# class SpaceTime contains implementation of gravity
class SpaceTime(object):
    def __init__(self):
        self.G = 7 * 10**(-11)  # Gravitational constant - real = 6.6743*10**(-11), changed to get better effects
        self.time = 0
        self.dt = 75 # timestep (useful to adjust speed)

    # components of Verlet Integration (second order integrator method):
    # update position, velocity, and acceleration
    # Mathematical reference: 
    # https://www.physics.udel.edu/~bnikolic/teaching/phys660/numerical_ode/node5.html
    def updatePos(self, on):
        # updating position for vector components individually
        for i in range(2):
            on.pos[i] += on.v[i]*self.dt + 0.5*on.a[i]*(self.dt**2)

    # calculating gravitational acceleration on "on" by "by" using a = Gm/r**2 in direction r^
    def updateAcceleration(self, on, by):
        r = (by.pos[0] - on.pos[0], by.pos[1] - on.pos[1])
        # debug: print(f"r = {r}")
        rsquared = r[0]**2 + r[1]**2
        Gm_by_rsq = (self.G * by.m)/rsquared
        a = (Gm_by_rsq * r[0]/(rsquared**0.5), Gm_by_rsq * r[1]/(rsquared**0.5))
        # debug: print(f"a = {a}")
        on.a = [on.a[0]+a[0], on.a[1]+a[1]]
        if rsquared < 10000000000000:
            on.captured = True

    def updateVelocity(self, on):
        # updating velocity for vector components individually
            for i in range(2):
                on.v[i] += 0.5*(on.aPrev[i] + on.a[i])*self.dt

    def updateTime(self):
        self.time += self.dt

# Portal to win/next level
class Portal(object):
    def __init__(self, position):
        self.colour = 'blue'
        self.position = position
        self.coords = [0, 0, 0, 0]
        self.length = 50  # half of length
        self.width = 5  # half of width
        self.margin = 15 # margin between edge of screen and centre of portal
    
    # get coordinates corresponding to the 3 different possible positions (board left, board right, board bottom)
    def getCoords(self, app):
        # board left
        if self.position == 1:
            self.coords = [self.margin-self.width, app.height//2-self.length, \
                self.margin+self.width, app.height//2+self.length]
        # board right
        if self.position == 2:
            self.coords = [(app.width-self.margin)-self.width, app.height//2-self.length, \
                (app.width-self.margin)+self.width, app.height//2+self.length]
        # board bottom
        if self.position == 3:
            self.coords = [app.width//2-self.length, (app.height-self.margin)-self.width, \
                app.width//2+self.length, (app.height-self.margin)+self.width]

    def draw(self, canvas, app):
        self.getCoords(app)
        (x0, y0, x1, y1) = self.coords
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.colour)

### Functions to update all objects on screen

# updating all satellites based on Verlet integration
def updateAll(app):
        # initialise  - As previous and current acceleration required individually for each force, 
        # dictionary initialised for every object with objects exerting force on it
        updateAllPos(app)
        updateAllAcceleration(app)
        # print(f'    {app.player.a}')
        # sum all aprevs; as
        updateAllVelocity(app)
        app.universe.updateTime()

def updateAllPos(app):
    if app.player.released == True:
        app.universe.updatePos(app.player)
    for planet in app.planets:
        app.universe.updatePos(planet)
    # gravity wells are stationary

# player mass & gravitational field is taken as too small to affect other Satellites
def updateAllAcceleration(app):        
    for planet in app.planets:
        # update acceleration on planet due to every other planet2
        planet.aPrev = planet.a     # necessary starting conditions
        planet.a = [0,0]
        for planet2 in app.planets:
            if planet != planet2:  # ensures planet doesn't update its own acceleration
                app.universe.updateAcceleration(planet, planet2)
        # update aceleration on planet due to gravity well  
        # only closest gravity well's acceleration is considered to have a stable orbit for the orbiting planets
        closestGravityWell = getClosestGravityWell(app, planet)
        app.universe.updateAcceleration(planet, closestGravityWell)

    # update acceleration on player due to all gravity wells
    if app.player.released == True:
        app.player.aPrev = app.player.a     # necessary starting conditions
        app.player.a = [0,0]
        for gravityWell in app.gravityWells:
            app.universe.updateAcceleration(app.player, gravityWell)
        # update acceleration on player due to planets
        for planet in app.planets:
            app.universe.updateAcceleration(app.player, planet)

def getClosestGravityWell(app, planet):
    closestGravityWell = None
    for gravityWell in app.gravityWells:
        if closestGravityWell == None:
            closestGravityWell = gravityWell
        if distBetween(app, gravityWell, planet) <= distBetween(app, closestGravityWell, planet):
            closestGravityWell = gravityWell
    return closestGravityWell

# returns distance between 2 objects in terms of the scaled positioning on the canvas
def distBetween(app, object1, object2):
    scaled1Pos = [object1.pos[0]*app.positionScale, object1.pos[1]*app.positionScale]
    scaled2Pos = [object2.pos[0]*app.positionScale, object2.pos[1]*app.positionScale]
    distX = abs(scaled1Pos[0] - scaled2Pos[0])
    distY = abs(scaled1Pos[1] - scaled2Pos[1])
    distBetween = (distX**2 + distY**2)**0.5
    return distBetween

def updateAllVelocity(app):
    if app.player.released == True:
        app.universe.updateVelocity(app.player)
    for planet in app.planets:
        app.universe.updateVelocity(planet)
    # gravity wells are stationary

### Win/lose conditions

def checkLose(app):
    scaledPos = [app.player.pos[0]*app.positionScale, app.player.pos[1]*app.positionScale]
    # if 0 > scaledPos[0] or scaledPos[0] > app.width:
    #     return True
    # if 0 > scaledPos[1] or scaledPos[1] > app.height:
    #     return True
    for planet in app.planets:
        if areColliding(app, app.player, planet):
            return True
    for gravityWell in app.gravityWells:
        if areColliding(app, app.player, gravityWell):
            return True

def drawLose(app, canvas):
    canvas.create_text(300, 100, text='Lost',
                       fill='black', font='Times 28 bold')
    canvas.create_text(300, 200, text='Press any key to play again',
                       fill='black', font='Times 25 bold')

def checkWin(app):
    if areRectColliding(app, app.player, app.portal):
        return True
    return False

def drawWin(app, canvas):
    canvas.create_text(300, 100, text='Won!!!',
                       fill='black', font='Times 28 bold')
    canvas.create_text(300, 200, text='Press any key to play again',
                       fill='black', font='Times 25 bold')

### Features of game (collisions and bounce on edge)

def areColliding(app, object1, object2):
    # check if distance between centres is less than sum of radii
    if distBetween(app, object1, object2) <= (object1.r + object2.r):
        return True
    return False

# Rectangle bounds based collision check for portal, which is rectangular
def areRectColliding(app, object, portal):
    # get coordinates in x0, y0, x1, y1 form
    scaledObjPos = [object.pos[0]*app.positionScale, object.pos[1]*app.positionScale]
    objCoords = [scaledObjPos[0]-object.r, scaledObjPos[1]-object.r, \
        scaledObjPos[0]+object.r, scaledObjPos[1]+object.r]
    portalCoords = portal.coords

    # check x of object in bounds of portal
    if (portalCoords[0] <= objCoords[0] <= portalCoords[2]) \
        or (portalCoords[0] <= objCoords[2] <= portalCoords[2]):
        # check y of object in bounds of portal
        if (portalCoords[1] <= objCoords[1] <= portalCoords[3]) \
            or (portalCoords[1] <= objCoords[3] <= portalCoords[3]):
            return True
    return False

# bounce on edge
def isOnEdge(app):
    scaledPos = [app.player.pos[0]*app.positionScale, app.player.pos[1]*app.positionScale]
    if 0 >= (scaledPos[0]-app.player.r) or (scaledPos[0]+app.player.r) >= app.width:
        return 'l/r' # left or right edge
    if 0 >= (scaledPos[1]-app.player.r) or (scaledPos[1]+app.player.r) >= app.height:
        return 't/b' # top or bottom edge
    return 'n'  # not on edge

# implementing bounce as inelastic collision with wall
def bounce(app):
    # side bounce means horizontal velocity changes
    if isOnEdge(app) == 'l/r':
        app.player.v[0] = -app.player.v[0]
    # top/bottom bounce means vertical velocity changes
    elif isOnEdge(app) == 't/b':
        app.player.v[1] = -app.player.v[1]

# Run game
def playGravityWells():
    runApp(width = 600, height = 600)

playGravityWells()
