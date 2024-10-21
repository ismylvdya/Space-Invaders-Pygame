<p align="center">
      <img src="images/for README/header_img.png" width="93%">
</p>

## 👾 About

A Space Invaders based game created in Python with visualization via PyGame, for the purpose of practicing in PyGame library.

## 👀 How it looks

<img src="images/for README/blinking_death.webp" width="49%"/> <img src="images/for README/win.webp" width="49%"/>

## 🕹 How to use

### Rules

- your goal is to shoot all the aliens before they reach the bottom of the screen

- if your cannon is hit you lose 1 hp

  if you encounter an alien, it will die, and you will lose 1 hp

- if you die the round automatically starts again

- if you hit a green alien, your hp increases by 1

  if you hit a black alien, the frequency of aliens shooting increases 3 times for 3 sec (the white time progress bar appears in the top right screen corner)
  <p align="center">
      <img src="images/for README/positive_negative_death.webp" width="49%">
  </p>

- if you hit the red UFO your cannon becomes invulnerable to bullets and touch from aliens for 7 seconds (the red time progress bar appears in the top right screen corner)

  <p align="center">
        <img src="images/for README/ufo.webp" width="49%">
  </p>
  
- highscore - the least number of bullets you fired during all winning rounds

- the fewer aliens left, the greater their horizontal speed

- you can still shoot on the win screen 👀


### What can be changed in [CONSTANTS.py](source/CONSTANTS.py)

General
+ screen size
+ framerate
+ the presence of sounds

Cannon
- the speed of the cannon and your bullets
- initial number of hp
- flashing of the cannon when hit and delay time when losing

Aliens
+ number of aliens
+ the speed and acceleration of the aliens, the speed of their bullets
+ duration of the splash when hitting an alien
+ the upper and lower limits of the number of green and black aliens
+ default frequency of aliens shooting
+ how many times does the frequency of shooting increase when hitting a black alien  
and the duration of this rapid shooting

UFO
- the upper limits of the moment of the UFO's appearance
- duration of the invulnerability effect after hitting the UFO
- UFO's speed

### Keys


- <kbd>a</kbd> and <kbd>d</kbd> &thinsp; or &thinsp; <kbd>◀</kbd> and <kbd>▶</kbd> &thinsp; move your cannon left and right
- <kbd>SPASE</kbd>, &thinsp; <kbd>w</kbd> &thinsp; or &thinsp; <kbd>▲</kbd> &thinsp; shoots a bullet
- <kbd>i</kbd> turns on a very dense stream of bullets 
  
  <img src="images/for README/infinitybullets.webp" width="49%"/> <img src="images/for README/kaleidoscope.webp" width="49%"/>

## 🖥 Software requirements

the PyGame library connected to this project in your IDE

## 🤌🏽 Contact

Данила Исмайлов - [GitHub](https://github.com/ismylvdya) - [Telegram](https://t.me/ismylvdya)
