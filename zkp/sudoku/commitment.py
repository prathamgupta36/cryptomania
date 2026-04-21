import json
import hashlib
import secrets

'''
Graph coloring commitment with sha256.
Format:
1. Commitment: hash hexdigest
2. Reveal: json dict with fields:
    - vertex index
    - vertex color
    - nonce
    - commitment (same as in graph) 
'''

# commit format
def commit_vertex(color, nonce=None):
    if nonce is None:
        nonce = secrets.randbelow(int(1e9))

    data = f'{color}|{nonce}|++'.encode()
    hash = hashlib.sha256(data).hexdigest()
    return hash

# reveal format
def reveal_vertex(idx, color, nonce, commit ):
    d = {
        'idx': idx,
        'color': color,
        'nonce': nonce,
        'commit': commit
    }
    return json.dumps(d)


def verify_com(r):
    data = f"{r['color']}|{r['nonce']}|++".encode()
    return hashlib.sha256(data).hexdigest() == r['commit']


def parse_graph(string):
    vertex_list = json.loads(string)
    assert isinstance(vertex_list, list)
    assert len(vertex_list)==90
    return vertex_list


def parse_reveals(string):
    reveals = json.loads(string)
    assert isinstance(reveals, list)
    for r in reveals:
        try:
            r['idx'] = int(r['idx'])
            r['color'] = int(r['color'])
            r['nonce'] = int(r['nonce'])
            assert isinstance(r['commit'], str)
        except:
            assert False, "Incorect reveal format!"

    return reveals


