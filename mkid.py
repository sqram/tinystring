# Random ID generator

import random

alphabet = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!&~-+_'

def mkid(min_length=1, max_length=8, alphabet=alphabet, cannot_be=[], cannot_start_with='' ):
  if min_length > max_length:
    min_length = max_length

  def _generate_id():
    random_length = random.randrange(min_length, max_length+1)
    id = ''.join(random.sample(alphabet, random_length))
    if id[0] in cannot_start_with or id in cannot_be:
      return _generate_id()
    else:
      return id

  return _generate_id()

