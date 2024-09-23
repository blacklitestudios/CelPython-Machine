def translate(dic: dict, start, end):
    copy = dic.copy()
    temp = copy[start]
    copy[end] = temp
    del copy[start]
    return copy

a = {1: 5, 3: 3}
b = translate(a, 1, 2)
print(b)