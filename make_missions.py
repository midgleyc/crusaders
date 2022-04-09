#!/bin/env python3
from collections import Counter
import json
import re
import sys

def make_title(tag):
  if tag == 'dps': return 'DPS'
  return tag.title()

def make_tags(tags):
  tags = Counter(tags)
  for race, count in tags.items():
    print(str(count) + ' {{MissionTag|' + race + '}} ' + make_title(race) + '<br/>')

def make_tags_table(tags):
  for race in tags:
    print('{{MissionTag|' + race + '}}', end='')

def print_mission_summary(j, loot):
  print(make_tags(loot['required_tags']))
  print('--')
  print(make_tags_table(loot['required_tags']))

def main(requested_ids):
  requested_ids = list(map(int, requested_ids))
  with open('fulljs.json', 'r') as f:
    j = json.loads(f.read())
  loots = j['mission_defines']
  for loot in [x for x in loots if x['id'] in requested_ids]:
    print_mission_summary(j, loot)

if __name__ == '__main__':
  main(sys.argv[1:])
