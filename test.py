from mkid import mkid

id = mkid(min_length=15, max_length=5,cannot_be = ['api', 'contact', 'about', 'login'])

print(id)