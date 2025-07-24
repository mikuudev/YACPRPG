import json
import os
# Cyberpunk Text-Based RPG Written in Python
# Dialogue
# Player Data
# Enemy Data	
# Place Data
# Weapons 

class Entity:
	def __init__(self, name: str, description: str, type: int, health: int, armor: int, inventory: list, power: int):
			self.name = name
			self.description = description
			self.type = type 
			self.health = health
			self.armor = armor 
			self.inventory = inventory
			self.power = power
            self.inventory.append(Weapon("Fists", 'The starting "weapon".', self, 1, 20))
            self.currently_equipped =self.inventory[0]
            
	
	def attack(self, other, weapon):
		damage = self.power * weapon.power 
		if damage > other.get_armor():
			other.set_health(other.health - damage)
			
	def set_health(self, new_health: int):
		self.health = max(0, new_health)
		

class Player(Entity):
	def __init__(self):
		super().__init__("Player","", 0, 100, 0, [], 10)
	
    @statickmethod 
    def take_choice() -> int:
        print("What would you like to do?")
        print("1. Attack\n2.Run")
        try:
            choice = int(input("Please enter your choice: "))
            while choice not in [1, 2]:
                choice = int(input("Please enter your choice: "))
        except:
            print("You have entered an incorrect value.")
            return take_choice()


    def fight(self, enemy: Entity) -> str: # This function returns "plr" if  he is victorious , "enemy", if, well, obvious. and "ran" if the player has ran away.
        while enemy.health > 0 && self.health > 0:
            choice = take_choice() # 1 = Attack, 2 = Run 
        
            match choice:
                case 1:
                    # attack logic 
                    self.attack(enemy, self.currently_equipped)
                case 2: 
                    # run logic
class Item:
	def __init__(self, name: str, description: str, owner: Entity):
		self.name = name 
		self.description = description
		self.owner = owner 
	

            


class Weapon(Item):
	def __init__(self, name: str, description: str, owner: Entity, power: int, critchance: int):
		super().__init__(name, description, owner)
		self.power = power 
		self.critchance = critchance # In percent 
	
	

		

class Scene:
	def __init__(self, name: str, description: str, ndoors: int, enemies: list[Entity], connections: list["Scene"]):
		self.name = name 
		self.description = description
		self.ndoors = ndoors 
		self.enemies = enemies
		self.connections = connections
		
	def __str__(self):
		return f"Location: {self.name}\nDescription: {self.description}\nDoor count: {self.ndoors}\nEnemy count: {len(self.enemies)}"
		
	@staticmethod
	def load_scene_from_json(filepath):
		with open(filepath, "r") as f:
				data = json.load(f)

		enemies = [Entity(**enemy_data) for enemy_data in data.get("enemies", [])]

		return Scene(
				name=data["name"],
				description=data["description"],
				ndoors=data["ndoors"],
				enemies=enemies,
				connections=[]
		) 
		 
		
class SceneError(Exception):
	pass

class Game:
	def __init__(self, starting_scene: Scene):
		self.scene = starting_scene
		
	def update_scene(self, new_scene: Scene):
		if new_scene.get_name():
			self.scene = new_scene
		else:
			raise SceneError("new_scene.name is None.")
	def get_active_scene(self):
		    return self.scene
			
	def game_loop(self):
		print(get_active_scene())
		player = Player()
		if len(self.scene.enemies) > 0:
			for enemy in self.enemies:
				print("You encounter an enemy!")
				if enemy.name != None:
					print(f"They are called: {enemy.name}")
				if len(enemy.description) > 0:
					print(f"The description reads: {enemy.description}")
                
                player.fight(enemy)



game = Game(Scene.load_scene_from_json("scenes/corpostart.json"))
print(game.get_active_scene())
