## TowerData

TowerData is the BaseModel for every and all towers within Citrus Cats. It contains all possible variables that any single tower can use. This includes technical variables like, `id` and "runtime" variables like `base_damage` and `damage_multiplier`.

```python
class TowerData(BaseModel):
    # Technical tower data
    id: str
    name: str

    # Base tower values
    base_damage: float
    base_cooldown: float
    base_damage: float
    base_crit_multiplier:sfloat
    base_crit_chance: float
    base_fire_rate: float
    base_cooldown: float
    base_projectile_speed: float

    # Variables values
    damage_multiplier: float
    crit_multiplier: float
    crit_chance_multiplier: float
    fire_rate_multiplier: float
    cooldown_reduction_multiplier: float
    projectile_speed_multiplier: float
    global_positive_multiplier: float
    global_negative_multiplier: float

    # Runtime values
    current_buffs: list
    current_debuffs: list
```


> [!note]- Pydantic BaseModel
>The TowerData method uses pydantic for its "BaseModel" inherited class.












## <u>Variables</u>

##### Technical tower data 
Id: The technical name that can be globally referred to when using/referring to a tower variation.
name: The formatted written name for the tower, used for text boxes, labels etc.
##### Base tower values 
base_damage: The flat damage that the tower will do, a tower cannot do less than this damage.
base_crit_multiplier: The amount that the base damage is multiplied by when a critical is landed.
base_crit_chance: How likely a critical is going to land on an enemy.
base_fire_rate: How quickly a tower can use its primary attacks like shooting or melee.
base_cooldown: The time inbetween events like reloading etc.
base_projectile_speed: Only applies if tower has projectiles of some kind.

##### Variables tower values
damage_multiplier: The amount the damage is multiplied by with buffs etc.
crit_multiplier: The amount extra that is multiplied to the critical_multiplier with buffs etc.
crit_chance_multiplier: The amount extra that is multiplied to the critical_multiplier with buffs etc.
fire_rate_multiplier: The amount extra that is multiplied to the base_fire_rate with buffs etc.
cooldown_reduction_multiplier: The amount the that is multiplied by to reduce cooldowns.
projectile_speed_multiplier: The amount the projectile speed is multiplied by with buffs etc.

global_positive_multiplier: The amount stats are buffed by positively. 
global_negative_multiplier: The amount stats are buffed by negatively. 

##### Run-time values
current_buffs: All the buffs that are applied to the tower
current_debuffs: All the debuffs that are applied to the tower


- Use a tower_data class
- a tower class that uses tower_data

