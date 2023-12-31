import pytweening, pydantic, pygame, json, sys, os
from pydantic import BaseModel, DirectoryPath

# Imported global libs

from cctd.script.libs.towers import *

example_tower = TowerData(
    id="example_tower",
    name="Example",
    base_rarity=2,
    base_damage=1.0, base_cooldown=2.0, base_crit_chance=1.25, 
    base_crit_multiplier=5.0, base_fire_rate=2.0, base_projectile_speed=10.0,
    damage_multiplier=0.0, crit_multiplier=0.0, crit_chance_multiplier=0.0, 
    fire_rate_multiplier=0.0, cooldown_reduction_multiplier=0.0, projectile_speed_multiplier=0.0, 
    global_positive_multiplier=0.0, global_negative_multiplier=0.0, current_buffs=[], current_debuffs=[]
)




def write_to_json(tower_data):
    tower_data_dict = tower_data.model_dump()
    file_path = f"cctd/towers/{tower_data_dict['id']}"
    
    f = open(f"{file_path}/tower_data.json" ,"w+")
    f.write(tower_data.model_dump_json())
    f.close
    
write_to_json(example_tower)