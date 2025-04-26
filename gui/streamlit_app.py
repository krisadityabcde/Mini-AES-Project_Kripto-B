import streamlit as st
import sys
import os
import pandas as pd
import tempfile

# Pastikan src folder bisa diimport
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\src')))

from utils import chars_to_16bit, bit16_to_chars, bit16_to_hex, bit16_to_binary, bit16_to_decimal
from main import encrypt, decrypt
from block_modes import ecb_encrypt, ecb_decrypt, cbc_encrypt, cbc_decrypt, generate_iv
from avalanche import analyze_plaintext_avalanche, analyze_key_avalanche, full_avalanche_analysis
from file_handler import save_to_txt, save_to_csv, load_from_file, parse_input_file

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
    st.set_page_config(page_title="Mini-AES 16-bit Cipher", layout="centered")
    
    # Initialize session state
    if 'file_upload_key' not in st.session_state:
        st.session_state.file_upload_key = 0
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Enkripsi & Dekripsi", "Mode Operasi Blok", "Analisis Avalanche", "Test Cases"])

    with tab1:
        st.title("🔒 Mini-AES 16-bit Encryptor & Decryptor")
        st.markdown("### Kriptografi B Project")

        # Pilihan Mode: Enkripsi atau Dekripsi
        mode = st.radio("Pilih Mode Operasi:", ["Enkripsi", "Dekripsi"], horizontal=True)

        # Input Options: Manual or File
        input_method = st.radio("Sumber Input:", ["Manual", "File"], horizontal=True)
        
        col1, col2 = st.columns(2)
        
        input_text = ""
        key = ""
        
        if input_method == "Manual":
            with col1:
                input_text = st.text_input(f"{'Plaintext' if mode == 'Enkripsi' else 'Ciphertext'} (2 karakter):", max_chars=2, key="input_text")

            with col2:
                key = st.text_input("Key (2 karakter):", max_chars=2, key="key_text")
        else:
            st.caption("Upload file input (plaintext/ciphertext) dan/atau key")
            
            input_col, key_col = st.columns(2)
            with input_col:
                input_file = st.file_uploader(f"Upload file {'plaintext' if mode == 'Enkripsi' else 'ciphertext'}",
                                            type=["txt", "json"],
                                            key=f"input_file_{st.session_state.file_upload_key}")
            
            with key_col:
                key_file = st.file_uploader("Upload file key",
                                          type=["txt"],
                                          key=f"key_file_{st.session_state.file_upload_key}")
            
            if input_file is not None:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
                    temp_file.write(input_file.getvalue())
                    temp_path = temp_file.name
                
                try:
                    file_data = parse_input_file(temp_path)
                    input_text = file_data.get('input', '')
                    
                    if 'key' in file_data and not key:
                        key = file_data['key']
                        
                    st.success(f"File input dimuat! ({len(input_text)} karakter)")
                    
                    if len(input_text) > 10:
                        st.caption(f"Konten: '{input_text[:10]}...'")
                    else:
                        st.caption(f"Konten: '{input_text}'")
                        
                except Exception as e:
                    st.error(f"Error membaca file: {str(e)}")
                
                # Clean up the temporary file
                os.unlink(temp_path)
            
            if key_file is not None:
                # Create a temporary file for key
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
                    temp_file.write(key_file.getvalue())
                    temp_path = temp_file.name
                
                try:
                    key = load_from_file(temp_path)[:2]  # Take only the first 2 chars
                    st.success(f"File key dimuat! Key: '{key}'")
                except Exception as e:
                    st.error(f"Error membaca file key: {str(e)}")
                
                # Clean up the temporary file
                os.unlink(temp_path)

        # Format Output Options
        st.write("### Format Output:")
        display_formats = st.multiselect(
            "Pilih format tampilan output:",
            ["16-bit (Desimal)", "16-bit (Hex)", "16-bit (Biner)", "Karakter"],
            default=["16-bit (Hex)", "Karakter"]
        )
        
        # Export Options
        export_format = st.radio("Simpan hasil ke file:", ["Tidak", "TXT", "CSV"], horizontal=True)

        if st.button(f"{'🔒 Enkripsi' if mode == 'Enkripsi' else '🔓 Dekripsi'}", type="primary"):
            if len(input_text) < 2 or len(key) < 2:
                st.error("Input dan Key minimal harus terdiri dari 2 karakter.")
            else:
                try:
                    # For simplicity, we'll just use the first 2 characters
                    input_text_short = input_text[:2]
                    key_short = key[:2]
                    
                    input_16bit = chars_to_16bit(input_text_short)
                    key_16bit = chars_to_16bit(key_short)

                    st.write("### Input:")
                    input_cols = st.columns(2)
                    with input_cols[0]:
                        st.write(f"{'Plaintext' if mode == 'Enkripsi' else 'Ciphertext'}: '{input_text_short}' → {input_16bit} (0x{input_16bit:04X})")
                    with input_cols[1]:
                        st.write(f"Key: '{key_short}' → {key_16bit} (0x{key_16bit:04X})")

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
                            
                    # Export functionality
                    if export_format != "Tidak":
                        export_data = {
                            "mode": "Enkripsi" if mode == "Enkripsi" else "Dekripsi",
                            "input": input_text_short,
                            "key": key_short,
                            "output": bit16_to_chars(output_16bit),
                            "output_decimal": bit16_to_decimal(output_16bit),
                            "output_hex": bit16_to_hex(output_16bit),
                            "output_binary": bit16_to_binary(output_16bit),
                            "logs": logs
                        }
                        
                        if export_format == "TXT":
                            file_path = save_to_txt(export_data)
                            st.success(f"Hasil berhasil disimpan ke file TXT: {file_path}")
                        else:  # CSV
                            file_path = save_to_csv(export_data)
                            st.success(f"Hasil berhasil disimpan ke file CSV: {file_path}")

                except Exception as e:
                    st.error(f"Proses Gagal: {str(e)}")

    with tab2:
        st.title("🧩 Mode Operasi Blok")
        st.markdown("### ECB dan CBC untuk data panjang")
        
        block_mode = st.radio("Pilih Mode Operasi Blok:", ["ECB (Electronic Codebook)", "CBC (Cipher Block Chaining)"], horizontal=True)
        mode_action = st.radio("Pilih Aksi:", ["Enkripsi", "Dekripsi"], horizontal=True)
        
        st.write("### Input:")
        col1, col2 = st.columns(2)
        
        with col1:
            block_input = st.text_area(f"{'Plaintext' if mode_action == 'Enkripsi' else 'Ciphertext'} (teks panjang):", 
                                       height=100, 
                                       key="block_input",
                                       help="Untuk mode CBC dekripsi, pastikan IV termasuk dalam 2 karakter pertama")
        
        with col2:
            block_key = st.text_input("Key (2 karakter):", max_chars=2, key="block_key_text")
            
            if block_mode == "CBC (Cipher Block Chaining)" and mode_action == "Enkripsi":
                use_custom_iv = st.checkbox("Custom IV")
                if use_custom_iv:
                    iv_value = st.text_input("IV (2 karakter):", max_chars=2, key="iv_text")
                else:
                    iv_value = None
        
        if st.button(f"{'🔒 Enkripsi' if mode_action == 'Enkripsi' else '🔓 Dekripsi'} dengan {block_mode.split(' ')[0]}", type="primary"):
            if not block_input or len(block_key) != 2:
                st.error("Input dan Key (2 karakter) diperlukan.")
            else:
                try:
                    if mode_action == "Enkripsi":
                        if block_mode == "ECB (Electronic Codebook)":
                            output, logs = ecb_encrypt(block_input, block_key)
                            iv_used = None
                        else:  # CBC
                            iv_to_use = iv_value if 'iv_value' in locals() and iv_value else None
                            output, logs = cbc_encrypt(block_input, block_key, iv_to_use)
                            iv_used = output[:2]  # First 2 chars are the IV
                            
                        st.success("Enkripsi Berhasil!")
                        
                        result_container = st.container()
                        with result_container:
                            st.write("### Hasil Enkripsi:")
                            
                            if block_mode == "CBC (Cipher Block Chaining)":
                                st.info(f"IV: '{iv_used}' (disertakan pada 2 karakter pertama hasil)")
                            
                            st.code(output, language="text")
                            
                            if len(output) > 50:
                                st.caption(f"Total panjang output: {len(output)} karakter")
                    else:
                        # Decryption
                        if block_mode == "ECB (Electronic Codebook)":
                            output, logs = ecb_decrypt(block_input, block_key)
                        else:  # CBC
                            if len(block_input) < 2:
                                st.error("Untuk CBC, ciphertext harus menyertakan IV (minimal 2 karakter)")
                                st.stop()
                            output, logs = cbc_decrypt(block_input, block_key)
                            
                        st.success("Dekripsi Berhasil!")
                        
                        result_container = st.container()
                        with result_container:
                            st.write("### Hasil Dekripsi:")
                            st.code(output, language="text")
                            if len(output) > 50:
                                st.caption(f"Total panjang output: {len(output)} karakter")
                    
                    # Show logs in expander
                    with st.expander(f"🔍 Lihat Proses {block_mode}"):
                        for log in logs:
                            st.text(log)
                    
                    # Export functionality
                    export_format = st.radio(
                        "Simpan hasil ke file:", 
                        ["Tidak", "TXT", "CSV"], 
                        horizontal=True,
                        key="block_export"
                    )
                    
                    if export_format != "Tidak":
                        export_data = {
                            "mode": mode_action,
                            "block_mode": block_mode.split(" ")[0],  # ECB or CBC
                            "input": block_input,
                            "key": block_key,
                            "output": output,
                            "logs": logs
                        }
                        
                        if block_mode == "CBC (Cipher Block Chaining)" and iv_used:
                            export_data["iv"] = iv_used
                        
                        if export_format == "TXT":
                            file_path = save_to_txt(export_data)
                            st.success(f"Hasil berhasil disimpan ke file TXT: {file_path}")
                        else:  # CSV
                            file_path = save_to_csv(export_data)
                            st.success(f"Hasil berhasil disimpan ke file CSV: {file_path}")
                
                except Exception as e:
                    st.error(f"Proses Gagal: {str(e)}")

    with tab3:
        st.title("📊 Analisis Avalanche Effect")
        st.markdown("### Pengujian sensitivitas terhadap perubahan 1-bit")
        
        col1, col2 = st.columns(2)
        with col1:
            avalanche_plaintext = st.text_input("Plaintext (2 karakter):", max_chars=2, key="avalanche_plaintext")
        
        with col2:
            avalanche_key = st.text_input("Key (2 karakter):", max_chars=2, key="avalanche_key")
        
        analysis_type = st.radio(
            "Pilih jenis analisis:", 
            ["Flip bit tertentu pada plaintext", "Flip bit tertentu pada key", "Analisis lengkap"],
            horizontal=True
        )
        
        if analysis_type != "Analisis lengkap":
            bit_position = st.slider("Pilih posisi bit yang akan diubah (0-15):", 0, 15, 0)
        
        if st.button("Analisis Avalanche Effect", type="primary"):
            if len(avalanche_plaintext) != 2 or len(avalanche_key) != 2:
                st.error("Plaintext dan Key harus terdiri dari 2 karakter.")
            else:
                try:
                    if analysis_type == "Flip bit tertentu pada plaintext":
                        result = analyze_plaintext_avalanche(avalanche_plaintext, avalanche_key, bit_position)
                        
                        st.write("### Hasil Analisis Avalanche Effect (Plaintext):")
                        st.write(f"**Plaintext Awal:** '{result['original_plaintext']}' ({result['original_plaintext_binary']})")
                        st.write(f"**Plaintext Dimodifikasi:** '{result['modified_plaintext']}' ({result['modified_plaintext_binary']})")
                        st.write(f"**Bit yang diubah:** Bit-{result['bit_position_flipped']}")
                        
                        st.write("### Hasil Enkripsi:")
                        st.write(f"**Ciphertext Awal:** 0x{result['original_cipher_hex']} ({result['original_cipher_binary']})")
                        st.write(f"**Ciphertext Dimodifikasi:** 0x{result['modified_cipher_hex']} ({result['modified_cipher_binary']})")
                        
                        st.write("### Analisis:")
                        st.metric("Jumlah bit yang berubah", f"{result['bits_changed']} dari {result['total_bits']}")
                        st.metric("Persentase perubahan", f"{result['change_percentage']:.1f}%")
                        
                        # Visualisasi perubahan bit
                        st.write("### Visualisasi Perubahan Bit:")
                        original_bits = result['original_cipher_binary']
                        modified_bits = result['modified_cipher_binary']
                        
                        # Create colored representation
                        html_viz = '<div style="font-family: monospace; font-size: 1.2em;">'
                        html_viz += '<div style="margin-bottom: 5px;">Original: '
                        
                        for i, bit in enumerate(original_bits):
                            html_viz += f'<span>{bit}</span>'
                        
                        html_viz += '</div><div>Modified: '
                        
                        for i, bit in enumerate(modified_bits):
                            if original_bits[i] != bit:
                                html_viz += f'<span style="color: red; font-weight: bold;">{bit}</span>'
                            else:
                                html_viz += f'<span>{bit}</span>'
                        
                        html_viz += '</div></div>'
                        
                        st.markdown(html_viz, unsafe_allow_html=True)
                        
                    elif analysis_type == "Flip bit tertentu pada key":
                        result = analyze_key_avalanche(avalanche_plaintext, avalanche_key, bit_position)
                        
                        st.write("### Hasil Analisis Avalanche Effect (Key):")
                        st.write(f"**Plaintext:** '{result['plaintext']}'")
                        st.write(f"**Key Awal:** '{result['original_key']}' ({result['original_key_binary']})")
                        st.write(f"**Key Dimodifikasi:** '{result['modified_key']}' ({result['modified_key_binary']})")
                        st.write(f"**Bit yang diubah:** Bit-{result['bit_position_flipped']}")
                        
                        st.write("### Hasil Enkripsi:")
                        st.write(f"**Ciphertext Awal:** 0x{result['original_cipher_hex']} ({result['original_cipher_binary']})")
                        st.write(f"**Ciphertext Dimodifikasi:** 0x{result['modified_cipher_hex']} ({result['modified_cipher_binary']})")
                        
                        st.write("### Analisis:")
                        st.metric("Jumlah bit yang berubah", f"{result['bits_changed']} dari {result['total_bits']}")
                        st.metric("Persentase perubahan", f"{result['change_percentage']:.1f}%")
                        
                        # Visualisasi perubahan bit
                        st.write("### Visualisasi Perubahan Bit:")
                        original_bits = result['original_cipher_binary']
                        modified_bits = result['modified_cipher_binary']
                        
                        # Create colored representation
                        html_viz = '<div style="font-family: monospace; font-size: 1.2em;">'
                        html_viz += '<div style="margin-bottom: 5px;">Original: '
                        
                        for i, bit in enumerate(original_bits):
                            html_viz += f'<span>{bit}</span>'
                        
                        html_viz += '</div><div>Modified: '
                        
                        for i, bit in enumerate(modified_bits):
                            if original_bits[i] != bit:
                                html_viz += f'<span style="color: red; font-weight: bold;">{bit}</span>'
                            else:
                                html_viz += f'<span>{bit}</span>'
                        
                        html_viz += '</div></div>'
                        
                        st.markdown(html_viz, unsafe_allow_html=True)
                        
                    else:  # Full analysis
                        with st.spinner("Melakukan analisis lengkap..."):
                            summary = full_avalanche_analysis(avalanche_plaintext, avalanche_key)
                        
                        # Display summary
                        st.write("### Ringkasan Analisis Avalanche Effect:")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("#### Perubahan Bit Plaintext:")
                            st.metric("Rata-rata bit yang berubah", f"{summary['plaintext_avg_bits_changed']:.2f} dari 16")
                            st.metric("Rata-rata persentase perubahan", f"{summary['plaintext_avg_percentage']:.1f}%")
                            
                        with col2:
                            st.write("#### Perubahan Bit Key:")
                            st.metric("Rata-rata bit yang berubah", f"{summary['key_avg_bits_changed']:.2f} dari 16")
                            st.metric("Rata-rata persentase perubahan", f"{summary['key_avg_percentage']:.1f}%")
                        
                        # Visualization with charts
                        st.write("### Grafik Distribusi Perubahan Bit:")
                        
                        pt_bit_changes = [r["bits_changed"] for r in summary["plaintext_results"]]
                        key_bit_changes = [r["bits_changed"] for r in summary["key_results"]]
                        
                        # Create a DataFrame for the chart
                        chart_data = pd.DataFrame({
                            "Bit Position": list(range(16)) + list(range(16)),
                            "Bits Changed": pt_bit_changes + key_bit_changes,
                            "Change Type": ["Plaintext"] * 16 + ["Key"] * 16
                        })
                        
                        st.bar_chart(
                            chart_data, 
                            x="Bit Position", 
                            y="Bits Changed", 
                            color="Change Type",
                            use_container_width=True
                        )
                        
                        # Show detailed results
                        with st.expander("Lihat Detail Hasil Plaintext"):
                            for i, result in enumerate(summary["plaintext_results"]):
                                st.write(f"**Bit {i}:** {result['bits_changed']} bit berubah ({result['change_percentage']:.1f}%)")
                                st.write(f"Original: {result['original_cipher_binary']}")
                                st.write(f"Modified: {result['modified_cipher_binary']}")
                                st.write("---")
                        
                        with st.expander("Lihat Detail Hasil Key"):
                            for i, result in enumerate(summary["key_results"]):
                                st.write(f"**Bit {i}:** {result['bits_changed']} bit berubah ({result['change_percentage']:.1f}%)")
                                st.write(f"Original: {result['original_cipher_binary']}")
                                st.write(f"Modified: {result['modified_cipher_binary']}")
                                st.write("---")
                                
                        # Export functionality
                        export_format = st.radio(
                            "Simpan hasil analisis ke file:", 
                            ["Tidak", "TXT", "CSV"], 
                            horizontal=True,
                            key="avalanche_export"
                        )
                        
                        if export_format != "Tidak":
                            export_data = {
                                "mode": "Avalanche Analysis",
                                "plaintext": avalanche_plaintext,
                                "key": avalanche_key,
                                "plaintext_avg_bits_changed": f"{summary['plaintext_avg_bits_changed']:.2f}",
                                "plaintext_avg_percentage": f"{summary['plaintext_avg_percentage']:.1f}%",
                                "key_avg_bits_changed": f"{summary['key_avg_bits_changed']:.2f}",
                                "key_avg_percentage": f"{summary['key_avg_percentage']:.1f}%",
                                "logs": [
                                    f"Plaintext Analysis: Average {summary['plaintext_avg_bits_changed']:.2f} bits changed ({summary['plaintext_avg_percentage']:.1f}%)",
                                    f"Key Analysis: Average {summary['key_avg_bits_changed']:.2f} bits changed ({summary['key_avg_bits_changed']:.1f}%)",
                                ]
                            }
                            
                            if export_format == "TXT":
                                file_path = save_to_txt(export_data)
                                st.success(f"Hasil berhasil disimpan ke file TXT: {file_path}")
                            else:  # CSV
                                file_path = save_to_csv(export_data)
                                st.success(f"Hasil berhasil disimpan ke file CSV: {file_path}")
                
                except Exception as e:
                    st.error(f"Analisis Gagal: {str(e)}")

    with tab4:
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
