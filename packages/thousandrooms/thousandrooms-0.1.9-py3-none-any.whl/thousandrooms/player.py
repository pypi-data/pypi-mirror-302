import random
import copy

from colored import Style, Fore, Back

from .creature import Creature
from .item import Item
from .utils import Utils
from .item_list import ItemList

class Player(Creature):
    def __init__(self, name, saveInfo = None):
        self.level = 1
        self.xp = 0
        self.gp = 0
        self.hp = 10
        self.maxHp = 10
        self.ac = 10
        self.atk = 1
        self.atkType = "blunt"
        self.history = {
            "rest": 0,
            "risky_win": 0,
            "reckless": 0,
            "run_away": 0,
            "kills": 0,
            "buy_item": 0,
            "sell_item": 0,
            "dismantle_item": 0,
            "craft_item": 0,
            "dmg_done": 0,
            "dmg_taken": 0,
            "epitaph": "Still exploring..."
        }
        self.name = name
        self.nextLevel = 1000
        self.items = []
        self.arrows = 0
        self.tools = 0
        self.wood = 0
        self.metal = 0
        self.skills = []
        self.innateAbilities = {}
        self.abilities = {}
        self.conditions = {}
        self.resist = []
        self.monsterLore = {}
        self.hasIdol = False
        
        if saveInfo:
            Creature.__init__(self, saveInfo)

    def loadItems(self, itemData):
        self.items = []
        for data in itemData:
            self.items.append(Item(0, data))

    def addGold(self, value):
        self.gp += value
        
    def removeGold(self, value):
        self.gp -= value

    def addItem(self, item):
        # auto-equip item if no item of this type is equipped
        kind = item.kind
        if kind == "usable":
            found = False
            for invItem in self.items:
                if invItem.id == item.id:
                    found = True
                    invItem.stack += 1
            if not found:
                self.items.append(item)
        else:
            found = False
            for invItem in self.items:
                if invItem.kind == kind:
                    found = True
            if not found:
                item.equipped = True
            self.items.append(item)
            self.applyItems()
        
    def removeItem(self, item):
        if item.kind == "usable" and item.stack > 1:
            item.stack -= 1
        else:
            self.items.remove(item)
        if item.kind != "usable":
            self.applyItems()
        
    def equipItem(self, newItem):
        for invItem in self.items:
            if invItem.kind == newItem.kind and invItem.equipped:
                invItem.equipped = False
        newItem.equipped = True

        self.applyItems()
        
    def unequipItem(self, kind):
        for invItem in self.items:
            if invItem.kind == kind and invItem.equipped:
                invItem.equipped = False
        self.applyItems()
        
    def applyItems(self):
        self.atk = (self.level + 1) // 2
        self.ac = 10
        self.abilities = copy.copy(self.innateAbilities)
        self.resist = []
        self.atkType = "blunt"

        for item in self.items:
            if item.equipped:
                if item.atk:
                    self.atk += item.atk
                if item.ac:
                    self.ac += item.ac
                if item.kind == "weapon" and not self.hasCondition("elementalAttack"):
                    self.atkType = item.type
                if item.ability:
                    if "resist_" in item.ability:
                        self.resist.append(item.ability.replace("resist_", ""))
                    else:
                        try: 
                            self.abilities[item.ability] += item.getAbilityLevel()
                        except KeyError:
                            self.abilities[item.ability] = item.getAbilityLevel()

        super().calculateDam()

    def setAttackType(self, name = ""):
        if name:
            self.atkType = name
        else:
            for item in self.items:
                if item.equipped and item.kind == "weapon":
                    self.atkType = item.type

    def checkLevelUp(self):
        if self.xp >= self.nextLevel:
            self.level += 1
            self.hp += 10
            self.maxHp += 10
            self.nextLevel += 1000 * self.level
            self.applyItems()
            return True
        else:
            return False

    def getAbilityLevel(self, ability):
        level = 0
        try:
            level = self.abilities[ability]
        except KeyError:
            pass
        return level

    def getAtkVerb(self):
        verbs = ItemList.atkVerb[self.atkType]
        return random.choice(verbs)
        
    def incrementHistory(self, field, value = 1):
        self.history[field] += value

    def drain(self, value):
        self.xp -= value
        if self.xp < 0:
            self.xp = 0
            
    def killedBy(self, monster, level):
        self.setEpitaph(f"Killed by a {monster.name} on level {level}.")

    def setEpitaph(self, text):
        self.history["epitaph"] = text

    def dismantleWeapon(weapon):
        self.wood += weapon.wood
        self.metal += weapon.metal
        self.incrementHistory("dismantle_item")
        return {
            "wood": weapon.wood,
            "metal": weapon.metal
        }

    def craftArrows(num):
        craftMax = min(self.wood, 10 - self.arrows)
        craftNum = min(num, craftMax)
        self.arrows += craftNum
        self.incrementHistory("craft_item", craftNum)
        return craftNum

    def craftTools(num):
        craftNum = min(num, self.metal)
        self.tools += craftNum
        self.incrementHistory("craft_item", craftNum)
        return craftNum

    def printStats(self):
        print(f"{Fore.MAGENTA}{Style.BOLD}{self.name}{Style.RESET}")

        hpColor = ""
        if self.hp / self.maxHp <= .25:
            hpColor = Fore.RED
        elif self.hp / self.maxHp <= .6:
            hpColor = Fore.YELLOW

        atkColor = ""
        weak = self.hasCondition("weakness")
        strong = self.hasCondition("strength")
        if weak and strong:
            atkColor = Fore.ORANGE
        elif weak:
            atkColor = Fore.RED
        elif strong:
            atkColor = Fore.YELLOW

        damColor = ""
        if self.hasCondition("nightshade"):
            damColor = Fore.GREEN

        stats = [
            {
                "Level": f"{self.level}",
                "XP": f"{self.xp} / {self.nextLevel}",
                "GP": f"{self.gp}"
            },
            {
                "HP": f"{hpColor}{self.hp}{Style.RESET} / {self.maxHp}",
                "ATK": f"{atkColor}{self.atk}{Style.RESET} {damColor}{Creature.calculateDam(self)}{Style.RESET}",
                "AC": f"{self.ac}",
            }
        ]
        Utils.printStats(stats)
        
        itemNames = []
        if len(self.items) == 0:
            itemNames = ["None"]
        for item in self.items:
            if item.equipped:
                itemNames.append(item.displayName)
        print("Equipped: " + ", ".join(itemNames))

    def getLoreRating(self, floor):
        maxLore = (floor + 1) * 12
        count = 0
        for key, m in self.monsterLore.items():
            if m["resist"]:
                count += 1
            if m["vulnerability"]:
                count += 1
            if m["special"]:
                count += 1
        return count / maxLore * 100

    def hasSeenMonster(self, monster):
        try:
            lore = self.monsterLore[monster.id]
            return True
        except KeyError:
            return False

    def printHistory(self, turns):
        print(f"{Fore.MAGENTA}{Style.BOLD}{self.name}{Style.RESET}")
        print(f"{Fore.RED}{self.history['epitaph']}{Style.RESET}\n")

        stats = [
            { 
                "Total Turns": f"{turns}",
                "Times Rested": f"{self.history['rest']}",
                "Battles Fled": f"{self.history['run_away']}"
            },
            {
                "Kills": f"{self.history['kills']}",
                "Reckless Attacks": f"{self.history['reckless']}",
                "Risky Wins": f"{self.history['risky_win']}" 
            },
            { 
                "Items Bought": f"{self.history['buy_item']}",
                "Items Sold": f"{self.history['sell_item']}",
                "Items Dismantled": f"{self.history['dismantle_item']}",
                "Items Crafted": f"{self.history['craft_item']}" 
            },
            { 
                "Damage Done": f"{self.history['dmg_done']}",
                "Damage Taken": f"{self.history['dmg_taken']}" 
            },
        ]
        Utils.printStats(stats)
