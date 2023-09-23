
from util.gpt import gpt_in_parallel

PROMPTS = [
    """
Dies ist für meine Informationssicherheit Vorlesung am KIT.
Hilf mir, indem du für das folgende Thema eine Zusammenfassung erstellst:
Z.B.:
Thema: Block Cipher Principles
""",
    """
## Block Cipher Principles

Block ciphers are a type of symmetric encryption algorithm that encrypts data in fixed-size blocks. Symmetric encryption means the same key is used for both encryption and decryption. Block ciphers differ from stream ciphers, which encrypt data bit-by-bit or byte-by-byte. Here are the key principles:

### 1. **Fixed Block Size**:
Block ciphers encrypt a block of plaintext into a block of ciphertext, both of a fixed size. Common block sizes include 64, 128, or 256 bits.

### 2. **Padding**:
If the last block of plaintext is smaller than the block size, it will be padded to fill up the remaining space. Various padding schemes exist, such as PKCS#5, PKCS#7, or zero-padding.

### 3. **Key Size**:
The key used for encryption and decryption is usually of a fixed length, determined by the cipher algorithm (e.g., 128, 192, or 256 bits for AES).

### 4. **Round Functions**:
Block ciphers typically work through multiple rounds of transformations to increase security. Each round applies various functions like substitution, permutation, and mixing to the data.

### 5. **Key Scheduling**:
The main key is often used to derive sub-keys for each round. This is called key scheduling.

### 6. **Reversible Operations**:
Block cipher operations are reversible. You can decrypt the ciphertext to get the original plaintext by applying the reverse operations in reverse order, using the same key.

---

### Application Example: Disk Encryption

One of the most common uses of block ciphers is in disk encryption. When you enable full disk encryption on your laptop, a block cipher is often used to encrypt and decrypt data on-the-fly as you read or write to the disk.

Let's say you have a file containing sensitive information, such as a text file with "my secret data."

1. **Fixed Block Size**: The block cipher will divide this file into fixed-size blocks. If AES with a 128-bit block size is used, each block will contain 128 bits of the file's data.

2. **Padding**: If the last block is not full, it will be padded.

3. **Key Scheduling**: A 256-bit encryption key you provided is used to generate sub-keys for each encryption round.

4. **Encryption Rounds**: The blocks go through multiple rounds of encryption, producing a set of 128-bit ciphertext blocks.

5. **Reading Data**: When you want to read the file, the blocks are decrypted on-the-fly using the same key, and the padding is removed to give you the original data.

In this manner, even if someone gains physical access to your disk, they cannot read the encrypted data without the encryption key.
""",
    """
Das Thema für das ich eine Zusammenfassung brauche ist: {text}
""",
]

OUTPUT_FILE = 'topics_explained.md'
INPUT_FILE = 'topics_refined.md'


topics = open(INPUT_FILE, 'r').read()

prompts = []

for topic in [t.strip()[2:] for t in topics.split('\n') if t.strip().startswith('-')]:
    prompt = [p for p in PROMPTS]
    prompt[-1] = prompts[-1].format(text=topic)
    prompts.append(prompt)

summaries = gpt_in_parallel(prompts)

with open(OUTPUT_FILE, 'w') as f:
    for summary in summaries:
        f.write(summary + "\n\n\n\n")
