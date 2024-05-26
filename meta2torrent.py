#!/usr/bin/env python3
# Convert rtorrent's meta file to valid torrent file
import fastbencode
import sys

def meta2binary(obj, announce):
  move2infotree(obj)
  add_announces(obj, announce.encode())

def move2infotree(obj):
  if b'info' not in obj:
    obj[b'info'] = {}

  obj[b'info'][b'files'] = obj[b'files']
  obj[b'info'][b'name'] = obj[b'name']
  obj[b'info'][b'piece length'] = obj[b'piece length']
  obj[b'info'][b'pieces'] = obj[b'pieces']

  del obj[b'files']
  del obj[b'name']
  del obj[b'piece length']
  del obj[b'pieces']

def add_announces(obj, announce):
  obj[b'announce'] = announce
  obj[b'announce-list'] = []
  obj[b'announce-list'].append([])
  obj[b'announce-list'][0].append(announce)

def main():
  if len(sys.argv) < 4:
    print(f'Usage: {sys.argv[0]} announce meta-file torrent-file', file=sys.stderr)
    sys.exit(1)

  with open(sys.argv[2], 'rb') as fp:
    binary = fp.read()

  obj = fastbencode.bdecode(binary)
  meta2binary(obj, sys.argv[1])
  bencoded = fastbencode.bencode(obj)

  with open(sys.argv[3], 'bw') as fp:
    fp.write(bencoded)

if __name__ == '__main__':
  main()
