# Platformer
## Made in python
This version works completely fine (except for the lack of levels and it just crashes when you try and load more levels)

## Known Bugs:
* Perfomance Issues
* Clipping on the ground
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

The name can be anything but if it is `Quicksand` the player will slowly sink into the ground instead of staying above it.
