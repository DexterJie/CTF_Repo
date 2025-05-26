#!/usr/local/bin/python -u

from random import randrange

# blatantly stealing from @lydxn's mathjail challenge xd

description = 'Write an expression that takes a positive integer n, and returns 1 if n is\n' \
                  'prime, 0 otherwise (e.g. n = 37 should yield 1, but n = 35 should yield 0).\n'

print("I heard you're pretty good at this math stuff, so prove it.")
print(description)

prime_check = input("Your prime check: ")

# gl with this one ;)
if len(prime_check) > 40:
    print("Way too long, you don't need all that.")
    exit(1)

ALLOWED = 'n+-/%()' # wtf! no *
for char in prime_check:
    if char not in ALLOWED:
        print(f"Your {char!r} can't fool me!")
        exit(1)

try:
    func = eval(f'lambda n: {prime_check}', {}, {})
except Exception:
    print("Wow, your code sucks...")
    exit(1)

def isprime(n):
    if n < 2:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

# make sure your solution is memory efficient :)
START = 100_000_000
END   = 1_000_000_000
TESTS = 100

for _ in range(TESTS):
    rand_num = randrange(START, END)
    if int(isprime(rand_num)) != func(rand_num):
        print("I knew you weren't worthy.")
        exit(1)

print("How???")

try:
    from secret import flag
except:
    flag = "fake{fake_flag}"

print(flag)