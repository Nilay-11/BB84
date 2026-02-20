import random
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

QBER_THRESHOLD = 0.11


def generate_bits(n):
    return np.random.randint(2, size=n)


def generate_bases(n):
    return np.random.choice(["Z", "X"], size=n)


def measure(bits, sender_bases, receiver_bases):
    result = []
    for i in range(len(bits)):
        if sender_bases[i] == receiver_bases[i]:
            result.append(bits[i])
        else:
            result.append(random.randint(0, 1))
    return np.array(result)


def sift_key(sender_bases, receiver_bases, bits):
    sifted = []
    indices = []
    for i in range(len(sender_bases)):
        if sender_bases[i] == receiver_bases[i]:
            sifted.append(int(bits[i]))
            indices.append(i + 1)
    return np.array(sifted), indices


def calculate_qber(key1, key2):
    errors = np.sum(key1 != key2)
    return errors / len(key1) if len(key1) > 0 else 1.0


def text_to_binary(text):
    return "".join(format(ord(char), "08b") for char in text)


def binary_to_text(binary):
    chars = [binary[i : i + 8] for i in range(0, len(binary), 8)]
    return "".join(chr(int(char, 2)) for char in chars if len(char) == 8)


def xor_binary(data, key):
    return "".join(str(int(data[i]) ^ int(key[i])) for i in range(len(data)))


def run_intercept_resend_simulation(total_qubits):
    alice_bits = generate_bits(total_qubits)
    alice_bases = generate_bases(total_qubits)
    eve_bases = generate_bases(total_qubits)
    bob_bases = generate_bases(total_qubits)

    eve_bits = measure(alice_bits, alice_bases, eve_bases)
    bob_bits = measure(eve_bits, eve_bases, bob_bases)

    alice_key, sifted_indices = sift_key(alice_bases, bob_bases, alice_bits)
    bob_key, _ = sift_key(alice_bases, bob_bases, bob_bits)

    qber = calculate_qber(alice_key, bob_key)

    # Running QBER on sifted bits
    running_errors = []
    for i in range(len(alice_key)):
        running_errors.append(int(alice_key[i] != bob_key[i]))

    qber_curve = []
    if running_errors:
        cumulative = np.cumsum(running_errors)
        trials = np.arange(1, len(cumulative) + 1)
        qber_curve = (cumulative / trials).tolist()

    sample_rows = []
    for i in range(min(20, total_qubits)):
        status = "Discarded"
        if alice_bases[i] == bob_bases[i]:
            status = "YES" if alice_bits[i] == bob_bits[i] else "ERROR"
        sample_rows.append(
            {
                "Idx": i + 1,
                "Alice Bit": int(alice_bits[i]),
                "Alice Basis": alice_bases[i],
                "Eve Basis": eve_bases[i],
                "Bob Basis": bob_bases[i],
                "Bob Bit": int(bob_bits[i]),
                "Status": status,
            }
        )

    return {
        "qber": qber,
        "sifted": len(alice_key),
        "errors": int(np.sum(alice_key != bob_key)) if len(alice_key) > 0 else 0,
        "qber_curve": qber_curve,
        "sifted_indices": sifted_indices,
        "sample_rows": sample_rows,
    }


