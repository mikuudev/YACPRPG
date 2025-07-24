import json
import os
import sys
import os
import time
# Cyberpunk Text-Based RPG Written in Python
# Dialogue
# Player Data
# Enemy Data	
# Place Data
# Weapons 


def clear_screen():
    if os.name == 'nt':  # windows
        os.system('cls')
    else:  # macOS and linux (posix)
        os.system('clear')

class Item:
	def __init__(self, name: str, description: str, owner):
		self.name = name 
		self.description = description
		self.owner = owner 
	

			


class Weapon(Item):
	def __init__(self, name: str, description: str, owner, power: int, critchance: int):
		super().__init__(name, description, owner)
		self.power = power 
		self.critchance = critchance # In percent 



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
			self.currently_equipped = self.inventory[0]
			
	def __str__(self):
		return f"{self.name} (HP: {self.health}, Armor: {self.armor})"

	def attack(self, other, weapon):
		damage = self.power * weapon.power
		modifier = None
		if damage >= other.armor:
			# damage breaks through armor
			leftover_damage = damage - other.armor
			if not other.armor == 0:
				modifier = "Ripped"

			other.armor = 0
			other.set_health(other.health - leftover_damage)
		else:
			# armor absorbs all damage
			other.armor -= damage

		return damage, modifier
			
	def set_health(self, new_health: int):
		self.health = max(0, new_health)
		

class Player(Entity):
	def __init__(self):
		super().__init__("Player","", 0, 100, 100, [], 20)
	
	def take_choice(self):
		print("What would you like to do?")
		print("1. Attack\n2. Run")
		try:
			choice = int(input("Please enter your choice: "))
			while choice not in [1, 2]:
				choice = int(input("Please enter your choice: "))
		except KeyboardInterrupt:
			sys.exit()
		except Exception as e:
			print("You have entered an incorrect value.")
			return self.take_choice()
		return choice

	def fight(self, enemy: Entity):
		while enemy.health > 0 and self.health > 0:
			clear_screen()
			print(f"--------\nFIGHT")
			print(f"{enemy.name}'s HP: {enemy.health}")
			print(f"{enemy.name}'s ARMOR: {enemy.armor}")
			print(f"{enemy.name}'s POWER: {enemy.power}")
			print(f"{enemy.name}'s WEAPON: {enemy.currently_equipped.name}")
			print(f"Your HP: {self.health}")
			print(f"Your ARMOR: {self.armor}")
			print(f"Your POWER: {self.power}")
			print(f"Your WEAPON: {self.currently_equipped.name}")
			print("--------")
	
			choice = self.take_choice()
			
			if choice == 1:
				playerdamage, modifier = self.attack(enemy, self.currently_equipped)
				print(f"You deal {playerdamage} damage to {enemy.name}!")
				if modifier == "Ripped":
					time.sleep(0.5)
					print("You broke through their armor!")
				time.sleep(2)
				if enemy.health <= 0:
					print("You defeated the enemy!")
					return "plr"
			elif choice == 2:
				print("You ran away...")
				return "ran"
			
			# Enemy attacks back
			enemydamage, modifier = enemy.attack(self, enemy.currently_equipped)
			print(f"{enemy.name} deals {enemydamage} damage to you!")
			if modifier == "Ripped":
				time.sleep(0.5)
				print("They broke through your armor!")
			time.sleep(2)
			if self.health <= 0:
				print("You died.")
				return "enemy"




		

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
		if new_scene.name:
			self.scene = new_scene
		else:
			raise SceneError("new_scene.name is None.")
	def get_active_scene(self):
			return self.scene
			
	def game_loop(self):
		clear_screen()
		print(self.get_active_scene())
		time.sleep(5)
		player = Player()
		if len(self.scene.enemies) > 0:
			for enemy in self.scene.enemies:
				print("You encounter an enemy!")
				time.sleep(2)
				if enemy.name != None:
					print(f"They are called: {enemy.name}")
					time.sleep(2)
				if len(enemy.description) > 0:
					print(f"The description reads: {enemy.description}")
					time.sleep(5)
				
				winner = player.fight(enemy)
				if winner == "plr":
					print("200 OK")



game = Game(Scene.load_scene_from_json("scenes/corpostart.json"))
game.game_loop()