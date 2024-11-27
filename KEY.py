class KEY:
    """
    This class is responsible for generating the round keys 
    for AES encryption. It uses the initial key provided 
    to derive keys for 10 rounds.
    """

    def __init__(self, initial_key: str):
        """
        Initialize the KEY class with the initial key.

        Args:
            initial_key (str): A 128-bit key represented as a hexadecimal string.
        """
        if len(initial_key) != 32:  # 32 hex characters = 128 bits
            raise ValueError("Initial key must be a 128-bit hexadecimal string (32 characters).")
        self.initial_key = initial_key
        self.S_BOX = [
            [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
            [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
            [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
            [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
            [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
            [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
            [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
            [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
            [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
            [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
            [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
            [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
            [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
            [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
            [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
            [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
        ]
        self.RCON = [
            [0x01, 0x00, 0x00, 0x00],
            [0x02, 0x00, 0x00, 0x00],
            [0x04, 0x00, 0x00, 0x00],
            [0x08, 0x00, 0x00, 0x00],
            [0x10, 0x00, 0x00, 0x00],
            [0x20, 0x00, 0x00, 0x00],
            [0x40, 0x00, 0x00, 0x00],
            [0x80, 0x00, 0x00, 0x00],
            [0x1b, 0x00, 0x00, 0x00],
            [0x36, 0x00, 0x00, 0x00]
        ]
        self.round_keys = []  # To store the 10 round keys
        self.key_schedule()
        

    def hex_to_matrix(self, hex_string: str) -> list:
        """
        Convert a 128-bit hexadecimal string into a 4x4 matrix.

        Args:
            hex_string (str): A 128-bit hexadecimal string.

        Returns:
            list: A 4x4 matrix representing the key.
        """
        if len(hex_string) != 32:
            raise ValueError("Input must be a 128-bit hexadecimal string (32 characters).")
        
        matrix = []
        for row in range(4):  # AES uses 4 rows in the key schedule
            matrix.append([hex_string[i:i+2] for i in range(row * 8, (row + 1) * 8, 2)])
        return [list(row) for row in zip(*matrix)]


    def generate_round_key(self, previous_key: list, round_constant: list) -> list:
        """
        Generate a new round key from the previous key and round constant.

        Args:
            previous_key (list): A 4x4 matrix representing the previous key.
            round_constant (list): A list of 4 bytes representing the round constant.

        Returns:
            list: A 4x4 matrix representing the new round key.
        """
        last_column = [previous_key[row][3] for row in range(4)]
        rotated_column = last_column[1:] + last_column[:1]
        
        substituted_column = []
        for byte in rotated_column:
            row = int(byte[0], 16)
            col = int(byte[1], 16)
            # Retrieve the value from the S-Box
            sbox_value = self.S_BOX[row][col]

            # Convert the value to a hexadecimal string
            hex_value = hex(sbox_value)[2:]  # Remove the '0x' prefix

            # Ensure the hex value is two characters long (pad with '0' if necessary)
            if len(hex_value) == 1:
                hex_value = '0' + hex_value

            # Append the two-character hex string to the substituted_column list
            substituted_column.append(hex_value)
        
        # Initialize an empty list for the first column
        first_column = []

        # Loop through the 4 rows
        for i in range(4):
            # Convert substituted_column[i] from hex to integer
            substituted_value = int(substituted_column[i], 16)

            # Convert round_constant[i] from hex to integer
            round_constant_value = int(round_constant[i], 16)

            # Convert previous_key[i][0] (first column) from hex to integer
            previous_key_value = int(previous_key[i][0], 16)

            # Perform XOR on the three values
            xor_result = substituted_value ^ round_constant_value ^ previous_key_value

            # Convert the XOR result back to hex and strip the '0x' prefix
            hex_result = hex(xor_result)[2:]

            # Ensure the hex string is two characters long
            if len(hex_result) == 1:
                hex_result = '0' + hex_result

            # Append the result to the first_column list
            first_column.append(hex_result)

        
        round_key = [[first_column[row]] for row in range(4)]
        for col in range(1, 4):  # Loop through columns 1 to 3
            for row in range(4):  # Loop through rows 0 to 3
                # Convert the current cell in previous_key to an integer
                prev_key_value = int(previous_key[row][col], 16)

                # Convert the corresponding cell in the previous round_key column to an integer
                round_key_value = int(round_key[row][col - 1], 16)

                # Perform the XOR operation
                xor_result = prev_key_value ^ round_key_value

                # Convert the XOR result back to a hexadecimal string
                hex_value = hex(xor_result)[2:]  # Remove the '0x' prefix

                # Ensure the hex value is two characters (padding with '0' if necessary)
                if len(hex_value) == 1:
                    hex_value = '0' + hex_value

                # Append the hex value to the current round_key column
                round_key[row].append(hex_value)
        
        return round_key

    def key_schedule(self):
        """
        Implements the AES key schedule to generate 10 round keys.
        """
        current_key = self.hex_to_matrix(self.initial_key)
        self.round_keys.append(current_key)

        # Loop over 10 rounds
        for round_number in range(10):
            # Initialize an empty list for the round constant
            round_constant = []
            
            # Loop through the 4 elements of the round constant
            for i in range(4):
                # Extract the value from RCON and convert it to a two-character hex string
                rcon_value = self.RCON[round_number][i]
                hex_value = hex(rcon_value)[2:]  # Convert to hex and remove '0x'
                
                # Ensure the hex string is two characters long
                if len(hex_value) == 1:
                    hex_value = '0' + hex_value
                
                # Append to the round constant list
                round_constant.append(hex_value)
            
            # Generate the new round key
            current_key = self.generate_round_key(current_key, round_constant)
            
            # Append the generated key to the list of round keys
            self.round_keys.append(current_key)
        

    def get_round_key(self, round_number: int) -> str:
        """
        Retrieve the key for a specific round.

        Args:
            round_number (int): The round number (0 to 10).

        Returns:
            str: The round key as a hexadecimal string.
        """
        if round_number < 0 or round_number > 10:
            raise ValueError("Invalid round number. Must be between 0 and 10.")
        
        matrix = self.round_keys[round_number]
        return ''.join(''.join(row) for row in matrix)
