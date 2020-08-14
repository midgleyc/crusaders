#!/usr/bin/env python3
from collections import defaultdict
from generate_equip_page import *

import json
import sys

class Item:
  def is_leg(self):
    return self.rarity.endswith('L')
  def make_link(self):
    if self.rarity == 'GE':
      return f'{self.name} (Golden Epic)|{self.name}'
    if self.rarity == 'GL':
      return f'{self.name} (Golden Legendary)|{self.name}'
    return self.name
  def effect_params(self):
    if self.is_leg():
      return self.effect + '||' + self.leg_effect
    return self.effect

class Slot:
  def __init__(self):
    self.items = []
    self.item_class = None

class Items:
  def __init__(self):
    self.slots = defaultdict(Slot)
  def to_wikitext(self):
    s = []
    s.append('{{Items subpage}}')
    s.append('')
    s.append('{{ItemT|top}}')
    for slot in self.slots.values():
      s.append(f'{{{{ItemT|class={slot.item_class}|row={len(slot.items)}|C|[[{slot.items[0].name}]]|{slot.items[0].effect_params()}}}}}')
      for item in slot.items[1:]:
        s.append(f'{{{{ItemT|{item.rarity}|[[{item.make_link()}]]|{item.effect_params()}}}}}')
      s.append('')
    s.append('{{ItemT|end}}')
    return '\n'.join(s)

def rarity_to_acronym(loot):
  return _rarity_to_acronym(loot['rarity'], loot['golden'])

def _rarity_to_acronym(num, golden):
  base = ['C', 'U', 'R', 'E', 'L'][num - 1]
  if golden:
    return f'G{base}'
  return base

def make_subpage(fulljs, loot):
  all_items = Items()
  for i in [1, 2, 3]:
    slot = all_items.slots[i]
    for item in [x for x in loot if x['slot_id'] == i]:
      item_to_add = Item()
      item_to_add.name = item['name']
      item_to_add.rarity = rarity_to_acronym(item)
      effect = item['effects'][0]['effect_string'].split(',')
      if effect[0] == 'buff_upgrade':
        upgrade = lookup_upgrade_by_id(fulljs, int(effect[-1]))['name']
        item_to_add.effect = f'effect|{upgrade}'
      elif effect[0] == 'buff_formation_ability':
        f_a = lookup_formation_ability_by_id(fulljs, int(effect[-1]))['name']
        item_to_add.effect = f'effect|{f_a}'
      else:
        raise AttributeError("Cannot parse effect " + ','.join(effect))
      if item_to_add.is_leg():
        item_to_add.leg_effect = 'YYY'
        pass # effect_to_string
      slot.items.append(item_to_add)
      if not slot.item_class:
        slot.item_class = item_to_add.name.split()[-1]
  print(all_items.to_wikitext())

def main(hero_id):
  with open('fulljs.json', 'r') as f:
    j = json.loads(f.read())
  loots = [x for x in j['loot_defines'] if x['hero_id'] == int(hero_id)]
  make_subpage(j, loots)

if __name__ == '__main__':
  main(sys.argv[1])
