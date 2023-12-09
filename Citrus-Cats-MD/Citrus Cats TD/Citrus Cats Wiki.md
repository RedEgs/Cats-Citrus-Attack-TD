Here you will find everything to-do with Citrus Cats. The project is open-source meaning you can view or edit the code as you so please. I'll post documentation every now and then on the various different libraries that I create to assist with Citrus cats' development. 

## Programmers guide to Citrus Cats TD






## <u>Index</u>
## <u>To-Do</u>

## Scenes
- [x] Tower selection screen  #WIP #NEEDS-POLISHING 
- [ ] Map selection scene
- [ ] Options

## Tower-system

- [ ] Implement actual towers not placeholder ones #WIP 
- [ ] Tower shop with placing #WIP 
- [ ] Damage types relative to towers #NEXT 
- [ ] Mouse preview actually working with selected tower etc.

## Enemy 
#WIP 

## GUI
- [ ] Do a whole redesign on EVERYTHING. #UI-REDESIGN
- [ ] Shop #WIP 
- [ ] Options 
- [ ] Button hover size bounce animation #NEXT
- [x] Text outlines and strokes (semi, due to broken thickness controls) #SEMI-FINISHED
	- [ ] Refactor strokes to be internal to text #NEEDS-TESTING

## Backend
- [ ] Implement cards system.
- [x] Fix tower data classes
- [x] Add vertical parameters for `calculate_index_spacing()` 
	- [x] Fix vertical parameters, past 5 elements.
- [ ] Refactor scene classes to pass in extra data if needed, make it optional
- [ ] Improve tower registry system #WIP
- [ ] Improve rarity system 
- [x] Refactor utils to make misc features 
- [ ] Make lib for damage calculations #NEXT
- [ ] Add tower and enemy loading at game startup #WIP #SEMI-FINISHED 
- [ ] Easy tower instancing #WIP 
- [ ] Tower logic refactor #WIP 
- [ ] Mouse preview refactor #UI-REDESIGN 
- [x] Fix clicking issues with tower selection cards
	- [x] Fix hovering in the list index too
- [ ] Make dedicated gui element and sprite group #WIP 
- [ ] Refactor all scenes with buttons and tweens to work properly
- [x] Add more parameters for tweens like, `self.start(reverse_on_finshed=bool)` #WIP  
- [x] Add a `wait(secs)` to utils for delaying in pygame 
- [x] Completely refactor menu scene to be organised and tidy
- [x] Refactor tweening on EVERYTHING (Use dataclasses) 
	- [x] Improve interaction between buttons and tweens #COULD-BE-IMPROVED 
	- [x] Try to get tweens to stop checking once they are finished 
	- [x] Make a tween manager to render all tweens in a group.
	- [x] Try to make tweens easier to use. #COULD-BE-IMPROVED
- [ ] ↑ Refactor buttons (specifically add group rendering, improve tweening) #WIP 
	- [ ] Fix buttons holding down when pressed but not hovered. #NEEDS-TESTING 
	- [x] Fix buttons not tweening back when they reach max progress
	- [x] Make a variant to buttons which allows for surfaces to be passed #SEMI-FINISHED 
## Other
- [ ] Write proper documentation for tweens and scenes because confised
- [ ] Finish writing the "programmers guide to citrus cats"