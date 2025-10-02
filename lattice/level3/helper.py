#!/usr/bin/env python3
from typing import Any, Dict, Iterator, List, Sequence, Tuple, Optional
import json, math, random, secrets

__all__ = ["generate_dataset", "shortest_vector_and_key"]

Vector = Tuple[int, ...]
Matrix = List[List[int]]

def _chunk_sizes_for_n(n: int, total_bytes: int = 16) -> List[int]:
    base = total_bytes // n
    rem  = total_bytes % n
    return [base + (1 if i < rem else 0) for i in range(n)]

def _encode_centered_base256(key_bytes: bytes, n: int) -> Tuple[Tuple[int, ...], List[int]]:
    sizes = _chunk_sizes_for_n(n, len(key_bytes))
    s = []
    idx = 0
    for sz in sizes:
        acc = 0; p = 1
        for _ in range(sz):
            acc += (key_bytes[idx] - 128) * p
            p *= 256
            idx += 1
        s.append(acc)
    return tuple(s), sizes

def _decode_centered_base256(vec: Sequence[int], n: int) -> bytes:
    sizes = _chunk_sizes_for_n(n, 16)
    if len(vec) != n:
        raise ValueError("vector length must equal n")
    out = bytearray()
    for sj, sz in zip(vec, sizes):
        x = int(sj)
        for _ in range(sz):
            r = x % 256
            c = r if r <= 127 else r - 256
            b = c + 128
            out.append(b)
            x = (x - c) // 256
        if x != 0:
            raise ValueError("decode overflow")
    return bytes(out)

def _cols_to_rows(cols: Sequence[Sequence[int]]) -> Matrix:
    n = len(cols[0])
    return [[int(cols[j][i]) for j in range(len(cols))] for i in range(n)]

def _shortest_2d_lagrange(b1: Tuple[int,int], b2: Tuple[int,int]) -> Tuple[int,int]:
    def n2(v): return v[0]*v[0] + v[1]*v[1]
    a = (int(b1[0]), int(b1[1])); b = (int(b2[0]), int(b2[1]))
    while True:
        if n2(b) < n2(a):
            a, b = b, a
        denom = n2(a)
        if denom == 0: break
        mu = round((a[0]*b[0] + a[1]*b[1]) / float(denom))
        if mu == 0: break
        b = (b[0] - mu*a[0], b[1] - mu*a[1])
    return (int(a[0]), int(a[1]))

def _enumerate_shortest(B_rows: Matrix, coeff_bound: int) -> Optional[Vector]:
    import itertools
    n = len(B_rows)
    cols = [tuple(B_rows[i][j] for i in range(n)) for j in range(n)]
    best = None; best2 = None
    rng = range(-coeff_bound, coeff_bound + 1)
    for z in itertools.product(rng, repeat=n):
        if all(c == 0 for c in z): continue
        v = [0]*n
        for j, cj in enumerate(z):
            if cj == 0: continue
            col = cols[j]
            for i in range(n): v[i] += col[i]*cj
        s2 = sum(x*x for x in v)
        if best2 is None or s2 < best2:
            best2 = s2; best = tuple(int(x) for x in v)
    return best

def _recover_shortest(basis_cols: Sequence[Sequence[int]], target_norm_hint: Optional[float], enum_bound: int) -> Vector:
    n = len(basis_cols)
    rows = _cols_to_rows(basis_cols)
    if n == 1: return (int(rows[0][0]),)
    if n == 2:
        b1 = (rows[0][0], rows[1][0]); b2 = (rows[0][1], rows[1][1])
        return _shortest_2d_lagrange(b1, b2)
    col_norms = [math.sqrt(sum(rows[i][j]*rows[i][j] for i in range(n))) for j in range(n)]
    mn = max(min(col_norms), 1e-9)
    if target_norm_hint is None:
        bound = min(max(4, 8), enum_bound)
    else:
        est = int(math.ceil(float(target_norm_hint) / mn)) + 2
        bound = min(max(4, est), enum_bound)
    for b in (bound, min(bound*2, enum_bound)):
        cand = _enumerate_shortest(rows, b)
        if cand is not None: return cand
    cand = _enumerate_shortest(rows, enum_bound)
    if cand is None: raise RuntimeError("no short vector found")
    return cand

def _iter_dataset(dataset_path: str) -> Iterator[Tuple[Dict[str, Any], Dict[str, Any]]]:
    with open(dataset_path, "r") as f:
        first = f.read(1); f.seek(0)
        if first == "{":
            obj = json.load(f)
            meta = obj.get("meta", {})
            for entry in obj.get("lattices", []): yield meta, entry
            return
        meta = {}
        head = f.readline()
        try:
            hdr = json.loads(head)
            if isinstance(hdr, dict) and hdr.get("__meta__") is True:
                meta = hdr
            else:
                try: yield {}, json.loads(head)
                except Exception: pass
        except Exception:
            f.seek(0)
        for line in f:
            if line.strip(): yield meta, json.loads(line)

def _get_lattice_by_id(dataset_path: str, lattice_id: str) -> Dict[str, Any]:
    for _, entry in _iter_dataset(dataset_path):
        if entry.get("id") == lattice_id: return entry
    raise KeyError(f"lattice id not found: {lattice_id}")

def _unit_ball_volume(n: int) -> float:
    return math.pi**(n/2) / math.gamma(1 + n/2)

