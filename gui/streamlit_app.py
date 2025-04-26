import streamlit as st
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\src')))

from utils import chars_to_16bit, bit16_to_chars, bit16_to_hex, bit16_to_binary, bit16_to_decimal
from main import encrypt

# Update the TEST_CASES array with correct expected values
TEST_CASES = [
    {
        "plaintext": "hi",
        "key": "01",
        "expected_hex": "82C4",
    },
    {
        "plaintext": "AB",
        "key": "CD",
        "expected_hex": "CA93",
    },
    {
        "plaintext": "Tz",
        "key": "k9",
        "expected_hex": "31A5",
    },
    {
        "plaintext": "!@",
        "key": "#$",
        "expected_hex": "F3AA",
    },
    {
        "plaintext": "ab",
        "key": "xy",
        "expected_hex": "D0AC",
    }
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
    
    # Create tabs for the application
    tab1, tab2 = st.tabs(["Enkripsi", "Test Cases"])
    
    # Tab 1: Encryption functionality
    with tab1:
        # Title and description
        st.title("Mini-AES 16-bit Encryptor")
        st.markdown("### Kriptografi B")
        st.info("Input 2 karakter dan lihat hasilnya dalam berbagai representasi")
        
        # Create two columns for inputs
        col1, col2 = st.columns(2)
        
        with col1:
            plaintext = st.text_input("Plaintext (2 karakter):", max_chars=2, key="encrypt_plaintext")
        
        with col2:
            key = st.text_input("Key (2 karakter):", max_chars=2, key="encrypt_key")
        
        # Display formats selection
        st.write("### Format Output:")
        display_formats = st.multiselect(
            "Pilih format tampilan output:",
            ["16-bit (Desimal)", "16-bit (Hex)", "16-bit (Biner)", "Karakter"],
            default=["16-bit (Hex)", "Karakter"]
        )
        
        # Encryption button
        if st.button("🔒 Enkripsi", type="primary"):
            if len(plaintext) != 2 or len(key) != 2:
                st.error("Plaintext dan Key harus terdiri dari 2 karakter.")
            else:
                try:
                    pt = chars_to_16bit(plaintext)
                    k = chars_to_16bit(key)
                    
                    # Display input values in 16-bit
                    st.write("### Input:")
                    input_cols = st.columns(2)
                    with input_cols[0]:
                        st.write(f"Plaintext: '{plaintext}' → {pt} (0x{pt:04X})")
                    with input_cols[1]:
                        st.write(f"Key: '{key}' → {k} (0x{k:04X})")
                    
                    # Perform encryption
                    ct, logs = encrypt(pt, k)
                    
                    # Display results based on selected formats
                    st.write("### Output Ciphertext:")
                    
                    results = {}
                    if "16-bit (Desimal)" in display_formats:
                        results["Desimal"] = bit16_to_decimal(ct)
                    if "16-bit (Hex)" in display_formats:
                        results["Hex"] = bit16_to_hex(ct)
                    if "16-bit (Biner)" in display_formats:
                        results["Biner"] = bit16_to_binary(ct)
                    if "Karakter" in display_formats:
                        results["Karakter"] = f"'{bit16_to_chars(ct)}'"
                    
                    # Format results in a nice grid or list
                    if results:
                        result_cols = st.columns(len(results))
                        for i, (format_name, value) in enumerate(results.items()):
                            with result_cols[i]:
                                st.metric(label=format_name, value=value)
                    
                    # Display encryption process details
                    with st.expander("Lihat Proses Enkripsi", expanded=False):
                        for line in logs:
                            st.text(line)
                            
                except Exception as e:
                    st.error(f"Enkripsi Gagal: {str(e)}")
    
    # Tab 2: Test Cases functionality
    with tab2:
        st.title("Mini-AES Test Cases")
        st.markdown("Run test cases to verify the implementation works correctly.")
        
        # Show test cases table
        test_df = pd.DataFrame(TEST_CASES)
        test_df = test_df[["plaintext", "key", "expected_hex"]]
        st.dataframe(test_df, use_container_width=True)
        
        # Run specific test
        col1, col2 = st.columns([1, 2])
        with col1:
            test_option = st.selectbox(
                "Select test case", 
                options=list(range(len(TEST_CASES))),
                format_func=lambda x: f"Test {x+1}: {TEST_CASES[x]['plaintext']} + {TEST_CASES[x]['key']}"
            )
        
        with col2:
            col2a, col2b = st.columns(2)
            with col2a:
                if st.button("Run Selected Test", type="primary"):
                    test_case = TEST_CASES[test_option]
                    result = run_test_case(test_case)
                    if result["passed"]:
                        st.success(f"✅ Test {test_option+1} PASSED")
                    else:
                        st.error(f"❌ Test {test_option+1} FAILED")
                        st.write(f"Expected: {test_case['expected_hex']}, Got: {result['actual_hex']}")
                    
                    with st.expander("View Test Details"):
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
                        st.write("**Encryption Process:**")
                        for line in result["logs"]:
                            st.text(line)
            
            with col2b:
                if st.button("Run All Tests"):
                    all_passed = True
                    results = []
                    
                    for i, test_case in enumerate(TEST_CASES):
                        result = run_test_case(test_case)
                        passed = result["passed"]
                        all_passed &= passed
                        results.append({
                            "id": i+1,
                            "plaintext": test_case["plaintext"],
                            "key": test_case["key"],
                            "expected": test_case["expected_hex"],
                            "actual": result["actual_hex"],
                            "status": "✅ PASS" if passed else "❌ FAIL"
                        })
                    
                    if all_passed:
                        st.success("✅ All tests passed!")
                    else:
                        st.error("❌ Some tests failed!")
                    
                    # Show results table
                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df, use_container_width=True)

    # Show project information
    st.markdown("---")
    st.caption("""
    **Mini AES Project Kelas Kriptografi B**
    
    Anggota:
    - Diandra Naufal Abror/004
    - Rafael Jonathan Arnoldus/006
    - Michael Kenneth Salim/008
    - Rafael Ega Krisaditya/025
    - Ricko Mianto Jaya Saputra/031
    """)

if __name__ == "__main__":
    main()