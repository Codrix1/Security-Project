from KEY import KEY
from AES import AES
import numpy as np

# Example usage:
plaintext = "3243f6a8885a308d313198a2e0370734"  # Example plaintext block
initial_key = "2b7e151628aed2a6abf7158809cf4f3c"  # Example 128-bit key

key_instance = KEY(initial_key)
aes = AES(plaintext)
ciphertext = aes.encrypt_block(key_instance)

print("Ciphertext:", ciphertext)
print("\nSteps:")

# Helper function to format and print state as a matrix of hex values
def format_state(state):
    return "\n".join(" ".join(f"{x:02x}" for x in row) for row in state)

# Step 0: Initial state
print("Step 0: Input State:")
state = np.zeros((4, 4), dtype=int)
for i in range(16):
    state[i // 4, i % 4] = int(plaintext[i * 2:(i * 2) + 2], 16)
print([f"{state[i, j]:02x}" for i in range(4) for j in range(4)])  # State printed in hex
print("\nRound Key [0]:")
print(aes.Steps[0][1])

# Initial AddRoundKey step
print("\nAfter AddRoundKey (Step 0):")
print(aes.Steps[0][0])  # Hex list for AddRoundKey at Step 0
print()

# Steps for each round
for round_number in range(1, 11):
    print(f"Step {round_number}: Start of Round {round_number}")
    print(aes.Steps[round_number - 1][-1])  # State after previous round's AddRoundKey
    
    print("\nAfter SubBytes:")
    print(aes.Steps[round_number][0])  # SubBytes step
    
    print("\nAfter ShiftRows:")
    print(aes.Steps[round_number][1])  # ShiftRows step
    
    if round_number < 10:  # No MixColumns in the final round
        print("\nAfter MixColumns:")
        print(aes.Steps[round_number][2])  # MixColumns step

    print(f"\nRound Key [{round_number}]:")
    print(aes.Steps[round_number][3])
    
    print("\nAfter AddRoundKey:")
    print(aes.Steps[round_number][-1])  # AddRoundKey step
    print()

# Final ciphertext
print("Final Ciphertext State:")
print(aes.Steps[10][-1])  # Final AddRoundKey step in round 10
