import random
import numpy as np
import streamlit as st

QBER_THRESHOLD = 0.11


def text_to_binary(text: str) -> str:
    return "".join(format(ord(char), "08b") for char in text)


def binary_to_text(binary: str) -> str:
    chunks = [binary[i : i + 8] for i in range(0, len(binary), 8)]
    return "".join(chr(int(chunk, 2)) for chunk in chunks if len(chunk) == 8)


def xor_operation(data: str, key: str) -> str:
    return "".join(str(int(data[i]) ^ int(key[i])) for i in range(len(data)))


def bb84_round(num_bits: int, eve_present: bool):
    alice_bits = np.random.randint(0, 2, num_bits)
    alice_bases = np.random.randint(0, 2, num_bits)
    bob_bases = np.random.randint(0, 2, num_bits)

    bob_results = []
    running_errors = []
    sifted_key = []
    table_rows = []
    errors = 0
    sifted_count = 0

    for idx in range(num_bits):
        bit = int(alice_bits[idx])
        basis = int(alice_bases[idx])

        eve_basis = "-"
        if eve_present:
            eve_basis = random.randint(0, 1)
            if eve_basis != basis:
                bit = random.randint(0, 1)

        if int(bob_bases[idx]) == basis:
            measured_bit = bit
            sifted_count += 1
            sifted_key.append(measured_bit)

            is_error = int(measured_bit != int(alice_bits[idx]))
            errors += is_error
            running_errors.append(is_error)
            status = "ERROR" if is_error else "OK"
        else:
            measured_bit = random.randint(0, 1)
            status = "DISCARDED"

        bob_results.append(measured_bit)

        if idx < 20:
            table_rows.append(
                {
                    "Idx": idx + 1,
                    "Alice Bit": int(alice_bits[idx]),
                    "Alice Basis": basis,
                    "Eve Basis": eve_basis,
                    "Bob Basis": int(bob_bases[idx]),
                    "Bob Bit": measured_bit,
                    "Status": status,
                }
            )

    qber = (errors / sifted_count) if sifted_count else 0.0
    qber_curve = []
    if running_errors:
        cumulative = np.cumsum(running_errors)
        trials = np.arange(1, len(cumulative) + 1)
        qber_curve = (cumulative / trials).tolist()

    return {
        "sifted_key": "".join(map(str, sifted_key)),
        "qber": qber,
        "errors": errors,
        "sifted_count": sifted_count,
        "table_rows": table_rows,
        "qber_curve": qber_curve,
        "num_bits": num_bits,
    }


def generate_key_for_message(required_bits: int, eve_present: bool, multiplier: int):
    collected_key = ""
    total_bits_sent = 0
    total_sifted = 0
    total_errors = 0
    last_rows = []
    last_curve = []

    max_rounds = 8
    for _ in range(max_rounds):
        num_bits = max(required_bits * multiplier, 64)
        round_result = bb84_round(num_bits, eve_present)

        collected_key += round_result["sifted_key"]
        total_bits_sent += round_result["num_bits"]
        total_sifted += round_result["sifted_count"]
        total_errors += round_result["errors"]
        last_rows = round_result["table_rows"]
        last_curve = round_result["qber_curve"]

        if len(collected_key) >= required_bits:
            break

    overall_qber = (total_errors / total_sifted) if total_sifted else 0.0
    return {
        "key": collected_key[:required_bits],
        "qber": overall_qber,
        "total_bits_sent": total_bits_sent,
        "total_sifted": total_sifted,
        "total_errors": total_errors,
        "last_rows": last_rows,
        "last_curve": last_curve,
    }


def qber_comparison(sample_bits: int):
    secure = bb84_round(sample_bits, eve_present=False)["qber"]
    attacked = bb84_round(sample_bits, eve_present=True)["qber"]
    return secure, attacked


