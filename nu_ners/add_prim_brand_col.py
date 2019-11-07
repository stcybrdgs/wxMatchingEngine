#!/usr/bin/env python
# coding: utf8
"""
Thur, Nov 7, 2019
Stacy Bridges

Selects the primary brand for each record:
- if wBrand_all == '', primary brand == ''
- if wBrand_all count == 1, primary brand == wBrand_all
- if wBrand_all count > 1:
    - for each brand b in the wBrand_all field, count each time it occurs in the column
    - then, primary brand == max [b1_count, b2_count, ..., bn_count]
- if wBrand_prim column was previously populated, overwrite it each time new values
  are determined

"""
def main():

    # end program
    print('Done.')

if __name__ == '__main__' : main()
