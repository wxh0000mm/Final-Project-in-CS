import random
import sys

key = ''
key_length = sys.argv[1] if len(sys.argv) > 1 else 2042
for _ in range(key_length):
    key += str(random.randint(0,1))

print(key)
