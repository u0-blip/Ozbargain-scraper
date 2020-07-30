def y():
    for i in range(10):
        if i == 5:
            return 
        yield i

for i in y():
    print(i)