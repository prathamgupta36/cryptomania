from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

def check_poly(n, c, poly, mod):
    b0 = bytes_to_long(b'Session Cookie: {user: "admin", secret: "') << 80
    b1 = bytes_to_long(b'"}')
    m0 = b0 + b1    
    correct = [0]*4
    correct[0] = m0**3 - c
    correct[1] = 196608*(m0**2)
    correct[2] = 3*m0 << 32
    correct[3] = 1 << 48
    return poly == correct and mod == n