from string import digits, ascii_letters, punctuation
from random import choices

characters = digits + ascii_letters + punctuation

while True:
    for n in range(8, 63):
        print(''.join(choices(characters, k=n)))
