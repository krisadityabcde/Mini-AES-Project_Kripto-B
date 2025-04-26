import streamlit as st
import sys
import os
import pandas as pd

# Pastikan src folder bisa diimport
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\src')))

from utils import chars_to_16bit, bit16_to_chars, bit16_to_hex, bit16_to_binary, bit16_to_decimal
from main import encrypt, decrypt

# Daftar Test Cases
TEST_CASES = [
    {"plaintext": "hi", "key": "01", "expected_hex": "82C4"},
    {"plaintext": "AB", "key": "CD", "expected_hex": "CA93"},
    {"plaintext": "Tz", "key": "k9", "expected_hex": "31A5"},
    {"plaintext": "!@", "key": "#$", "expected_hex": "F3AA"},
    {"plaintext": "ab", "key": "xy", "expected_hex": "D0AC"}
]

def run_test_case(test_case):
    plaintext = test_case["plaintext"]
    key = test_case["key"]
    expected_hex = test_case["expected_hex"]

    pt = chars_to_16bit(plaintext)
    k = chars_to_16bit(key)

    ct, logs = encrypt(pt, k)
    result_hex = bit16_to_hex(ct)

    passed = (result_hex == expected_hex)

    return {
        "passed": passed,
        "actual_hex": result_hex,
        "actual_value": ct,
        "logs": logs
    }