st.set_page_config(page_title="BB84 Exhibition Demo", page_icon="B", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=DM+Serif+Display&display=swap');

    .stApp {
        background:
            radial-gradient(80rem 35rem at 10% -10%, #d5f5ec 0%, rgba(213,245,236,0) 60%),
            radial-gradient(70rem 30rem at 90% -20%, #ffe7c6 0%, rgba(255,231,198,0) 60%),
            linear-gradient(180deg, #f9f7f2 0%, #f4f1ea 100%);
        color: #0f172a;
        font-family: 'Manrope', sans-serif;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }

    .hero-tag {
        display: inline-block;
        background: #0f766e;
        color: #ecfeff;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 700;
    }

    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: clamp(2rem, 5vw, 3.8rem);
        margin: 0.8rem 0 0.35rem;
        letter-spacing: -0.01em;
        line-height: 1.03;
    }

    .hero-sub {
        color: #475569;
        max-width: 62ch;
        margin-bottom: 1rem;
        font-size: 1.02rem;
    }

    .card {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid #e5dfd4;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }

    .metric-title {
        font-size: 0.82rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0f172a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<span class="hero-tag">Exhibition Demo</span>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">BB84 Quantum Secure Communication</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Interactive frontend for your project: simulate BB84 key exchange, detect eavesdropping via QBER, and encrypt/decrypt visitor messages live.</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1.25, 1])

with left:
    st.subheader("Secure Transmission")
    message = st.text_area(
        "Message",
        value="Welcome to our quantum security exhibition.",
        height=120,
        help="This message is converted to binary and protected with a BB84-generated key.",
    )

    eve_present = st.toggle("Simulate Eve attack", value=False)
    multiplier = st.slider("Key generation scale", min_value=2, max_value=6, value=4)

    run_demo = st.button("Run BB84 Transmission", type="primary", use_container_width=True)

with right:
    st.subheader("Live Threshold")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("Transmission is aborted if QBER exceeds 11%.")
    st.progress(QBER_THRESHOLD)
    st.write("Reference: secure channels should stay well below this threshold.")
    st.markdown('</div>', unsafe_allow_html=True)

if run_demo:
    if not message.strip():
        st.warning("Enter a message before running the transmission.")
    else:
        msg_binary = text_to_binary(message)
        result = generate_key_for_message(len(msg_binary), eve_present, multiplier)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="card"><div class="metric-title">QBER</div><div class="metric-value">{:.2f}%</div></div>'.format(result["qber"] * 100), unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card"><div class="metric-title">Sifted Bits</div><div class="metric-value">{}</div></div>'.format(result["total_sifted"]), unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="card"><div class="metric-title">Qubits Sent</div><div class="metric-value">{}</div></div>'.format(result["total_bits_sent"]), unsafe_allow_html=True)

        if result["qber"] > QBER_THRESHOLD:
            st.error("Eavesdropping detected. Transmission aborted.")
        elif len(result["key"]) < len(msg_binary):
            st.error("Not enough sifted key bits generated. Increase key generation scale and rerun.")
        else:
            encrypted_binary = xor_operation(msg_binary, result["key"])
            decrypted_binary = xor_operation(encrypted_binary, result["key"])
            decrypted_message = binary_to_text(decrypted_binary)

            st.success("Transmission successful. Message encrypted and recovered.")
            st.code(encrypted_binary[:320] + ("..." if len(encrypted_binary) > 320 else ""), language="text")
            st.write("Decrypted message:")
            st.info(decrypted_message)

        st.subheader("QBER Convergence (last round)")
        if result["last_curve"]:
            st.line_chart(result["last_curve"])
        else:
            st.write("No sifted bits in the last round.")

        st.subheader("Sample Measurement Table (first 20 qubits)")
        st.dataframe(result["last_rows"], use_container_width=True, hide_index=True)

st.divider()
st.subheader("Attack Impact Snapshot")
comparison_bits = st.slider("Comparison qubits", min_value=100, max_value=2000, value=600, step=100)
if st.button("Compare secure vs attack", use_container_width=True):
    secure_qber, attacked_qber = qber_comparison(comparison_bits)
    st.bar_chart(
        {
            "QBER": {
                "Secure Channel": secure_qber,
                "With Eve Attack": attacked_qber,
            }
        }
    )
    st.write(
        f"Secure QBER: {secure_qber*100:.2f}% | Attack QBER: {attacked_qber*100:.2f}%"
    )

st.caption("Built for exhibition demo: BB84 simulation + message encryption workflow in one Streamlit frontend.")
