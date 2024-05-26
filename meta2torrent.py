#!/usr/bin/env python3
# Convert rtorrent's meta file to valid torrent file
import fastbencode
import sys

def meta2binary(obj):
  move2infotree(obj)

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

def main():
  if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} meta-file torrent-file', file=sys.stderr)
    sys.exit(1)

  with open(sys.argv[1], 'rb') as fp:
    binary = fp.read()

  obj = fastbencode.bdecode(binary)
  meta2binary(obj)
  bencoded = fastbencode.bencode(obj)

  with open(sys.argv[2], 'bw') as fp:
    fp.write(bencoded)

if __name__ == '__main__':
  main()
