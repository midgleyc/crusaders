#!/usr/bin/env python3
import json
import sys

class Template:
  def __init__(self):
    self.fields = dict()
  def to_wikitext(self):
    s = []
    s.append('{{Item Infobox')
    for field in self.fields:
      s.append(f'|{field} = {self.fields[field]}')
    s.append('}}')
    return '\n'.join(s)

def lookup_upgrade_by_id(j, a_id):
  upgrades = [x for x in j['upgrade_defines'] if x['id'] == a_id]
  return upgrades[0]

def lookup_ability_by_id(j, a_id):
  abilities = [x for x in j['ability_defines'] if x['id'] == a_id]
  return abilities[0]

def lookup_formation_ability_by_id(j, fa_id):
  fas = [x for x in j['formation_ability_defines'] if x['id'] == fa_id]
  return fas[0]

def lookup_effect_by_key(j, effect_key):
  effects = [x for x in j['effect_defines'] if x['effect_key'] == effect_key]
  return effects[0]

def effect_string_to_effect(j, effect_string, extra_fields={}):
  effect_name, *param_values = effect_string.split(',')
  effect = lookup_effect_by_key(j, effect_name)
  params = extra_fields
  param_names = effect["param_names"]
  if not param_names:
    param_names = "amount"
  for i, param_name in enumerate(param_names.split(',')):
    p_v = param_values[i]
    if ' ' in param_name:
      p_t, p_n = param_name.split()
      if p_t == 'int':
        p_v = int(p_v)
      elif p_t == 'str':
        p_v = str(p_v)
      else:
        raise AttributeError("Cannot parse parameter type " + param_name)
      params[p_n] = p_v
    else:
      params[param_name] = p_v
  if effect_name == "unlock_formation_ability":
    f_a = lookup_formation_ability_by_id(j, int(params['id']))
    base = effect_string_to_effect(j, f_a['effect'][0]['effect_string'], extra_fields)
    # TODO: formation_ability_desc is the right one
    extra = ''
    extra_reqs = f_a['requirements']
    if extra_reqs:
      for req in extra_reqs:
        requirement = req['requirement']
        if requirement == "hero_in_formation":
          hero = lookup_hero_by_id(j, req['target_hero_id'])['name']
          extra = f' when {hero} is also in the formation'
        elif requirement == "num_in_formation":
          amount = req.get('amount', None)
          if amount == 0:
            extra += ' when there are no '
          else:
            raise AttributeError('Cannot parse num_in_formation' + f_a)
          satisfies_tag_exp = req.get("satisfies_tag_exp", None)
          if not satisfies_tag_exp:
            raise AttributeError('Cannot parse num_in_formation' + f_a)
          if satisfies_tag_exp.startswith('!'):
            extra += f'non-{satisfies_tag_exp[1:].title()} Crusaders in the formation'
        elif requirement == 'fa_stacks':
          fa_stack_id = req['fa_id']
          fa_stack_name = lookup_formation_ability_by_id(j, fa_stack_id)['name']
          extra += f' when {fa_stack_name} has {req["amount"]} stacks'
        else:
          raise AttributeError('Unrecognised requirement: ' + requirement, f_a)
    return str(base) + extra
  s = effect['descriptions']['desc']
  for x in params:
    s = s.replace('$' + x, str(params[x]))
  for x in params:
    s = s.replace('$(' + x + ')', str(params[x]))
  if effect['owner'] == 'formation_ability':
    f_a = lookup_formation_ability_by_id(j, int(params['id']))
    hero = lookup_hero_by_id(j, f_a['hero_id'])['name']
    s = s.replace('$(formation_ability_owner_name id)', hero)
    s = s.replace('$(formation_ability_name id)', f_a['name'])
  if effect['owner'] == 'ability':
    a = lookup_ability_by_id(j, int(params['id']))
    s = s.replace('$(ability_name id)', a['name'])
  if effect['owner'] == 'upgrade':
    u = lookup_upgrade_by_id(j, int(params['id']))
    hero = lookup_hero_by_id(j, u['hero_id'])['name']
    s = s.replace('$(upgrade_hero id)', hero)
    s = s.replace('$(upgrade_name id)', u['name'])
  if '$' in s:
    return (s, ','.join([str((x, params[x])) for x in params]))
  else:
    return s

def lookup_hero_by_id(j, hero_id):
  heroes = [x for x in j['hero_defines'] if x['id'] == hero_id]
  return heroes[0]

def rarity_to_string(loot):
  return _rarity_to_string(loot['rarity'], loot['golden'])

def _rarity_to_string(num, golden):
  base = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'][num - 1]
  if golden:
    return f'Golden {base}'
  return base

def print_loot(fulljs, loot):
  name = loot['name']
  rarity = rarity_to_string(loot)
  url_template = 'https://crusaders-of-the-lost-idols.fandom.com/wiki/{}?action=edit'
  url_name = name
  if rarity.startswith('Golden'):
    url_name = f'{url_name} ({rarity})'
  url_name = url_name.replace(' ', '_')
  url = url_template.format(url_name)
  print('-'*10)
  print(url)
  print('\n')
  template = Template()
  template.fields['name'] = name
  image_name = name.replace("'", '').replace('-', '').title().replace(' ', '') + ('GL1' if rarity == 'Golden Legendary' else 'L1' if rarity == 'Legendary' else 'GE' if rarity == 'Golden Epic' else '')
  template.fields['image'] = f'{image_name}.png'
  template.fields['category'] = 'Gear'
  template.fields['rarity'] = rarity
  if loot['description']:
    template.fields['description'] = loot['description']
  effects = loot['effects']
  hero = lookup_hero_by_id(fulljs, loot['hero_id']).get('name', '')
  extra_effect_fields = {'target': hero}
  template.fields['effect'] = effect_string_to_effect(fulljs, effects[0]['effect_string'], extra_effect_fields)
  if rarity.endswith('Legendary'):
    leg_effect = effects[1]
    extra_effect_fields['level_amount'] = leg_effect['base_amount']
    template.fields['legendary'] = effect_string_to_effect(fulljs, leg_effect['effect_string'], extra_effect_fields)
    template.fields['legendarybase'] = leg_effect['base_amount']
    if leg_effect.get('growth', None):
      b = int(leg_effect['base_amount'])
      f = leg_effect['factor']
      template.fields['lvl1'] = f'{b}|lvl2 = {b+f}|lvl3 = {b+2*f}|lvl4 = {b+3*f}|lvln = {"" if b==f else str(b-f) + " + "}n*{f}'
  template.fields['usedBy'] = lookup_hero_by_id(fulljs, loot['hero_id']).get('name', '')
  print(template.to_wikitext())

def main(requested_ids):
  requested_ids = list(map(int, requested_ids))
  with open('fulljs.json', 'r') as f:
    j = json.loads(f.read())
  loots = j['loot_defines']
  for loot in [x for x in loots if x['id'] in requested_ids]:
    print_loot(j, loot)

if __name__ == '__main__':
  main(sys.argv[1:])
