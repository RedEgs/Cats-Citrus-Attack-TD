Here you will find everything to-do with Citrus Cats. The project is open-source meaning you can view or edit the code as you so please. I'll post documentation every now and then on the various different libraries that I create to assist with Citrus cats' development. 
## <u>Index</u>
## [[Gameplay]]

## <u>To-Do</u>

## Scenes
- [x] Tower selection screen  #WIP #SEMI-FINISHED 
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
- [ ] Shop #WIP 
- [ ] Options 
- [ ] Button hover size bounce animation #NEXT
- [x] Text outlines and strokes (semi, due to broken thickness controls) #SEMI-FINISHED

## Backend
- [x] Add vertical parameters for `calculate_index_spacing()` 
	- [ ] Fix vertical parameters, past 5 elements.
- [ ] Refactor scene classes to pass in extra data if needed, make it optional
- [ ] Improve tower registry system #WIP
- [ ] Improve rarity system 
- [ ] Refactor utils to make misc features #WIP
- [ ] Make lib for damage calculations #NEXT
- [ ] Add tower and enemy loading at game startup #WIP 
- [ ] Easy tower instancing #WIP 
- [ ] Tower logic refactor #WIP 
- [ ] Mouse preview refactor
- [x] Refactor tweening on EVERYTHING (Use dataclasses)
- [ ] ↑ Refactor buttons (specifically add group rendering, improve tweening) #WIP 
	- [ ] Fix buttons holding down when pressed but not hovered.
	- [ ] Make a variant to buttons which allows for surfaces to be passed directly