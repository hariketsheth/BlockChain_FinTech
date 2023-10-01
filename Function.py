n = 10
num1 = 0
num2 = 1
next_number = num2
count = 1

while count <= n:
	print(next_number, end=" ")
	count += 1
	num1, num2 = num2, next_number
	next_number = num1 + num2
print()
# Function for nth fibonacci
# number
FibArray = [0, 1]

def fibonacci(n):

	# Check is n is less
	# than 0
	if n < 0:
		print("Incorrect input")
		
	# Check is n is less
	# than len(FibArray)
	elif n < len(FibArray):
		return FibArray[n]
	else:	
		FibArray.append(fibonacci(n - 1) + fibonacci(n - 2))
		return FibArray[n]

# Driver Program
print(fibonacci(9))
