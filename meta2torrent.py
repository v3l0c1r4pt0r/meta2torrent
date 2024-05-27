#!/usr/bin/env python3
# Convert rtorrent's meta file to valid torrent file
import argparse
import datetime
import fastbencode
import sys

def meta2binary(obj, announces):
  move2infotree(obj)
  for announce in announces:
    add_announces(obj, announce.encode())
  extract_title(obj)
  add_metadata(obj)

def move2infotree(obj):
  # create info node
  if b'info' not in obj:
    obj[b'info'] = {}

  # there are 2 variants of torrent file
  if b'files' in obj:
    # one has files node containing file list
    obj[b'info'][b'files'] = obj[b'files']
    del obj[b'files']
  elif b'length' in obj:
    # the other has length defining size of the only file inside
    obj[b'info'][b'length'] = obj[b'length']
    del obj[b'length']
  else:
    raise Exception('Neither files nor length found in meta file. Unsupported.')

  # copy other nodes to info
  obj[b'info'][b'name'] = obj[b'name']
  obj[b'info'][b'piece length'] = obj[b'piece length']
  obj[b'info'][b'pieces'] = obj[b'pieces']

  # and delete from root node
  del obj[b'name']
  del obj[b'piece length']
  del obj[b'pieces']

def add_announces(obj, announce):
  if b'announce' not in obj:
    obj[b'announce'] = announce

  obj[b'announce-list'] = []
  obj[b'announce-list'].append([])
  obj[b'announce-list'][0].append(announce)

def extract_title(obj):
  obj[b'title'] = obj[b'info'][b'name']

def add_metadata(obj):
  obj[b'comment'] = b'Converted by meta2torrent.py from rtorrent meta file'
  obj[b'created by'] = b'meta2torrent.py'
  obj[b'locale'] = b'en'

  now = datetime.datetime.now()
  sec_from_epoch = now.strftime('%s')
  obj[b'creation date'] = int(sec_from_epoch)

def main():
  parser = argparse.ArgumentParser(prog='meta2torrent',
      description='Convert rtorrent\' meta file into valid torrent')
  parser.add_argument('meta', help='meta file to convert')
  parser.add_argument('torrent', help='torrent file to create')
  parser.add_argument('--announce', help='add to announce list', default=[],
      action='append')

  args = parser.parse_args()

  with open(args.meta, 'rb') as fp:
    binary = fp.read()

  obj = fastbencode.bdecode(binary)
  meta2binary(obj, args.announce)
  bencoded = fastbencode.bencode(obj)

  with open(args.torrent, 'bw') as fp:
    fp.write(bencoded)

if __name__ == '__main__':
  main()
