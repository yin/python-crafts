max = 30

for i in range(1, max + 1):
    out = ''
    if not i % 3:
        out += 'Fizz'
    if not i % 5:
        out += 'Buzz'
    if not out:
        out = str(i)
    print out
        
