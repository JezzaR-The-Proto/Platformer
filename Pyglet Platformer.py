import pyglet, os, datetime, random, math, shapely
from pyglet.window import key
from pyglet import clock
from random import randint
from shapely.geometry import LineString, Point

gameFolder = os.path.dirname(os.path.realpath(__file__))
assetsFolder = os.path.join(gameFolder,"assets")
pyglet.resource.path = [assetsFolder]
pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

width = 1280
height = 720

sky = pyglet.graphics.OrderedGroup(2)
background = pyglet.graphics.OrderedGroup(1)
foreground = pyglet.graphics.OrderedGroup(0)
groundTexture = pyglet.resource.image("grass.png")
dirtTexture = pyglet.resource.image("dirt.png")
skyTexture = pyglet.resource.image("sky.png")
skySprite = pyglet.sprite.Sprite(skyTexture, x=0, y=0, group=sky)
playerStill = pyglet.resource.image("PlayerStill.png")
playerLeft = pyglet.resource.image("PlayerLeft.png")
playerRight = pyglet.resource.image("PlayerRight.png")
playerUp = pyglet.resource.image("PlayerUp.png")
playerDown = pyglet.resource.image("PlayerDown.png")
playerTextures = []
playerTextures.append(playerStill)
playerTextures.append(playerUp)
playerTextures.append(playerDown)
playerTextures.append(playerLeft)
playerTextures.append(playerRight)
playerTextures.append(groundTexture)
playerTextures.append(dirtTexture)
for tex in playerTextures:
    tex.anchor_x = tex.width // 2
    tex.anchor_y = tex.height // 2
playerSprite = pyglet.sprite.Sprite(playerStill, x=32, y=103, group=foreground)
icon1 = pyglet.resource.image("16x16.png")
icon2 = pyglet.resource.image("32x32.png")


pressedKeys = {}
alive = 1
moving = False
xVel = 0
yVel = 0
currentGround = {}
groundPoses = []
level = 1
onWallLeft = False
onWallRight = False
onFloor = True

