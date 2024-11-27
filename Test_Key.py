from KEY import KEY  # Import the KEY class from the KEY module

# Prompt the user to input a 128-bit key
initial_key = input("Enter a 128-bit key (32 hexadecimal characters): ")

try:
    # Initialize the KEY class with the provided key
    aes_key = KEY(initial_key)

    # Print the round keys for all 11 rounds
    print("\nGenerated Round Keys:")
    for round_num in range(11):  # Include the initial key (round 0) and rounds 1-10
        round_key = aes_key.get_round_key(round_num)
        print(f"Round {round_num}: {round_key}")

except ValueError as e:
    print(f"Error: {e}")
