#'io/input/test/tender.txt'
global row_heads
row_heads = []

import sys
import os
sys.path.append('io/')

def temp(d):
    global row_heads

    with open(d) as data:
        i = 0
        for line in data:
            j = 0
            row = line.rstrip()
            id_start = j
            id_end = id_start
            for char in row:
                if i > 0:
                    if char == '|' and id_end == id_start:
                        id_end = j
                        row_heads.append(row[id_start:id_end])
                        print('{}:{}'.format(id_start, id_end))
                    j += 1
            i += 1

        #print('total char found: {}'.format(i))
        #print('total num_lines: {}'. format(num_lines))
        # end function //

def temp2(d):
    global row_heads

    with open(d) as data:
        i = 0                              # 25
        for line in data:
            row = line.rstrip()
            print(row[0:25]) # test
            i += 1

        #print('total char found: {}'.format(i))
        #print('total num_lines: {}'. format(num_lines))
        # end function //

'''
    doc = ''
    with open(d) as data:
        i = 0
        for line in data:
            line.rstrip()
            row_head = row[0]
            row_heads.append(row_head)
            # regex removes blank lines
            doc = doc + re.sub(r'^\s+$', '', row)
    return doc
    # end function //
'''
def main():
    print('row_heads before:', row_heads)

    print('\nrun function...\n')
    temp('io/input/test/tender.txt')

    print('row_heads after:', row_heads)

    print('Done.')
    # end function //

if __name__ == '__main__' : main()
