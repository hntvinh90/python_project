with open('nei.txt', 'w') as f:
    f.write('[')
    for i in range(81):
        f.write('[')
        x = i % 9
        y = i // 9
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (abs(i)!=abs(j) and x+i>=0 and x+i<9 and
                    y+j>=0 and y+j<9
                ):
                    f.write(str((y+j)*9 + x+i)+', ')
        f.write('],\n')
    f.write(']')