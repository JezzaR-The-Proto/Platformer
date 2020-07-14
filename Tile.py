import pyglet

class Tile:
	def __init__(self, width: int, height: int, texture, startX: int, startY: int, name: str):
		self.Width = width
		self.Height = height
		self.Sprite = pyglet.sprite.Sprite(texture, x=startX, y=startY)
		self.Sprite.draw()
		self.Pos = [startX, startY]
		self.Name = name

	def draw(self):
		self.Sprite.update()
		self.Sprite.draw()
