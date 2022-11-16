import random

class Shadowrun5_Dice():
    def __init__(self, dice_pool:int, edge:bool):
        self.dice_pool = dice_pool
        self.edge = edge

    #Set up the value modifiers
    def set_pool(self, numb:int):
        self.dice_pool = numb
    
    def get_pool(self):
        return self.dice_pool
    
    def set_edge(self, edge:bool):
        self.edge = edge
    
    def get_edge(self):
        return self.edge

    def basic_roll(self):
        #Rolls the number of dice set and records them to display back
        dice_pool = self.get_pool()
        edge = self.get_edge()
        results = []
        for _ in range(dice_pool):
            results.append(random.randint(1,6))
        if edge = True:
            results.append(self.check_explode(results,6))
            
        return results

    def count_hits(self, results,):
        successes = 0
        for die in results:
                if die >= 5:
                    successes += 1
                     
        return successes

    def check_glitch(self, results:list, pool:int):
        glitch = False
        glitch_count = 0
        for die in results:
            if die == 1:
                glitch_count += 1
        if glitch_count >= pool/2:
            glitch = True
        return glitch

    def check_explode(self, results:list, value:int):
        added_dice = 0
        added_results =[]
        for die in results:
            if die == value:
                added_dice += 1
        for _ in range(added_dice):
            added_die = random.randint(1,10)
            if added_die == value:
                added_dice += 1
            added_results.append(added_die)
        for die in added_results:
            results.append(die)



