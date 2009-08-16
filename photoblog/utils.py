def find(l, func):
    for item in l:
        if func(item):
            return item
