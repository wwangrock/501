s = [2, 3, 1, 4, 5]
a = sorted(range(len(s)), reverse = True, key=lambda k: s[k])
print(a)