def _gh_target_det(norm_s: float, n: int, c: float) -> float:
    return (_unit_ball_volume(n) / c) * (norm_s ** n)

def _ident(n: int):
    I = [[0]*n for _ in range(n)]
    for i in range(n): I[i][i] = 1
    return I

def _matmul(A, B):
    r, k, c = len(A), len(A[0]), len(B[0])
    return [[sum(A[i][t]*B[t][j] for t in range(k)) for j in range(c)] for i in range(r)]

def _random_unimodular(n: int, steps: int, rng: random.Random):
    U = _ident(n)
    for _ in range(steps):
        op = rng.random()
        if op < 0.5:
            i, j = rng.randrange(n), rng.randrange(n)
            if i == j: continue
            k = rng.choice([-2, -1, 1, 2])
            for r in range(n): U[r][j] += k * U[r][i]
        elif op < 0.75:
            i, j = rng.sample(range(n), 2)
            for r in range(n): U[r][i], U[r][j] = U[r][j], U[r][i]
        else:
            j = rng.randrange(n)
            for r in range(n): U[r][j] = -U[r][j]
    return U


def _build_basis_with_det(n: int, s: Tuple[int, ...], D_target: float, rng: random.Random, unimod_steps: int):
    if n == 1:
        B0 = [[int(s[0] if s[0] != 0 else 1)]]
    elif n == 2:
        x, y = s
        u2 = (-y, x)
        det0 = x*x + y*y
        a = max(1, int(round(D_target / max(1, det0))))
        B0 = [[x, a*u2[0]],[y, a*u2[1]]]
    else:
        idx = next((i for i,v in enumerate(s) if v != 0), 0)
        rows = [r for r in range(n) if r != idx]
        a0 = max(1, int(round((D_target / max(1, abs(s[idx]))) ** (1.0/(n-1)))))
        cols = [list(s)]
        for r in rows:
            col = [0]*n; col[r] = a0
            cols.append(col)
        rng.shuffle(cols[1:])
        B0 = [[cols[j][i] for j in range(n)] for i in range(n)]
    U = _random_unimodular(n, unimod_steps, rng)
    B = _matmul(B0, U)
    return [[B[i][j] for i in range(n)] for j in range(n)]



def generate_dataset(
    DATASET_PATH,
    N,
    M,
    CGH,
    UNIMOD_STEPS,
    progress,
    ) -> Tuple[str, bytes, float]:
    
    rng = random.Random()
    key = secrets.token_bytes(16)
    s, _ = _encode_centered_base256(key, N)
    norm_s = math.sqrt(sum(int(x) * int(x) for x in s))
    D_star = _gh_target_det(norm_s, N, c=CGH)

    ids = [f"L{i:05d}" for i in range(M)]
    star = rng.randrange(M)
    GMIN, GMAX = 3.0, 8.0
    MAX_RESAMPLE = 8

    lattices = []
    for i, lid in enumerate(ids):
        if i == star:
           
            D = D_star
            Bcols = _build_basis_with_det(N, s, D, rng, 0)
        else:
            gap = rng.uniform(GMIN, GMAX)
            desired = norm_s / gap

            attempts = 0
            while True:
                attempts += 1
                ang = rng.random() * 2.0 * math.pi
                mag = max(1.0, rng.uniform(0.5, 1.5) * desired)
                cx = int(round(mag * math.cos(ang)))
                cy = int(round(mag * math.sin(ang)))
                if cx == 0 and cy == 0:
                    continue
                c2 = (cx, cy)
                c1 = (int(s[0]) - c2[0], int(s[1]) - c2[1])

                if (c2[0]*c2[0] + c2[1]*c2[1]) < (norm_s * norm_s):
                    Bcols = [[c1[0], c1[1]], [c2[0], c2[1]]]
                    break

                if attempts >= MAX_RESAMPLE:
                    Bcols = [[c1[0], c1[1]], [c2[0], c2[1]]]
                    break

            U = _random_unimodular(N, max(1, UNIMOD_STEPS//3), rng)
            A = [[Bcols[j][i] for j in range(N)] for i in range(N)]
            B = _matmul(A, U)
            Bcols = [[B[i][j] for i in range(N)] for j in range(N)]

        lattices.append({"id": lid, "n": N, "basis_cols": Bcols})
        if progress and (i % 100 == 0 or i == M - 1):
            progress(i + 1, M)

    dataset = {"meta": {"n": N, "m": M, "target_norm": float(norm_s)}, "lattices": lattices}
    with open(DATASET_PATH, "w") as f:
        json.dump(dataset, f)

    return DATASET_PATH, key, norm_s

# Use this to recover the key.
def shortest_vector_and_key(
    dataset_path: str,
    lattice_id: str,
    target_norm_hint: Optional[float] = None,
    enum_bound: int = 40,
    ) -> Tuple[Vector, bytes]:
    
    entry = _get_lattice_by_id(dataset_path, lattice_id)
    n = int(entry["n"])
    cols = entry["basis_cols"]
    s = _recover_shortest(cols, target_norm_hint=target_norm_hint, enum_bound=enum_bound)
    try:
        key = _decode_centered_base256(s, n)
        return s, key
    except Exception:
        s2 = tuple(-x for x in s)
        key = _decode_centered_base256(s2, n)
        return s2, key

