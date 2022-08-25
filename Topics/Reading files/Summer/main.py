#  write your code here 

my_file = open('./data/dataset/input.txt')
count = 0
for line in my_file:
    print(line)
    if line == 'summer\n':
        count = count + 1
print(count)
