import random
from math import comb
from commitment import *
import sys


FLAG = open('/flag', 'r').read().strip()

'''
set up sudoky
'''

def set_cartesian(A, B):
    return {(a,b) for a in A for b in B}

def rc_to_idx(r,c):
    return r*9+c

edges = set()
# row constraints
for r in range(9):
    edges |= {(rc_to_idx(r,c1), rc_to_idx(r,c2)) for c1 in range(9) for c2 in range(9) if c1!=c2}
# col constraints
for c in range(9):
    edges |= {(rc_to_idx(r1, c), rc_to_idx(r2, c)) for r1 in range(9) for r2 in range(9) if r1!=r2}
# subgrid constraints
for r in range(1, 9, 3):
    for c in range(1, 9, 3):
        subgrid = {(rc_to_idx(r+d1, c+d2)) for d1,d2 in set_cartesian([-1,0,1], [-1,0,1])}
        edges |= set_cartesian(subgrid, subgrid)

edges |= set_cartesian(range(81,90), range(81,90)) # color clique
edges = {(a,b) for a,b in edges if a<b} # orient, remove duplicates, remove loops

'''
Initial game constraints
'''
d = {
    (0, 3): 2,
    (0, 5): 1,
    (3, 0): 1,
    (5, 0): 2,
    (3, 8): 2,
    (5, 8): 1,
    (8, 3): 1,
    (8, 5): 2
}
for (r,c), v in d.items():
    edges |= {(rc_to_idx(r,c), x) for x in range(81,90) if x-81 != v}

'''End initialization'''



def main():
    num_rounds = 10

    print(f'There are {num_rounds} rounds. In each round, a random edge constraint will be queried. You will be asked to commit your sudoku solve and verify each constraint in random order.')
    print(f'Input the commitment graph as a json list of strings (hash hexdigets of vertex commitments). Input reveals as a json 2-list of dicts with fields: idx, color, commit, nonce.\n')

    for _round in range(num_rounds):
        print(f'Round {_round}...')

        edge_list = list(edges)
        random.shuffle(edge_list)

        for x, y in edge_list:
            print('Enter the committed graph of 90 vertices as a json list of strings (hash hexdigests);')
            G = parse_graph(input())

            print(f'Reveal vertices ({x}), ({y}) as a json list of 2 reveal dicts;')
            reveals = parse_reveals(input())

            rx, ry = reveals
            assert rx['idx'] == x and ry['idx'] == y, 'Incorrect vertices!'
            assert rx['commit'] == G[x] and ry['commit'] == G[y], 'Commitment mismatch!'
            assert rx['color'] in range(1,10) and ry['color'] in range(1,10), 'Color not in [1,9]!'
            assert verify_com(rx), f'Verification failed: ({x}) !'
            assert verify_com(ry), f'Verification failed: ({y}) !'
            assert rx['color'] != ry['color'], 'Constraint violation!'


    print('Not bad, I might actually believe youve solved it...')
    print(FLAG)






