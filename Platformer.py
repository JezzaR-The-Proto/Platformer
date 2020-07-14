import pyglet, os, datetime, json
from pyglet.window import key
from pyglet import clock
from random import randint
from Player import Player
from Tile import Tile

gameFolder = os.path.dirname(os.path.realpath(__file__))
assetsFolder = os.path.join(gameFolder,"assets")
pyglet.resource.path = [assetsFolder]
levelFolder = os.path.join(gameFolder, "levels")
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
playerSprite = pyglet.sprite.Sprite(playerStill, x=100, y=200, group=foreground)
icon1 = pyglet.resource.image("16x16.png")
icon2 = pyglet.resource.image("32x32.png")

pressedKeys = {}
Extras = False

# The game window
class Window(pyglet.window.Window):

	def __init__(self):
		super(Window, self).__init__(width = width, height = height, vsync = True, caption="Platformer")
		self.set_icon(icon1,icon2)
		self.CurrentLevel = 1
		self.PlayerSprite = Player(playerStill.width, playerStill.height, playerStill, 0, 0)
		self.LoadLevel(self.CurrentLevel)
		pyglet.clock.schedule_interval(self.DrawScreen, 1/60)
		pyglet.clock.schedule_interval(self.UpdatePlayer, 1/60)
		self.Gravity = -1
		self.AveFPS = []

	def on_draw(self):
		pyglet.clock.tick()
		FPSVal = str(round(pyglet.clock.get_fps(), 2))
		self.AveFPS.append(float(FPSVal))
		if Extras:
			TotFPS = 0
			for FPSValue in self.AveFPS:
				TotFPS += float(FPSValue)
			TotFPS /= len(self.AveFPS)
			while len(self.AveFPS) > 5000:
				del self.AveFPS[0]
			fpsDisplay = pyglet.text.Label(f"FPS: {FPSVal}", font_size=10, x=10, y=700)
			AveFPSDisplay = pyglet.text.Label(f"Ave FPS: {round(TotFPS, 2)}", font_size=10, x=10, y=680)
			fpsDisplay.draw()
			AveFPSDisplay.draw()

	def on_key_release(dt, symbol, modifiers):
		try:
			del pressedKeys[symbol]
		except:
			pass

	def on_key_press(dt, symbol, modifiers):
		global Extras
		if symbol == key.ESCAPE:
			pyglet.app.exit()
		if symbol == key.F3:
			Extras = not Extras
		pressedKeys[symbol] = True

	def UpdatePlayer(self, dt):
		Moved = False
		if key.W in pressedKeys and self.PlayerSprite.OnFloor:
			self.PlayerSprite.applyforce(0, 18)
			Moved = "W"
		if key.S in pressedKeys:
			self.PlayerSprite.applyforce(0, -0.8)
			Moved = "S"
		if key.A in pressedKeys:
			self.PlayerSprite.applyforce(-1, 0)
			Moved = "A"
		if key.D in pressedKeys:
			self.PlayerSprite.applyforce(1, 0)
			Moved = "D"
		if not(Moved):
			self.PlayerSprite.update(playerStill)
		elif Moved == "W":
			self.PlayerSprite.update(playerUp)
		elif Moved == "S":
			self.PlayerSprite.update(playerDown)
		elif Moved == "A":
			self.PlayerSprite.update(playerLeft)
		elif Moved == "D":
			self.PlayerSprite.update(playerRight)
		Collide = False
		for CurrentTile in self.LoadedData:
			if abs(CurrentTile.Pos[0] - self.PlayerSprite.Pos[0]) > 100:
				continue
			if abs(CurrentTile.Pos[1] - self.PlayerSprite.Pos[1]) > 100:
				continue
			if self.PlayerSprite.collideswith(CurrentTile):
				if key.W in pressedKeys:
					self.PlayerSprite.resetvel(CurrentTile, "UP")
					Collide = True
				if key.S in pressedKeys:
					self.PlayerSprite.resetvel(CurrentTile, "DOWN")
					Collide = True
				if key.A in pressedKeys:
					self.PlayerSprite.resetvel(CurrentTile, "LEFT")
					Collide = True
				if key.D in pressedKeys:
					self.PlayerSprite.resetvel(CurrentTile, "RIGHT")
					Collide = True
				if Moved == False:
					self.PlayerSprite.resetvel(CurrentTile)
					Collide = True
			if self.PlayerSprite.checkfloor(CurrentTile):
				self.PlayerSprite.resetvel(CurrentTile)
				Collide = True
		if not Collide:
			self.PlayerSprite.OnFloor = False
		if self.PlayerSprite.nextlevel(self.width):
			self.CurrentLevel += 1
			self.LoadLevel(self.CurrentLevel)

	def DrawScreen(self, dt):
		self.clear()
		self.PlayerSprite.draw()
		for CurrentTile in self.LoadedData:
			CurrentTile.draw()

	def LoadLevel(self, num: int):
		Index = num - 1
		self.LoadedData = []
		with open("Level.Data","r") as LevelData:
			LevelData = json.loads(LevelData.read())
		GroundData = LevelData["levels"][Index]["Data"]
		for Data in GroundData:
			Data = Data.split(",")
			if Data[2] == "gr":
				Data[2] = groundTexture
			elif Data[2] == "drt":
				Data[2] = dirtTexture
			Data[0] = int(Data[0])
			Data[1] = int(Data[1])
			CurrentTile = Tile(Data[2].width, Data[2].height, Data[2], Data[0], Data[1], Data[3])
			self.LoadedData.append(CurrentTile)
		StartingPos = LevelData["levels"][Index]["StartingPos"]
		self.PlayerSprite.movepos(StartingPos[0], StartingPos[1])

win = Window()
pyglet.app.run()
