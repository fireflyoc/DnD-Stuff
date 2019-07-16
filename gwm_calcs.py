# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 15:53:16 2019

@author: Noah G
"""

import random

rounds = 1000000

d20 = (1, 20)
d12 = (1, 12)
d6 = (1,6)
d10 = (1, 10)

def roll(number, die, gwf = False):
    result = 0
    for i in range(number):
        num = random.randint(die[0], die[1])
        if gwf:
            if num == 1:
                num = random.randint(die[0], die[1])
        result += num
    return result

player = {
        'str_mod': 4,
        'prof': 3,
        'rage': 2
        }

def attack(reckless, gwm, player, magic, number, die, ac):
    result = 0
    bonus_atk = player['str_mod'] + player['prof'] + magic
    bonus_dmg = player['str_mod'] + player['rage'] + magic
    ba_atk = False
    
    to_hit = random.randint(d20[0], d20[1])
    
    if reckless:
        advantage = random.randint(d20[0], d20[1])
        if advantage > to_hit:
            to_hit = advantage
    
    if gwm:
        bonus_atk -= 5
        bonus_dmg += 10
#    print('To Hit: ', to_hit, to_hit+bonus_atk)
    n = 1
    if to_hit == 20:
        n = 2
        ba_atk = True
#        print('CRIT')
    
    if to_hit + bonus_atk >= ac:
        result += roll(n*number, die) + bonus_dmg
#        print('HIT: Damage:', result)
#    else:
#        print('MISS')
    return result, ba_atk

def turn(number, die, ac, player, gwm, magic, reckless):
    result = 0
    crits = 0
    misses = 0
    num_attacks = 2
#    First Attack
    ba_atk = False
#    print('Atk 1')
    n, x = attack(reckless, gwm, player, magic, number, die, ac)
    result += n
    if x:
        ba_atk = True
        crits +=1
    if n == 0:
        misses += 1
#    Second Attack
#    print('Atk 2')
    n, x = attack(reckless, gwm, player, magic, number, die, ac)
    result += n
    if x:
        ba_atk = True
        crits += 1
    if n == 0:
        misses += 1
    
    if ba_atk:
        num_attacks +=1
#        print('Bonus Action Attack')
        n, x = attack(reckless, gwm, player, magic, number, die, ac)
        result += n
        if x:
            crits += 1
        if n == 0:
            misses += 1
    
    return result, crits, num_attacks, misses
    
    
    
# Damage, Name, Num Crits, Num Attacks, Num Misses
axe= [0, 'Normal Axe', 0 ,0, 0]
maul= [0, 'Normal Maul', 0, 0, 0]
gwm_axe = [0, 'GWM Axe', 0, 0, 0]
gwm_maul = [0, 'GWM Maul', 0, 0, 0]
reck_axe = [0, 'Reckless Axe', 0, 0, 0]
reck_maul = [0, 'Reckless Maul', 0, 0, 0]
gwm_reck_axe = [0, 'Reck GWM Axe', 0, 0, 0]
gwm_reck_maul = [0, 'Reck GWM Maul', 0, 0, 0]
crits = 0
reck_crits = 0

str_mod = 4
prof = 3

rage = 2

target_ac = 14

for i in range(rounds):    
#    Normal Attacks
#    print('----------Axe Normal-------')
    res = turn(1, d10, target_ac, player, False, 1, False)
    axe[0] += res[0]
    axe[2] += res[1]
    axe[3] += res[2]
    axe[4] += res[3]
    
#    print('----------Maul Normal-------')
    res = turn(2, d6, target_ac, player, False, 0, False)
    maul[0] += res[0]
    maul[2] += res[1]
    maul[3] += res[2]
    maul[4] += res[3]
#    Great Weapon Master
#    print('----------Axe GWM-------')
    res = turn(1, d10, target_ac, player, True, 1, False)
    gwm_axe[0] += res[0]
    gwm_axe[2] += res[1]
    gwm_axe[3] += res[2]
    gwm_axe[4] += res[3]
#    print('----------Maul GWM-------')
    res = turn(2, d6, target_ac, player, True, 0, False)
    gwm_maul[0] += res[0]
    gwm_maul[2] += res[1]
    gwm_maul[3] += res[2]
    gwm_maul[4] += res[3]
    
#    Reckless
#    print('----------Axe Reckless-------')
    res = turn(1, d10, target_ac, player, False, 1, True)
    reck_axe[0] += res[0]
    reck_axe[2] += res[1]
    reck_axe[3] += res[2]
    reck_axe[4] += res[3]
#    print('----------Maul Reckless-------')
    res = turn(2, d6, target_ac, player, False, 0, True)
    reck_maul[0] += res[0]
    reck_maul[2] += res[1]
    reck_maul[3] += res[2]
    reck_maul[4] += res[3]
    
#    Reckless GWM
#    print('----------Axe GWM Reck-------')
    res = turn(1, d10, target_ac, player, True, 1, True)
    gwm_reck_axe[0] += res[0]
    gwm_reck_axe[2] += res[1]
    gwm_reck_axe[3] += res[2]
    gwm_reck_axe[4] += res[3]
#    print('----------Maul GWM Reck-------')
    res = turn(2, d6, target_ac, player, True, 0, True)
    gwm_reck_maul[0] += res[0]
    gwm_reck_maul[2] += res[1]
    gwm_reck_maul[3] += res[2]
    gwm_reck_maul[4] += res[3]
    
res = [axe, maul, gwm_axe, gwm_maul, reck_axe, reck_maul, gwm_reck_axe, gwm_reck_maul]
res.sort(key=lambda x: x[0])

print('-----------------RESULTS-------------')
print('Weapon\t\t', 'DPR\t', 'Crit Rate', 'Miss Rate')
for result in res:
    print(result[1] + ':', round(result[0]/rounds, 4), round(result[2]/result[3], 4), round(result[4]/result[3], 4), sep = '\t')
#print('Normal Crits:\t', crits/iters)
#print('Reckless Crits:\t', reck_crits/iters)