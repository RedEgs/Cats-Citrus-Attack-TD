Here you will find everything to-do with Citrus Cats. The project is open-source meaning you can view or edit the code as you so please. I'll post documentation every now and then on the various different libraries that I create to assist with Citrus cats' development.  

esesf
# <u>To-Do  (Engine</u>)

- [ ] Make the engine independent of citrus cats
## GUI
- [x] Button hover size bounce animation
- [ ] Text outlines and strokes (semi, due to broken thickness controls) 
	- [ ] Refactor strokes to be internal to text
- [ ] Add support for CSS and HTML
- [ ] Add dropdown menus
## Backend
- [ ] Always figure out ways to optimise
- [ ] Make game loops less repetive ( Make use of globals & class methods) #WIP
- [ ] Create app options, see [[App Options]]
- [ ] Add vertical parameters for `calculate_index_spacing()` 
	- [ ] Fix vertical parameters, past 5 elements.
- [x] Refactor scene classes to pass in extra data if needed, make it optional
	- [ ] Document it cuz its kinda complicated to figure out
- [x] Refactor utils to make misc features 
- [x] Make dedicated gui element and sprite group 
- [x] Refactor all scenes with buttons and tweens to work properly
- [x] Add more parameters for tweens like, `self.start(reverse_on_finshed=bool)` #WIP  
- [x] Add a `wait(secs)` to utils for delaying in pygame 
- [x] Refactor tweening on EVERYTHING (Use dataclasses) 
	- [x] Improve interaction between buttons and tweens #COULD-BE-IMPROVED 
	- [x] Try to get tweens to stop checking once they are finished 
	- [x] Make a tween manager to render all tweens in a group.
	- [x] Try to make tweens easier to use. #COULD-BE-IMPROVED
- [x] ↑ Refactor buttons (specifically add group rendering, improve tweening) #WIP 
	- [x] Fix buttons holding down when pressed but not hovered. #NEEDS-TESTING 
	- [x] Fix surface buttons collision
	- [x] Fix buttons not tweening back when they reach max progress
	- [x] Make a variant to buttons which allows for surfaces to be passed #SEMI-FINISHED 
	- [ ] Try to remove the input delay
# <u>To-Do (In-Game) </u>


- [ ] Restart and Transition the game into the engine. 
## Scenes
- [ ] Implement all scenes #WIP
	- [ ] Tower selection screen  #WIP
	- [ ] Map selection scene #WIP
	- [ ] Options #WIP
	- [ ] Shop #WIP 
## GUI
- [ ] Do a whole redesign on EVERYTHING. #UI-REDESIGN #WIP
## Tower-system
- [ ] Implement actual towers not placeholder ones #WIP 
- [ ] Tower shop with placing #WIP 
- [ ] Damage types relative to towers #NEXT 
- [x] Mouse preview actually working with selected tower etc.
## Enemy 
- [ ] Make enemies usable, fix enemies basically #WIP
- [ ] Fix enemies rendering underneath the map
## Backend
- [ ] Make map editor
- [x] Make debug info
- [ ] Make difficulty selecting
- [ ] Implement cards system.
- [ ] Fix tower data classes
- [ ] Improve tower registry system #WIP
- [ ] Improve rarity system 
- [ ] Make element system
- [ ] Make upgrades system
- [ ] Make lib for damage calculations #NEXT
- [ ] Add tower and enemy loading at game startup 
- [ ] Easy tower instancing #WIP 
- [ ] Make easy tower instancing easier #WIP 
- [ ] Tower logic refactor #WIP 
- [ ] Mouse preview refactor #UI-REDESIGN 
- [ ] Fix clicking issues with tower selection cards
	- [ ] Fix hovering in the list index too
## Other
- [ ] Write proper documentation for tweens and scenes because confised
- [ ] Finish writing the "programmers guide to citrus cats"