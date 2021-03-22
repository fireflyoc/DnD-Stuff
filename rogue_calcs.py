# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 13:11:05 2021

@author: Noah G
"""

import random


d20 = (1, 20)
d12 = (1, 12)
d8 = (1, 8)
d6 = (1, 6)
d4 = (1, 4)
d10 = (1, 10)

def roll(number, die, gwf = False):
    result = 0
    for i in range(number):
        num = random.randint(die[0], die[1])
        if gwf:
            if num == 1 or num == 2:
                num = random.randint(die[0], die[1])
        result += num
    return result

player = {
        'stat_mod': 5,
        'prof': 4,
        'sneak': 6,
        'num_atks':1
        }

def attack(aim, player, magic, number, die, ac, crit_mod=2, ss_level=0):
    damage = 0
    bonus_atk = player['stat_mod'] + player['prof'] + magic
    bonus_dmg = player['stat_mod'] + magic
    crit = False
    ss_die = ss_level - 2
    
    to_hit = random.randint(d20[0], d20[1])
    
    if aim:
        advantage = random.randint(d20[0], d20[1])
        if advantage > to_hit:
            to_hit = advantage
    
#    print('To Hit: ', to_hit, to_hit+bonus_atk)
    n = number
    if to_hit == 20:
        n = crit_mod * number
        ss_die *= crit_mod
        crit = True
#        print('CRIT')
    
    if to_hit + bonus_atk >= ac:
        damage += roll(n, die) + bonus_dmg + roll(ss_die, d8)
#        print('HIT: Damage:', result)
#    else:
#        print('MISS')
    return damage, crit

def turn(number, die, ac, player, ba_atk, magic, aim, ally, sneak_die=d6, crit_mod=2, ss_level=0):
    damage = 0
    crits = 0
    misses = 0
    can_sneak = False
    if aim or ally:
        can_sneak = True
    num_attacks = player['num_atks']
#    First Attack
#    print('Atk 1')
    for i in range(player['num_atks']):
        dmg, crit = attack(aim, player, magic, number, die, ac, ss_level)
        damage += dmg
        if crit:
            crits +=1 
        if dmg == 0:
                misses += 1
#    Second Attack
#    print('Atk 2')
#    n, x = attack(reckless, gwm, player, magic, number, die, ac)
#    result += n
#    if x:
#        ba_atk = True
#        crits += 1
#    if n == 0:
#        misses += 1
    
    if ba_atk:
        num_attacks +=1
#        print('Bonus Action Attack')
        dmg, x = attack(aim, player, magic, number, die, ac)
        damage += dmg
        if x:
            crits += 1
        if dmg == 0:
            misses += 1
#    Sneak Attack
    if damage and can_sneak:
        num = player['sneak']
        if crits > 0:
            num *= crit_mod
        damage += roll(num, sneak_die)
    
    return damage, crits, num_attacks, misses

target_ac = 15
rounds = 1000000

#No Ally to trigger Sneak Attack
rapier = [0, 'Rapier BA Atk', 0 ,0, 0]
nilas = [0, 'Nila\'s BA Atk', 0 ,0, 0]
kwegra = [0, 'Kwegra BA Atk', 0 ,0, 0]

rapier_aim = [0, 'Rapier BA Aim', 0 ,0, 0]
nilas_aim = [0, 'Nila\'s BA Aim', 0 ,0, 0]
kwegra_aim = [0, 'Kwegra BA Aim', 0 ,0, 0]

#Ally assumes BA Attack
rapier_ally = [0, 'Rapier BA Ally', 0 ,0, 0]
nilas_ally = [0, 'Nila\'s BA Ally', 0 ,0, 0]
kwegra_ally = [0, 'Kwegra BA Ally', 0 ,0, 0]

#Spells
nilas_ss5_ally = [0, 'Nilas SS 5th', 0 ,0, 0]
nilas_ss6_ally = [0, 'Nilas SS 6th', 0 ,0, 0]
nilas_tashas_ally = [0, 'Nilas Tashas', 0 ,0, 0]

nilas_ss5_aim = [0, 'Nilas SS 5th aim', 0 ,0, 0]
nilas_ss6_aim = [0, 'Nilas SS 6th aim', 0 ,0, 0]
nilas_tashas_aim = [0, 'Nilas Tashas aim', 0 ,0, 0]

for i in range(rounds):
    """
#    Normal Attacks
#    print('----------Normal Rapier-------')
    res = turn(1, d8, target_ac, player, True, 2, False, False)
    rapier[0] += res[0]
    rapier[2] += res[1]
    rapier[3] += res[2]
    rapier[4] += res[3]
    
#    print('----------Nila\'s Razor-------')
    res = turn(1, d4, target_ac, player, True, 2, False, False, d8, 4)
    nilas[0] += res[0]
    nilas[2] += res[1]
    nilas[3] += res[2]
    nilas[4] += res[3]
    
