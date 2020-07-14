import pyglet, typing
from shapely.geometry import box, Point, LinearRing

class Player:
	def __init__(self, width: int, height: int, texture, startX: int, startY: int):
		self.Width = width
		self.Height = height
		self.Sprite = pyglet.sprite.Sprite(texture, x=startX, y=startY)
		self.Sprite.draw()
		self.Pos = [startX, startY]
		self.Acc = [0, 0]
		self.Vel = [0, 0]
		self.OnFloor = False
		self.Gravity = 0.5

	def draw(self):
		self.Sprite.update(x = self.Pos[0], y = self.Pos[1])
		self.Sprite.draw()

	def update(self, texture: typing.Optional[pyglet.resource.image] = None):
		if texture != None:
			self.Sprite.image = texture
		self.Pos[0] += self.Vel[0]
		self.Pos[0] = round(self.Pos[0], 1)
		self.Pos[1] += self.Vel[1]
		self.Pos[1] = round(self.Pos[1], 1)
		self.Vel[0] *= 0.85
		self.Vel[1] -= self.Gravity
		self.Vel[1] = self.clamp(self.Vel[1], -20, 10)
		self.Vel[0] = self.clamp(self.Vel[0], -5, 5)
		if self.Vel[1] < 0.01 and self.Vel[1] > -0.01:
			self.Vel[1] = 0
		if self.Vel[0] < 0.01 and self.Vel[0] > -0.01:
			self.Vel[0] = 0

	def clamp(self, n, minn, maxn):
		if n < minn:
			return minn
		elif n > maxn:
			return maxn
		else:
			return n

	def applyforce(self, XForce: int, YForce: int):
		if XForce != 0:
			self.Vel[0] += XForce
		if YForce != 0:
			self.Vel[1] += YForce

	def collideswith(self, Tile):
		# Top left, Bottom left, Top right, Bottom right.
		TileTopLeft = Point(Tile.Pos[0] - (Tile.Width // 2), Tile.Pos[1] + (Tile.Height // 2))
		TileBottomLeft = Point(Tile.Pos[0] - (Tile.Width // 2), Tile.Pos[1] - (Tile.Height // 2))
		TileTopRight = Point(Tile.Pos[0] + (Tile.Width // 2), Tile.Pos[1] + (Tile.Height // 2))
		TileBottomRight = Point(Tile.Pos[0] + (Tile.Width // 2), Tile.Pos[1] - (Tile.Height // 2))
		TileBox = LinearRing([TileTopLeft, TileBottomLeft, TileBottomRight, TileTopRight, TileTopLeft])
		selfTopLeft = Point(self.Pos[0] - (self.Width // 2), self.Pos[1] + (self.Height // 2))
		selfBottomLeft = Point(self.Pos[0] - (self.Width // 2), self.Pos[1] - (self.Height // 2))
		selfTopRight = Point(self.Pos[0] + (self.Width // 2), self.Pos[1] + (self.Height // 2))
		selfBottomRight = Point(self.Pos[0] + (self.Width // 2), self.Pos[1] - (self.Height // 2))
		selfBox = LinearRing([selfTopLeft, selfBottomLeft, selfBottomRight, selfTopRight, selfTopLeft])
		if TileBox.intersection(selfBox):
			return True

	def checkfloor(self, Tile):
		selfTopLeft = Point(self.Pos[0] - (self.Width // 2), self.Pos[1] + (self.Height // 2))
		selfBottomLeft = Point(self.Pos[0] - (self.Width // 2), self.Pos[1] - (self.Height // 2))
		selfTopRight = Point(self.Pos[0] + (self.Width // 2), self.Pos[1] + (self.Height // 2))
		selfBottomRight = Point(self.Pos[0] + (self.Width // 2), self.Pos[1] - (self.Height // 2))
		selfBox = LinearRing([selfTopLeft, selfBottomLeft, selfBottomRight, selfTopRight, selfTopLeft])
		TileTopLeft = Point(Tile.Pos[0] - (Tile.Width // 2), Tile.Pos[1] + (Tile.Height // 2))
		TileBottomLeft = Point(Tile.Pos[0] - (Tile.Width // 2), Tile.Pos[1] + (Tile.Height // 4))
		TileTopRight = Point(Tile.Pos[0] + (Tile.Width // 2), Tile.Pos[1] + (Tile.Height // 2))
		TileBottomRight = Point(Tile.Pos[0] + (Tile.Width // 2), Tile.Pos[1] + (Tile.Height // 4))
		TileBox = LinearRing([TileTopLeft, TileBottomLeft, TileBottomRight, TileTopRight, TileTopLeft])
		if TileBox.intersection(selfBox):
			return True

	def resetvel(self, Tile, Dir: typing.Optional[str] = None):
		if Dir == "UP":
			while self.Vel[1] > 0.5:
				self.Vel[1] -= 0.01
			self.OnFloor = False
		elif Dir == "DOWN":
			while self.Vel[1] < 0.5:
				self.Vel[1] += 0.01
			self.OnFloor = True
		elif Dir == "LEFT":
			if not self.checkfloor(Tile):
				while self.Vel[0] < 0.5:
					self.Vel[0] += 0.01
			print("Left")
		elif Dir == "RIGHT":
			if not self.checkfloor(Tile):
				while self.Vel[0] > 0.5:
					self.Vel[0] -= 0.01
			print("Right")
		else:
			if Tile.Name == "Quicksand":
				while self.Vel[1] < -0.5:
					self.Vel[1] += 0.01
				self.OnFloor = True
			else:
				while self.Vel[1] < 0.5:
					self.Vel[1] += 0.01
				self.OnFloor = True

	def nextlevel(self, width: int):
		if self.Pos[0] + self.Width // 2 > width:
			return True
		return False

	def movepos(self, x: int, y: int):
		self.Pos = [x, y]
		return True
