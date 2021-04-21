#!/usr/bin/env python3

import sys
import re

x=-31 # lower is righter
y=-30

def correct_viewbox(s):
  for index, line in enumerate(s):
    if line.startswith('<svg'):
      s[index] = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="256" height="256" viewBox="{x - 1.5} {y - 1.5} 64 64">\n'
      break

def add_clippath(s):
  for index, line in enumerate(s):
    match = re.match('^(\s*)<defs>', line)
    if match:
      s[index] = line.rstrip() + f'<clipPath id="clip"><rect x="{x}" y="{y}" width="61" height="61" /></clipPath>\n'
      break
  for index, line in reversed(list(enumerate(s))):
    match = re.match('^(\s*)<use([^>]+)xlink:href="([^"]+)"', line)
    if match:
      s[index] = f'{match.group(1)}<use{match.group(2)}xlink:href="{match.group(3)}" clip-path="url(#clip)"/>\n'
      break

def add_border(s):
  for index, line in reversed(list(enumerate(s[:]))):
    match = re.match('^(\s*)<use xlink:href="([^"]+)"', line)
    if match:
      indent = match.group(1)
      s.insert(index, indent + f'<rect x="{x}" y="{y}" width="61" height="61" stroke="none" fill="#73270B" />\n')
      s.insert(index + 2, indent + f'<rect x="{x}" y="{y}" width="61" height="61" stroke="#9A340E" stroke-width="1" fill="none" />\n')
      s.insert(index + 2, indent + f'<rect x="{x}" y="{y}" width="61" height="61" stroke="#331104" stroke-width="3" fill="none" />\n')
      break

def adjust_lines(s):
  correct_viewbox(s)
  add_clippath(s)
  add_border(s)

def main(filename):
  with open(filename, 'r') as f:
    s = f.readlines()
  adjust_lines(s)
  with open(filename, 'w') as f:
    f.writelines(s)

if __name__ == '__main__':
  main(sys.argv[1])
