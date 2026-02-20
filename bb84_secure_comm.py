import numpy as np
import matplotlib.pyplot as plt
import random

# -------------------------------
# TEXT ?? BINARY CONVERSION
# -------------------------------

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

# -------------------------------
# XOR ENCRYPTION
# -------------------------------

def xor_operation(data, key):
    return ''.join(str(int(data[i]) ^ int(key[i])) for i in range(len(data)))

# -------------------------------
# BB84 SIMULATION
# -------------------------------

def bb84_simulation(num_bits, eve_present=False):
    alice_bits = np.random.randint(0, 2, num_bits)
    alice_bases = np.random.randint(0, 2, num_bits)
    bob_bases = np.random.randint(0, 2, num_bits)

    bob_results = []
    errors = 0
    sifted_key = []

    for i in range(num_bits):
        bit = alice_bits[i]
        basis = alice_bases[i]

        # Eve intercepts
        if eve_present:
            eve_basis = random.randint(0, 1)
            if eve_basis == basis:
                measured_bit = bit
            else:
                measured_bit = random.randint(0, 1)
            bit = measured_bit  # Eve resends

        # Bob measures
        if bob_bases[i] == basis:
            measured_bit = bit
        else:
            measured_bit = random.randint(0, 1)

        bob_results.append(measured_bit)

        # Sifting
        if bob_bases[i] == basis:
            sifted_key.append(measured_bit)
            if measured_bit != alice_bits[i]:
                errors += 1

    sifted_key = np.array(sifted_key)

    if len(sifted_key) == 0:
        qber = 0
    else:
        qber = errors / len(sifted_key)

    return sifted_key, qber

# -------------------------------
# GRAPH FUNCTION
# -------------------------------

def plot_qber(qber, eve_present):
    plt.figure()
    label = "With Eve (Attack)" if eve_present else "Without Eve (Secure)"
    plt.bar([label], [qber])
    plt.axhline(y=0.11, linestyle='--')
    plt.ylabel("QBER")
    plt.title("Quantum Bit Error Rate")
    plt.ylim(0, 0.5)
    plt.show()

# -------------------------------
# MAIN PROGRAM
# -------------------------------

def main():
    print("\n?? QUANTUM SECURE COMMUNICATION PLATFORM\n")

    message = input("Enter message to send: ")
    message_binary = text_to_binary(message)

    eve_choice = input("Simulate Eve attack? (yes/no): ").lower()
    eve_present = True if eve_choice == "yes" else False

    num_bits = len(message_binary) * 2  # Generate extra bits for safety

    sifted_key, qber = bb84_simulation(num_bits, eve_present)

    print(f"\nQBER: {round(qber*100, 2)}%")

    threshold = 0.11  # 11% threshold

    if qber > threshold:
        print("? Eavesdropping detected! Transmission aborted.")
        plot_qber(qber, eve_present)
        return

    # Ensure key length matches message length
    key_binary = ''.join(map(str, sifted_key))
    key_binary = key_binary[:len(message_binary)]

    encrypted_binary = xor_operation(message_binary, key_binary)
    decrypted_binary = xor_operation(encrypted_binary, key_binary)
    decrypted_message = binary_to_text(decrypted_binary)

    print("\n--- Transmission Successful ---")
    print("Encrypted (binary):", encrypted_binary)
    print("Decrypted message:", decrypted_message)

    plot_qber(qber, eve_present)


if __name__ == "__main__":
    main()
