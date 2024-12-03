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
print(format_state(state))
print("\nRound Key [0]:")
print(format_state(key_instance.round_keys[0]))

# Initial AddRoundKey
print("\nAfter AddRoundKey (Step 0):")
print(format_state(aes.add_round_key_steps[0]))
print()

# Steps for each round
for round_number in range(1, 11):
    print(f"Step {round_number}: Start of Round {round_number}")
    print(format_state(aes.add_round_key_steps[round_number - 1]))

    print("\nAfter SubBytes:")
    print(format_state(aes.sub_bytes_steps[round_number - 1]))

    print("\nAfter ShiftRows:")
    print(format_state(aes.shift_rows_steps[round_number - 1]))

    if round_number < 10:  # No MixColumns in the final round
        print("\nAfter MixColumns:")
        print(format_state(aes.mix_columns_steps[round_number - 1]))

    print(f"\nRound Key [{round_number}]:")
    print(format_state(key_instance.round_keys[round_number]))

    print("\nAfter AddRoundKey:")
    print(format_state(aes.add_round_key_steps[round_number]))
    print()

# Final ciphertext
print("Final Ciphertext State:")
state = aes.add_round_key_steps[10]
print(format_state(state))