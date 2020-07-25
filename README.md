# Platformer
## Made in python
I mean, it kinda works? You clip on the ground a bit but eh its good enough for me.

## Known Bugs:
* Perfomance Issues
* Clipping on the ground
* There is literally 1 level
* Its just flat ground
* Its boring
Yes ik all of these pls dont bug me about it

## Level Editing:
Add your own levels!
The game uses a json file to store them.
Each level format should be:
```json
{
		"StartingPos": [35, 105],
		"Data": ["35,35,gr,Ground","105,35,gr,Ground"]
}
```
The `StartingPos` key is for what X and Y the game should start the player at.

The `Data` key is for what tiles exist inside the level. This is an array and each entry in the array should be: "{XPos},{YPos},{Texture},{Name}".

Currently supported textures are: `gr` for the default grass texture and `drt` for the default dirt texture.

~~Yes there is no way to change level ingame shut up~~ If you change `self.CurrentLevel = 1` to whatever level you want inside the json array (Its the array index + 1) you can access whatever level you want.