# The game window
class Window(pyglet.window.Window):

    def __init__(self):
        super(Window, self).__init__(width = width, height = height, vsync = True, caption="Platformer")
        self.set_icon(icon1,icon2)
        pyglet.clock.schedule_interval(self.update, 1.0/round(pyglet.clock.get_fps(), 2))
        pyglet.clock.schedule_interval(self.physics, 1.0/round(pyglet.clock.get_fps(), 2))
        pyglet.clock.schedule_interval(self.collision, 1.0/round(pyglet.clock.get_fps(), 2))

    def update(self, dt):
        self.check_bounds(playerSprite)

    def on_draw(self):
        pyglet.clock.tick()
        self.clear()
        skySprite.draw()
        self.create_ground()
        self.drawGround()
        playerSprite.draw()
        fpsDisplay = pyglet.text.Label("FPS: " + str(round(pyglet.clock.get_fps(), 2)), font_size = 20, x = 10, y = 690)
        fpsDisplay.draw()

    def on_key_release(dt, symbol, modifiers):
        try:
            del pressedKeys[symbol]
        except:
            pass

    def on_key_press(dt, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        pressedKeys[symbol] = True

    def physics(dt, dts):
        global xVel, yVel, moving, onWallRight, onWallLeft, onFloor
        moving = False
        if key.W in pressedKeys:
            if onFloor:
                yVel = 7.5
                playerSprite.image = playerUp
                moving = True
                onFloor = False
        if key.A in pressedKeys:
            xVel -= 1
            playerSprite.image = playerLeft
            moving = True
        if key.D in pressedKeys:
            xVel += 1
            playerSprite.image = playerRight
            moving = True
        if (playerSprite.y) == 720:
            playerSprite.y = 656
        xVel = xVel * 0.85
        yVel -= 0.25
        if yVel == -5:
            yVel = -5
        if xVel < 0.01 and xVel > -0.01:
            xVel = 0
        if yVel < 0.01 and yVel > -0.01:
            yVel = 0
        if not(moving):
            playerSprite.image = playerStill
        playerSprite.x += xVel
        playerSprite.y += yVel

    def check_bounds(dt, spriteNam):
        global xVel, yVel, level
        min_x = 32
        max_x = 1252
        max_y = 682
        if spriteNam.x < min_x:
            spriteNam.x = min_x
            xVel = 0
        elif spriteNam.x > max_x:
            spriteNam.x = min_x
            level += 1
        if spriteNam.y > max_y:
            spriteNam.y = max_y
            yVel = 0
        if spriteNam.y < 35:
            spriteNam.y = 103
            spriteNam.x = min_x
            yVel = 0
            xVel = 0

    def create_ground(dt):
        global currentGround, level, groundPoses
        x = 35
        groundCount = 0
        groundPoses = []
        if level == 1:
            while x < 1315:
                y = 35
                groundPoses.append(x)
                groundPoses.append(y)
                groundPoses.append(groundTexture)
                currentGround[groundCount] = f"{x},{y}"
                groundCount += 1
                x += 70
        elif level == 2:
            while x < 1315:
                if x != 665:
                    y = 35
                    groundPoses.append(x)
                    groundPoses.append(y)
                    groundPoses.append(groundTexture)
                    currentGround[groundCount] = f"{x},{y},{groundTexture}"
                    groundCount += 1
                    x += 70
                else:
                    y = 105
                    groundPoses.append(x)
                    groundPoses.append(y)
                    groundPoses.append(groundTexture)
                    currentGround[groundCount] = f"{x},{y},{groundTexture}"
                    groundCount += 1
                    y = 35
                    groundPoses.append(x)
                    groundPoses.append(y)
                    groundPoses.append(dirtTexture)
                    currentGround[groundCount] = f"{x},{y},{dirtTexture}"
                    groundCount += 1
                    x += 70

    def collision(dt, dts):
        global yVel, onFloor, xVel
        RightTop = Point(playerSprite.x+32, playerSprite.y+32)
        RightBottom = Point(playerSprite.x+32, playerSprite.y-32)
        LeftTop = Point(playerSprite.x-32, playerSprite.y+32)
        LeftBottom = Point(playerSprite.x-32, playerSprite.y-32)
        playerTopSide = LineString([LeftTop,RightTop])
        playerRightSide = LineString([RightTop,RightBottom])
        playerBottomSide = LineString([LeftBottom,RightBottom])
        playerLeftSide = LineString([LeftTop,LeftBottom])
        coord = 0
        getPos = 0
        while getPos < len(groundPoses):
            currentX = groundPoses[getPos]
            currentY = groundPoses[getPos+1]
            getPos += 3
            groundTopSide = LineString([(currentX-35, currentY+35),(currentX+35, currentY+29)])
            groundLeftSide = LineString([(currentX-25, currentY+35),(currentX-35, currentY-35)])
            groundBottomSide = LineString([(currentX-35, currentY-30),(currentX+35, currentY-35)])
            groundRightSide = LineString([(currentX+25, currentY-35),(currentX+35, currentY+35)])
            oppositeGroundTopSide = LineString([(currentX-35, currentY+29),(currentX+35, currentY+35)])
            oppositeGroundLeftSide = LineString([(currentX-35, currentY+35),(currentX-25, currentY-35)])
            oppositeGroundBottomSide = LineString([(currentX-35, currentY-35),(currentX+35, currentY-30)])
            oppositeGroundRightSide = LineString([(currentX+35, currentY-35),(currentX+25, currentY+35)])
            intersectBottom = playerBottomSide.intersection(groundTopSide)
            intersectTop = playerTopSide.intersection(groundBottomSide)
            intersectRight = playerRightSide.intersection(groundLeftSide)
            intersectLeft = playerLeftSide.intersection(groundRightSide)
            oppositeIntersectBottom = playerBottomSide.intersection(oppositeGroundTopSide)
            oppositeIntersectTop = playerTopSide.intersection(oppositeGroundBottomSide)
            oppositeIntersectRight = playerRightSide.intersection(oppositeGroundLeftSide)
            oppositeIntersectLeft = playerLeftSide.intersection(oppositeGroundRightSide)
            if intersectBottom or oppositeIntersectBottom:
                playerSprite.y = currentY + 67
                onFloor = True
                while yVel < 0:
                    yVel += 0.25
            if intersectTop or oppositeIntersectTop:
                playerSprite.y = currentY - 67
            if intersectRight or oppositeIntersectRight:
                playerSprite.x = currentX - 67
                if xVel > 0:
                    xVel = 0
            if intersectLeft or oppositeIntersectLeft:
                playerSprite.x = currentX + 67
                if xVel < 0:
                    xVel = 0

    def drawGround(dt):
        coord = 0
        groundSprite = pyglet.sprite.Sprite(groundTexture, group=background)
        for pos in groundPoses:
            if coord == 0:
                groundSprite.x = pos
                coord = 1
            elif coord == 1:
                groundSprite.y = pos
                coord = 2
            else:
                groundSprite.image = pos
                coord = 0
                groundSprite.draw()

win = Window()
pyglet.app.run()
