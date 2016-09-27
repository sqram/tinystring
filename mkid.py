# Random ID generator
# Python version of https://github.com/sqram/mkid

import random

def mkid(min_length=None, max_length=None, alphabet=None, cannot_be=None, cannot_start_with=None ):
  min_length = min_length if min_length else 1
  max_length = max_length if max_length else 8
  alphabet = alphabet if alphabet else 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!&~-+_'
  cannot_be = cannot_be if cannot_be else []
  cannot_start_with = cannot_be if cannot_start_with else ''

  def _generate_id():
    random_length = random.randrange(min_length, max_length+1)
    id = ''.join(random.sample(alphabet, random_length))
    if id[0] in cannot_start_with or id in cannot_be:
      return _generate_id()
    else:
      return id

  return _generate_id()