#    print('----------Kwegra-------')
    res = turn(1, d6, target_ac, player, True, 2, False, False)
    kwegra[0] += res[0]
    kwegra[2] += res[1]
    kwegra[3] += res[2]
    kwegra[4] += res[3]
    
#    print('----------Rapier Aim-------')
    res = turn(1, d8, target_ac, player, False, 2, True, False)
    rapier_aim[0] += res[0]
    rapier_aim[2] += res[1]
    rapier_aim[3] += res[2]
    rapier_aim[4] += res[3]
    
#    print('----------Nila\'s Razor Aim-------')
    res = turn(1, d4, target_ac, player, False, 2, True, False, d8, 4)
    nilas_aim[0] += res[0]
    nilas_aim[2] += res[1]
    nilas_aim[3] += res[2]
    nilas_aim[4] += res[3]
    
#    print('----------Kwegra Aim-------')
    res = turn(1, d6, target_ac, player, False, 2, True, False)
    kwegra_aim[0] += res[0]
    kwegra_aim[2] += res[1]
    kwegra_aim[3] += res[2]
    kwegra_aim[4] += res[3]

#    print('----------Rapier Ally-------')
    res = turn(1, d8, target_ac, player, True, 2, False, True)
    rapier_ally[0] += res[0]
    rapier_ally[2] += res[1]
    rapier_ally[3] += res[2]
    rapier_ally[4] += res[3]
    
#    print('----------Nila\'s Razor Ally-------')
    res = turn(1, d4, target_ac, player, True, 2, False, True, d8, 4)
    nilas_ally[0] += res[0]
    nilas_ally[2] += res[1]
    nilas_ally[3] += res[2]
    nilas_ally[4] += res[3]
    
#    print('----------Kwegra Ally-------')
    res = turn(1, d6, target_ac, player, True, 2, False, True)
    kwegra_ally[0] += res[0]
    kwegra_ally[2] += res[1]
    kwegra_ally[3] += res[2]
    kwegra_ally[4] += res[3]
    """
#    Nilas Spirit Shroud 5th Level Ally
    res = turn(1, d4, target_ac, player, True, 2, False, True, d8, 4, 5)
    nilas_ss5_ally[0] += res[0]
    nilas_ss5_ally[2] += res[1]
    nilas_ss5_ally[3] += res[2]
    nilas_ss5_ally[4] += res[3]
    
#    Nilas Spirit Shroud6th Level Ally
    res = turn(1, d4, target_ac, player, True, 2, False, True, d8, 4, 6)
    nilas_ss6_ally[0] += res[0]
    nilas_ss6_ally[2] += res[1]
    nilas_ss6_ally[3] += res[2]
    nilas_ss6_ally[4] += res[3]
    
#    Nilas Tashas Otherworldly Guise Ally
    res = turn(2, d4, target_ac, player, True, 2, False, True, d8, 4)
    nilas_tashas_ally[0] += res[0]
    nilas_tashas_ally[2] += res[1]
    nilas_tashas_ally[3] += res[2]
    nilas_tashas_ally[4] += res[3]
    
#    Nilas Spirit Shroud 5th Level Aim
    res = turn(1, d4, target_ac, player, False, 2, True, True, d8, 4, 5)
    nilas_ss5_aim[0] += res[0]
    nilas_ss5_aim[2] += res[1]
    nilas_ss5_aim[3] += res[2]
    nilas_ss5_aim[4] += res[3]
    
#    Nilas Spirit Shroud6th Level Aim
    res = turn(1, d4, target_ac, player, False, 2, True, True, d8, 4, 6)
    nilas_ss6_aim[0] += res[0]
    nilas_ss6_aim[2] += res[1]
    nilas_ss6_aim[3] += res[2]
    nilas_ss6_aim[4] += res[3]
    
#    Nilas Tashas Otherworldly Guise Aim
    res = turn(2, d4, target_ac, player, False, 2, True, True, d8, 4)
    nilas_tashas_aim[0] += res[0]
    nilas_tashas_aim[2] += res[1]
    nilas_tashas_aim[3] += res[2]
    nilas_tashas_aim[4] += res[3]
    
    
res = [nilas_ss5_ally, nilas_ss6_ally, nilas_tashas_ally, nilas_ss5_aim, nilas_ss6_aim, nilas_tashas_aim]
res.sort(key=lambda x: x[0])

print('-----------------RESULTS-------------')
print('Weapon\t\t', 'DPR\t', 'Crit Rate', 'Miss Rate')
for result in res:
    print(result[1] + ':', round(result[0]/rounds, 4), round(result[2]/result[3], 4), round(result[4]/result[3], 4), sep = '\t')