def run_live_demo(message, eve_attack, n_bits):
    alice_bits = generate_bits(n_bits)
    alice_bases = generate_bases(n_bits)
    bob_bases = generate_bases(n_bits)

    if eve_attack:
        eve_bases = generate_bases(n_bits)
        eve_measure = measure(alice_bits, alice_bases, eve_bases)
        bob_bits = measure(eve_measure, eve_bases, bob_bases)
    else:
        bob_bits = measure(alice_bits, alice_bases, bob_bases)

    alice_key, _ = sift_key(alice_bases, bob_bases, alice_bits)
    bob_key, _ = sift_key(alice_bases, bob_bases, bob_bits)

    qber = calculate_qber(alice_key, bob_key)

    if len(alice_key) == 0:
        return {"qber": qber, "ok": False, "reason": "No sifted key generated."}

    message_binary = text_to_binary(message)
    key_binary = "".join(map(str, alice_key))
    key_binary = (key_binary * (len(message_binary) // len(key_binary) + 1))[: len(message_binary)]

    encrypted_binary = xor_binary(message_binary, key_binary)
    decrypted_binary = xor_binary(encrypted_binary, key_binary)
    decrypted_message = binary_to_text(decrypted_binary)

    return {
        "qber": qber,
        "ok": qber < 0.2,
        "encrypted_binary": encrypted_binary,
        "decrypted_message": decrypted_message,
        "alice_key_len": len(alice_key),
    }


st.set_page_config(page_title="Quantum Encryption Exhibition", page_icon="Q", layout="wide")

st.markdown(
    """
        <style>
    .stApp {
      background:
        radial-gradient(60rem 30rem at 10% -10%, rgba(34,197,94,0.18) 0%, rgba(34,197,94,0) 60%),
        radial-gradient(70rem 35rem at 100% 0%, rgba(59,130,246,0.20) 0%, rgba(59,130,246,0) 60%),
        linear-gradient(180deg, #020617 0%, #0b1120 50%, #020617 100%);
      color: #dbeafe;
    }
    .block-container { max-width: 1100px; }
    h1, h2, h3 { color: #86efac; }
    p, label, .stMarkdown, .stCaption { color: #bfdbfe !important; }
    .stButton > button {
      background: linear-gradient(90deg, #2563eb 0%, #22c55e 100%);
      color: #ecfeff;
      border: none;
      border-radius: 10px;
      font-weight: 700;
    }
    .stMetric {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(59,130,246,0.35);
      border-radius: 10px;
      padding: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Quantum Encryption Project - BB84")
st.write("Clean exhibition app with two modes: full simulation and live message demo.")

sim_tab, live_tab = st.tabs(["Simulation", "Live Demo"])

with sim_tab:
    st.subheader("Intercept-Resend Simulation (First Model)")
    total_qubits = st.slider("Total Qubits", 100, 2000, 350, step=50)

    if st.button("Run Simulation", key="run_sim"):
        result = run_intercept_resend_simulation(total_qubits)

        c1, c2, c3 = st.columns(3)
        c1.metric("QBER", f"{result['qber']*100:.2f}%")
        c2.metric("Sifted Key Length", result["sifted"])
        c3.metric("Errors", result["errors"])

        fig, ax = plt.subplots(figsize=(9, 4.5))
        if result["qber_curve"]:
            ax.plot(result["sifted_indices"], result["qber_curve"], color="#22d3ee", linewidth=2, label="Simulated QBER")
        ax.axhline(y=0.25, color="#ef4444", linestyle="--", linewidth=2, label="Theory (25%)")
        ax.set_title("QBER During Intercept-Resend Attack")
        ax.set_xlabel("Sifted Qubit Index")
        ax.set_ylabel("QBER")
        ax.set_ylim(0, 0.5)
        ax.grid(alpha=0.3)
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)

        st.dataframe(result["sample_rows"], use_container_width=True, hide_index=True)

with live_tab:
    st.subheader("Interactive Live Demo (Message Encryption + QBER)")
    message = st.text_input("Enter Message", value="Welcome to our quantum exhibition")
    eve_attack = st.checkbox("Simulate Eve Attack")
    n_bits = st.slider("Transmission Bits", 100, 2000, 400, step=50)

    if st.button("Start Secure Transmission", key="run_live"):
        if not message.strip():
            st.warning("Please enter a message.")
        else:
            output = run_live_demo(message, eve_attack, n_bits)

            fig2, ax2 = plt.subplots(figsize=(5, 3))
            ax2.bar(["QBER"], [output["qber"]], color="#38bdf8")
            ax2.axhline(y=QBER_THRESHOLD, color="#f59e0b", linestyle="--", label="11% Threshold")
            ax2.set_ylim(0, 1)
            ax2.set_ylabel("QBER")
            ax2.legend()
            st.pyplot(fig2)
            plt.close(fig2)

            st.write(f"QBER: {output['qber']:.3f}")

            if not output["ok"]:
                st.error("Possible eavesdropping detected or insecure channel. Transmission aborted.")
                if "reason" in output:
                    st.caption(output["reason"])
            else:
                st.success("Secure channel established.")
                st.code(output["encrypted_binary"][:400] + ("..." if len(output["encrypted_binary"]) > 400 else ""))
                st.write("Decrypted Message:")
                st.info(output["decrypted_message"])
                st.caption(f"Sifted key length: {output['alice_key_len']} bits")

