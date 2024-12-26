def chunk_plaintext(plain_text):
    block_size = 32
    chunks = []

    for i in range(0, len(plain_text), block_size):
        chunks.append(plain_text[i:i + block_size])

    # Check if the last block needs padding
    if len(chunks[-1]) < block_size:
        diff = block_size - len(chunks[-1])
        chunks[-1] += "f" * (diff) # Custom padding

    for chunk in chunks:
        print("chunk")
        print(chunk)
    return chunks


def padd_plaintext(plain_text):
    if len(plain_text) < 32:
        diff = 32 - len(plain_text)
        print(f"diff: {diff}")
        plain_text = plain_text + "f" * (diff)
        return [plain_text]
    else:
        return chunk_plaintext(plain_text)


def validate_plaintext(plain_text):
    if len(plain_text) == 32:
        return [plain_text]
    else:
        return padd_plaintext(plain_text)
    