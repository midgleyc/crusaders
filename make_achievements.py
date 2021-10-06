#!/bin/env python3
import json
import re
import sys

def make_desc(x):
  patt = 'Season5Tier(\d)Reached(\d+)Areas>(\d+)'
  m = re.match(patt, x)
  if m:
    return f'Season 5: Reach area {m.group(2)} in {m.group(3)} Tier {m.group(1)} Dungeon objective{"s" if int(m.group(3)) > 1 else ""}'
  return ''

def print_acvs(fulljs, acv):
  print('|-')
  description = make_desc(acv['requirements'])
  if 'Tier 2' in description:
    print('|[[File:DungeonLevel2Ach.png|50px]]')
  elif 'Tier 3' in description:
    print('|[[File:DungeonLevel3Ach.png|50px]]')
  elif 'Tier 4' in description:
    print('|[[File:DungeonLevel4Ach.png|50px]]')
  print('|' + acv['name'])
  print('|' + description)
  incdps = acv['effect'].split(',')[-1]
  print('|{{IncDPS|All|' + incdps + '%}}')

def main(requested_ids):
  requested_ids = list(map(int, requested_ids))
  with open('fulljs.json', 'r') as f:
    j = json.loads(f.read())
  loots = j['achievement_defines']
  for loot in [x for x in loots if x['id'] in requested_ids]:
    print_acvs(j, loot)

if __name__ == '__main__':
  main(sys.argv[1:])