def main():
    st.set_page_config(page_title="Mini-AES 16-bit Encryptor", layout="centered")

    # Tabs
    tab1, tab2 = st.tabs(["Enkripsi & Dekripsi", "Test Cases"])

    with tab1:
        st.title("🔒 Mini-AES 16-bit Encryptor & Decryptor")
        st.markdown("### Kriptografi B Project")

        # Pilihan Mode: Enkripsi atau Dekripsi
        mode = st.radio("Pilih Mode Operasi:", ["Enkripsi", "Dekripsi"], horizontal=True)

        col1, col2 = st.columns(2)

        with col1:
            input_text = st.text_input(f"{'Plaintext' if mode == 'Enkripsi' else 'Ciphertext'} (2 karakter):", max_chars=2, key="input_text")

        with col2:
            key = st.text_input("Key (2 karakter):", max_chars=2, key="key_text")

        st.write("### Format Output:")
        display_formats = st.multiselect(
            "Pilih format tampilan output:",
            ["16-bit (Desimal)", "16-bit (Hex)", "16-bit (Biner)", "Karakter"],
            default=["16-bit (Hex)", "Karakter"]
        )

        if st.button(f"{'🔒 Enkripsi' if mode == 'Enkripsi' else '🔓 Dekripsi'}", type="primary"):
            if len(input_text) != 2 or len(key) != 2:
                st.error("Input dan Key harus terdiri dari 2 karakter.")
            else:
                try:

                    input_16bit = chars_to_16bit(input_text)
                    key_16bit = chars_to_16bit(key)

                    st.write("### Input:")
                    input_cols = st.columns(2)
                    with input_cols[0]:
                        st.write(f"{'Plaintext' if mode == 'Enkripsi' else 'Ciphertext'}: '{input_text}' → {input_16bit} (0x{input_16bit:04X})")
                    with input_cols[1]:
                        st.write(f"Key: '{key}' → {key_16bit} (0x{key_16bit:04X})")

                    # Proses
                    if mode == "Enkripsi":
                        output_16bit, logs = encrypt(input_16bit, key_16bit)
                    else:
                        output_16bit, logs = decrypt(input_16bit, key_16bit)

                    st.write(f"### Output {'Ciphertext' if mode == 'Enkripsi' else 'Plaintext'}:")

                    results = {}
                    if "16-bit (Desimal)" in display_formats:
                        results["Desimal"] = bit16_to_decimal(output_16bit)
                    if "16-bit (Hex)" in display_formats:
                        results["Hex"] = bit16_to_hex(output_16bit)
                    if "16-bit (Biner)" in display_formats:
                        results["Biner"] = bit16_to_binary(output_16bit)
                    if "Karakter" in display_formats:
                        results["Karakter"] = f"'{bit16_to_chars(output_16bit)}'"

                    result_cols = st.columns(len(results))
                    for i, (format_name, value) in enumerate(results.items()):
                        with result_cols[i]:
                            st.metric(label=format_name, value=value)

                    with st.expander(f"🔍 Lihat Proses {'Enkripsi' if mode == 'Enkripsi' else 'Dekripsi'}"):
                        for line in logs:
                            st.text(line)

                except Exception as e:
                    st.error(f"Proses Gagal: {str(e)}")

    with tab2:
        st.title("🧪 Mini-AES Test Cases")
        st.markdown("Run test cases untuk verifikasi implementasi.")

        test_df = pd.DataFrame(TEST_CASES)
        st.dataframe(test_df, use_container_width=True)

        col1, col2 = st.columns([1, 2])

        with col1:
            test_option = st.selectbox(
                "Pilih test case", 
                options=list(range(len(TEST_CASES))),
                format_func=lambda x: f"Test {x+1}: {TEST_CASES[x]['plaintext']} + {TEST_CASES[x]['key']}"
            )

        with col2:
            col2a, col2b = st.columns(2)

            with col2a:
                if st.button("▶️ Run Selected Test"):
                    test_case = TEST_CASES[test_option]
                    result = run_test_case(test_case)
                    if result["passed"]:
                        st.success(f"✅ Test {test_option+1} PASSED")
                    else:
                        st.error(f"❌ Test {test_option+1} FAILED")
                        st.write(f"Expected: {test_case['expected_hex']}, Got: {result['actual_hex']}")

                    with st.expander("🔍 Detail Test"):
                        st.write("**Input:**")
                        pt_value = chars_to_16bit(test_case['plaintext'])
                        st.write(f"Plaintext: '{test_case['plaintext']}' ({pt_value} / 0x{pt_value:04X})")
                        k_value = chars_to_16bit(test_case['key'])
                        st.write(f"Key: '{test_case['key']}' ({k_value} / 0x{k_value:04X})")

                        st.write("**Expected Output:**")
                        st.write(f"Ciphertext (HEX): {test_case['expected_hex']}")

                        st.write("**Actual Output:**")
                        st.write(f"Ciphertext (Decimal): {result['actual_value']}")
                        st.write(f"Ciphertext (HEX): {result['actual_hex']}")
                        st.write(f"Ciphertext (Chars): '{bit16_to_chars(result['actual_value'])}'")

                        st.write("**Proses Enkripsi:**")
                        for line in result["logs"]:
                            st.text(line)

            with col2b:
                if st.button("▶️ Run All Tests"):
                    all_passed = True
                    results = []

                    for i, test_case in enumerate(TEST_CASES):
                        result = run_test_case(test_case)
                        passed = result["passed"]
                        all_passed &= passed
                        results.append({
                            "ID": i+1,
                            "Plaintext": test_case["plaintext"],
                            "Key": test_case["key"],
                            "Expected HEX": test_case["expected_hex"],
                            "Actual HEX": result["actual_hex"],
                            "Status": "✅ PASS" if passed else "❌ FAIL"
                        })

                    if all_passed:
                        st.success("✅ Semua Test LULUS!")
                    else:
                        st.error("❌ Ada Test yang GAGAL!")

                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df, use_container_width=True)

    # Informasi Anggota
    st.markdown("---")
    st.caption("""
    **Mini-AES 16-bit Project | Kriptografi B**
    Anggota:
    - Diandra Naufal Abror / 004
    - Rafael Jonathan Arnoldus / 006
    - Michael Kenneth Salim / 008
    - Rafael Ega Krisaditya / 025
    - Ricko Mianto Jaya Saputra / 031
    """)

if __name__ == "__main__":
    main()
