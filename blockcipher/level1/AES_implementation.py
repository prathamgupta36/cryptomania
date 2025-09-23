#!/usr/bin/exec-suid -- /usr/bin/python3
from Tables import *
import time

'''

Key Expansion function: 
- rot_word (rotate a 4 byte_word)
- sub_word (S_box substitution)
- rcon (rcon lookup function)
- xor bytes

'''
def xor_bytes(a, b):
    return bytes(i ^ j for i, j in zip(a, b))

def rot_word(word):
    if len(word) != 4:
        raise ValueError("Input must be exactly 4 bytes")
    return word[1:] + word[:1]

def sub_word(word):
    
    substituted_word = bytearray()
    
    for byte in word:
        substituted_word.append(S_box[byte]) 
    
    return bytes(substituted_word)

def rcon_lookup(i):
    return [rcon[i], 0x00, 0x00, 0x00]

def KeyExpansion(key, num_rounds):
    
    key_columns = [list(key[i:i + 4]) for i in range(0, len(key), 4)]
    iteration_size = len(key) // 4
        
    i = 1 
    

    while len(key_columns) < (num_rounds + 1) * 4:
        word = list(key_columns[-1])
        
        if len(key_columns) % iteration_size == 0:
            word.append(word.pop(0))
            word = [S_box[b] for b in word]
            word[0] ^= rcon[i]
            i += 1
        elif len(key) == 32 and len(key_columns) % iteration_size == 4:
            word = [S_box[b] for b in word]

        word = xor_bytes((word), (key_columns[-iteration_size]))
        key_columns.append((word))

    round_keys = [key_columns[4 * i: 4 * (i + 1)] for i in range(len(key_columns) // 4)]
    
    
    return round_keys


'''

inverse Key Expansion function: 
- xor
'''
def xor(state1, state2):
    state = b""
    for x,y in zip(state1, state2):
        state += bytes([y ^ x])
    return state

def inv_key_expansion(key, current_round):

    key_schedule = []
    key_schedule.append(key)

    for r in range(current_round, 0, -1):
      
        target_key = key_schedule[0]
        prev_key_round = [None] * 4

        prev_key_round[3] = xor(target_key[12:], target_key[8:12])
        prev_key_round[2] = xor(target_key[8:12], target_key[4:8])
        prev_key_round[1] = xor(target_key[4:8], target_key[:4])

        xored_rcon = xor(rcon_lookup(r), target_key[:4])

        prev_key_round[0] = xor(sub_word(rot_word(prev_key_round[3])), xored_rcon)

        prev_key_round = (prev_key_round[0] + prev_key_round[1] + prev_key_round[2] + prev_key_round[3])

        key_schedule.insert(0, prev_key_round)

    return key_schedule[0]
'''

AES Round Operations:

- Add Round Key 
- Sub bytes
- Shift Rows
- Mix columns

'''

'''

Normal Round Operations + inverses

'''
def add_round_key(state, round_key):
    
    if len(state) == 16:
        state = [state[i:i + 4] for i in range(0, len(state), 4)]
    
    if len(round_key) == 16:
        round_key = [round_key[i:i + 4] for i in range(0, len(round_key), 4)]
    
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    
    return state

def sub_bytes(state):
    
    for i in range(4):
        for j in range(4):
            byte = state[i][j]
            state[i][j] = S_box[byte]
    
    return state

def inv_sub_bytes(state):
    for i in range(4):
        for j in range(4):
            byte = state[i][j]
            state[i][j] = inv_sbox[byte]
    
    return state

def shift_rows(entry):
    for col in range(1, 4):  
        for _ in range(col):  
            temp = entry[0][col]
            for row in range(3):
                entry[row][col] = entry[row + 1][col]
            entry[3][col] = temp
    return entry

def inv_shift_rows(entry):
    for col in range(1, 4):  
        for _ in range(col):  
            temp = entry[3][col]
            for row in range(3, 0, -1):
                entry[row][col] = entry[row - 1][col]
            entry[0][col] = temp
    return entry

def xtime(byte):
    if byte & 0x80:  
        return (((byte << 1) ^ 0x1B) & 0xFF)
    else:
        return (byte << 1) & 0xFF

def mix_single_column(column):
    combined_xor  = column[0] ^ column[1] ^ column[2] ^ column[3]
    index = column[0]
    column[0] ^= combined_xor  ^ xtime(column[0] ^ column[1])
    column[1] ^= combined_xor  ^ xtime(column[1] ^ column[2])
    column[2] ^= combined_xor  ^ xtime(column[2] ^ column[3])
    column[3] ^= combined_xor  ^ xtime(column[3] ^ index)
    
    return column
    
    
def mix_columns(state): 
    for i in range(4):
        mix_single_column(state[i])

    return state

def inv_mix_columns(state):
    for i in range(4):
        index = xtime(xtime(state[i][0] ^ state[i][2]))
        rev_index = xtime(xtime(state[i][1] ^ state[i][3]))
        state[i][0] ^= index
        state[i][1] ^= rev_index
        state[i][2] ^= index
        state[i][3] ^= rev_index

    mix_columns(state)
    return state

'''

Encryption function for n rounds:

- text_to_state (converts plaintexts/ciphertexts into an AES state)
- printState (print the state for debugging)
'''

def text_to_state(text):
    
    if isinstance(text, str):
        text_bytes = text.encode('utf-8')
    else:
        text_bytes = text

    if len(text_bytes) < 16:
        text_bytes += b' ' * (16 - len(text_bytes))
    elif len(text_bytes) > 16:
        text_bytes = text_bytes[:16]

    state = [[0] * 4 for _ in range(4)]
    for i in range(16):
        row = i % 4
        col = i // 4
        state[row][col] = text_bytes[i]

    return state

def printState(state):
    for row in state:
        print(" ".join(f"{byte:02x}" for byte in row))


def encrypt(plaintext, key, num_rounds, verbose = False):
    
    state = text_to_state(plaintext)
    if verbose:
        print("Initial State (plaintext):")
        printState(state)
    
    round_keys = KeyExpansion(key, num_rounds)
    
    state = add_round_key(state, round_keys[0])
    if verbose:
        print("\nAfter AddRoundKey (Round 0):")
        printState(state)
    
    
    for round_num in range(1, num_rounds):
        # SubBytes
        state = sub_bytes(state)
        if verbose:
            print(f"\nAfter SubBytes (Round {round_num}):")
            printState(state)
        
        # ShiftRows
        state = shift_rows(state)
        if verbose:
            print(f"\nAfter ShiftRows (Round {round_num}):")
            printState(state)
        
        # MixColumns (only for rounds before the final round)
        if round_num < num_rounds:
            state = mix_columns(state)
            if verbose:
                print(f"\nAfter MixColumns (Round {round_num}):")
                printState(state)
        
        # AddRoundKey
        state = add_round_key(state, round_keys[round_num])
        if verbose:
            print(f"\nAfter AddRoundKey (Round {round_num}):")
            printState(state)
    
    # Final Round (without MixColumns)
    state = sub_bytes(state)
    if verbose:
        print(f"\nAfter SubBytes (Round {num_rounds}):")
        printState(state)
    
    state = shift_rows(state)
    if verbose:
        print(f"\nAfter ShiftRows (Round {num_rounds}):")
        printState(state)
    
    state = add_round_key(state, round_keys[-1])
    if verbose:
        print(f"\nAfter AddRoundKey (Round {num_rounds}):")
        printState(state)
    
    return bytes(sum(state, []))


'''
Decryption function for n rounds:

- state_to_text (debugging function)

'''
def state_to_text(state):
    text_bytes = [state[row][col] for col in range(4) for row in range(4)]
    text = ''.join(chr(byte) for byte in text_bytes)
    
    return text

def decrypt(ciphertext, key, num_rounds = 3, verbose=False):
    
    if isinstance(ciphertext, str):
        state = text_to_state(ciphertext)
        
    elif isinstance(ciphertext, bytes):
        state = [list(ciphertext[i:i+4]) for i in range(0, len(ciphertext), 4)]
    else:
        state = (ciphertext)
        
    if verbose:
        print("Initial State (ciphertext):")
        printState(state)
    
    
    round_keys = KeyExpansion(key, num_rounds)

    state = add_round_key(state, round_keys[-1])
    if verbose:
        print("\nAfter Initial AddRoundKey:")
        printState(state)
    

    state = inv_shift_rows(state)
    if verbose:
        print(f"\nAfter Initial Inverse ShiftRows:")
        printState(state)
    
    state = inv_sub_bytes(state)
    if verbose:
        print(f"\nAfter Initial Inverse SubBytes:")
        printState(state)
    
    
    for round_num in range(num_rounds - 1 , 0, -1):
        
        # AddRoundKey
        state = add_round_key(state, round_keys[round_num])
        if verbose:
            print(f"\nAfter AddRoundKey (Round {round_num}):")
            printState(state)
        
        # Inverse MixColumns (not in the last round)
        state = inv_mix_columns(state)
        if verbose:
            print(f"\nAfter Inverse MixColumns (Round {round_num}):")
            printState(state)
    
        # Inverse ShiftRows
        
        state = inv_shift_rows(state)
        
        if verbose:
            print(f"\nAfter Inverse ShiftRows (Round {round_num}):")
            printState(state)
        
        # Inverse SubBytes
        state = inv_sub_bytes(state)
        if verbose:
            print(f"\nAfter Inverse SubBytes (Round {round_num}):")
            printState(state)
        
    # Final AddRoundKey with the first round key
    state = add_round_key(state, round_keys[0])
    if verbose:
        print("\nAfter Final AddRoundKey (Round 0):")
        printState(state)
    
    return bytes(sum(state, []))

