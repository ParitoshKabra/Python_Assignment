matrix = []
for i in range(5):
    row = []
    row = [int(x) for x in input().split(" ")]
    # print(row)
    matrix.append(row)
def abs(x):
    if x > 0:
        return x 
    else:
        return -x
    
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if matrix[i][j] == 1:
            print(abs(2-i)+abs(2-j))
            break