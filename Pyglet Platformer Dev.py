import pyglet, os, datetime, random, math
from pyglet.window import key
from pyglet import clock
from random import randint

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
        pyglet.clock.schedule_interval(self.update, 1.0/120.0)
        pyglet.clock.schedule_interval(self.physics, 1.0/120.0)

    def update(self, dt):
        self.check_bounds(playerSprite)

    def on_draw(self):
        global currentGround
        pyglet.clock.tick()
        self.clear()
        skySprite.draw()
        self.create_ground()
        self.drawGround()
        playerSprite.draw()
        self.collision()
        print("FPS: " + str(round(pyglet.clock.get_fps(), 2)))
        print("X Speed: " + str(xVel))
        print("Y Speed: " + str(yVel))

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
            if onWallRight:
                yVel = 7.5
                xVel = -5
                playerSprite.image = playerUp
                moving = True
                onWallRight = False
            elif onWallLeft:
                yVel = 7.5
                xVel = 5
                playerSprite.image = playerUp
                moving = True
                onWallLeft = False
            elif onFloor:
                yVel = 7.5
                playerSprite.image = playerUp
                moving = True
                onFloor = False
            moving = True
        if key.S in pressedKeys:
            yVel -= 2
            playerSprite.image = playerDown
            moving = True
        if key.A in pressedKeys:
            if xVel == 0:
                xVel = -1
            else:
                xVel -= 1
            playerSprite.image = playerLeft
            moving = True
        if key.D in pressedKeys:
            if xVel == 0:
                xVel = 1
            else:
                xVel += 1
            playerSprite.image = playerRight
            moving = True
        if (playerSprite.y) == 720:
            playerSprite.y = 656
        xVel = xVel * 0.85
        yVel -= 0.25
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
                currentGround[groundCount] = f"{x},{y}"
                groundCount += 1
                x += 70
        elif level == 2:
            while x < 1315:
                if x != 665:
                    y = 35
                    groundPoses.append(x)
                    groundPoses.append(y)
                    currentGround[groundCount] = f"{x},{y},{groundTexture}"
                    groundCount += 1
                    x += 70
                else:
                    y = 105
                    groundPoses.append(x)
                    groundPoses.append(y)
                    currentGround[groundCount] = f"{x},{y},{groundTexture}"
                    groundCount += 1
                    y = 35
                    groundPoses.append(x)
                    groundPoses.append(y)
                    currentGround[groundCount] = f"{x},{y},{dirtTexture}"
                    groundCount += 1
                    x += 70

    def collision(dt):
        global currentGround, xVel, yVel, onWallRight, onWallLeft, onFloor
        playerTopSide = {(playerSprite.x-32, playerSprite.y+32),(playerSprite.x+32, playerSprite.y+32)}
        playerRightSide = {(playerSprite.x-32, playerSprite.y+32),(playerSprite.x-32, playerSprite.y-32)}
        playerBottomSide = {(playerSprite.x-32, playerSprite.y-32),(playerSprite.x+32, playerSprite.y-32)}
        playerLeftSide = {(playerSprite.x+32, playerSprite.y-32),(playerSprite.x+32, playerSprite.y+32)}

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
            elif coord == 2:
                groundSprite.image = pos
                coord = 0
                groundSprite.draw()

win = Window()
pyglet.app.run()
