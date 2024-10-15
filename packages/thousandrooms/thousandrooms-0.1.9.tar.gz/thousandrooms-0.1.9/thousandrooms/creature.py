from colored import Style, Fore, Back

from .utils import Utils

class Creature:
    def __init__(self, info):
        for i in info:
            setattr(self, i, info[i])

        self.calculateDam()

    def calculateDam(self):
        return f"{Style.DIM}({self.atk + 2}-{self.atk + (self.level * 2)}){Style.RESET}"

    def damage(self, value, type):
        damage = value
        try:
            if type in self.resist:
                damage = value // 2
        except KeyError:
            pass
        except AttributeError:
            pass
        try:
            if self.vulnerability == type:
                damage = value * 2
        except KeyError:
            pass
        except AttributeError:
            pass
        self.hp -= damage
        return damage
        
    def heal(self, value = 0):
        if value == 0:
            self.hp = self.maxHp
        else :
            self.hp = min(self.hp + value, self.maxHp)

    def processTick(self):
        for key, value in self.conditions.items():
            self.conditions[key] = value - 1
            if self.conditions[key] == 0:
                self.removeCondition(key)
            else:
                self.applyCondition(key)

    def addCondition(self, name, value):
        if name == "strength":
            self.atk += 10
        elif name == "weakness":
            self.atk -= 5

        self.conditions[name] = value + 1

    def removeCondition(self, name):
        try:
            del self.conditions[name]
            
            if name == "strength":
                self.atk -= 10
            elif name == "weakness":
                self.atk += 5
            elif name == "elementalAttack":
                self.setAttackType()
        except KeyError:
            pass

    def hasCondition(self, name):
        try:
            if self.conditions[name]:
                return True
        except KeyError:
            return False

    def applyCondition(self, name):
        return

    def clearConditions(self):
        keys = []
        for key, value in self.conditions.items():
            keys.append(key)
        for key in keys:
            self.removeCondition(key)
    