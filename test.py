while True:
	a = int(input())
	b = float()
	
	for b in range(1,100):
		if a != 0 and b < 100:
			b = b + 1
			print(b)
		elif a == 0:
			break
		else:
			b = 0
			a = int(input())
