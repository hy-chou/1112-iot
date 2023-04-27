from string import digits, ascii_letters, punctuation
from random import choices

while True:
    for n in range(8, 63):
        print(''.join(choices(digits + ascii_letters + punctuation, k=n)))
