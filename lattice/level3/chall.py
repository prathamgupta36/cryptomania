#!/usr/bin/exec-suid -- /usr/bin/python3
from helper import generate_dataset
import random

N = 2                   
M = random.randint(500_000, 1_000_000)           
CGH = 2.0               
UNIMOD_STEPS = 12       
DATASET_PATH = "lattice_dataset.json"

def progress_callback():
    state = {"last_bucket": -1}
    def cb(done: int, total: int):
        if total <= 0:
            return
        pct = int(done * 100 / total)
        bucket = pct // 5
        if bucket != state["last_bucket"]:
            print(f"[+] Generating lattices: {pct:3d}% ({done}/{total})", flush=True)
            state["last_bucket"] = bucket
    return cb

def submission_loop(secret_key: bytes):
    print("Enter the recovered 16-byte secret as hex (32 characters).") 
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            continue
        user_hex = line.lower().replace(" ", "")
        if user_hex.startswith("0x"):
            user_hex = user_hex[2:]
        if len(user_hex) != 32:
            print("Invalid: must be exactly 32 hex characters.")
            continue
        try:
            user_key = bytes.fromhex(user_hex)
        except Exception:
            print("Invalid hex encoding.")
            continue
        if user_key == secret_key:
            print("Great! you found the secret key.")
            print("Here is a flag for your troubles:")
            with open("/flag", "r") as f:
                print(f.read())
                break
        else:
            print("Incorrect. Try again.")

print("HQ has just sent out encrypted mission assignments.")
print("But before we could retrieve the decryption key, our rival division intercepted it.")
print("Trying to get back at us for the prank we pulled, they embedded the key inside")
print("a massive collection of lattices to make our job harder.")

print("\nThey did leave this message though:")
print("\"Every lattice carries the SAME 16-byte secret key, but only ONE lattice reveals it as its SHORTEST vector.\"\n")

cb = progress_callback()
dataset_path, secret_key, target_norm = generate_dataset(
    DATASET_PATH=DATASET_PATH,
    N=N,
    M=M,
    CGH=CGH,
    UNIMOD_STEPS=UNIMOD_STEPS,
    progress=cb,
)

print("\n=== Dataset Ready ===")
print(f"Lattices generated: {M}")
print(f"Dataset file:       {dataset_path}")
print(f"Target ||s||:       {target_norm:.6f}")
print("recover the 16-byte secret, and submit it below as 32 hex characters.\n")

submission_loop(secret_key)

