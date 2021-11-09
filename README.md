# Alien Invasion
This is a remake of the classic game space invaders.
In Alien Invasion, the player controls a rocket ship that appears at the bottom center of the screen.
The player can move the ship right,left up and down using the arrow keys and shoot bullets using the spacebar.
When the game begins, a fleet of aliens' ships fills the sky and moves across and down the screen.
The player shoots and destroys the aliens' ships.
If any alien hits the player's ship or reaches the bottom of the screen, the player losses a ship.
If the player shoots all the aliens' ships, a new fleet appears.
As the game continues the aliens' ships become stronger, so destroying the ships require more shots or stronger firearm.
There are 3 types of power-ups: another life, weapon upgrade and a shield.
The shield protects from aliens' ships shooting and crashing into an alien ship.
The shield doesn't protect against the fleet reaching the bottom (which will make the player lose a life, and the level to restart).


https://user-images.githubusercontent.com/13748234/140519262-a9b98d52-4747-470c-96f9-59a22b59649b.mp4



### How to run this game?
In order to run this game you need to have python and the pygame library installed.

For downloading python (Use python 3.7.7 or greater since it's better for pygame):
https://www.python.org/downloads/


The best way to install pygame is with the pip tool (which is what python uses to install packages). Note, this comes with python in recent versions. We use the --user flag to tell it to install into the home directory, rather than globally.  
`python3 -m pip install -U pygame --user`

Download/clone this repo, in the extracted folder enter in the command line:  
`python alien_invasion.py`

