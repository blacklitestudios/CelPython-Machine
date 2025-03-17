import math

raw = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^{}/#_*':,@~|"
cheatsheet = {}
for i in range(0,84):
	cheatsheet[i] = raw[i]

reverse_cheatsheet = {}
for k, v in zip(cheatsheet.keys(), cheatsheet.values()):
	reverse_cheatsheet[v]=k


def base84(origvalue):
	result = ""
	iter = 0
	neg = False
	if origvalue == 0: 
		return '0'
	elif origvalue < 0: 
		origvalue = -origvalue
		neg = True
	while True:
		iter = iter + 1
		lowermult = 84**(iter-1)
		mult = 84**(iter)
		if lowermult > origvalue:
			break
		else:
			result = cheatsheet[math.floor(origvalue/lowermult)%84] + result
		

	if neg: 
		result = ">"+result
	return result

def unbase84(origvalue):
	neg = False
	if origvalue[0] == ">":
		neg = True
		origvalue = origvalue[1:len(origvalue)]
	
	result = 0
	iter = 0
	chars = len(origvalue)
	for i in range(chars,0,-1):
		iter = iter + 1
		mult = 84**(iter-1)
		#if not cheatsheet[string.sub(origvalue,i,i)] then error(string.sub(origvalue,i,i)) end
		result = result + reverse_cheatsheet[origvalue[i-1]] * mult

	return result*(-1 if neg else 1)

#print(base64.b64encode(zlib.compress("]<placeable<0]<placeable<0]<placeable<00000]<placeable<0]<placeable<8]<placeable<00000]<placeable<0]<placeable<0]<placeable<000Q0]<placeable<0]<placeable<0]<placeable<00000]<placeable<0]<placeable<0]<placeable<00000".encode())).decode())




