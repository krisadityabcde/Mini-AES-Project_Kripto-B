# Mini AES Project_Kelas Kriptografi B

Anggota:
- Diandra Naufal Abror/004
- Rafael Jonathan Arnoldus/006
- Michael Kenneth Salim/008
- Rafael Ega Krisaditya/025
- Ricko Mianto Jaya Saputra/031


## How To Install
1. Clone the repository:
    ```bash
    git clone https://github.com/krisadityabcde/Mini-AES-Project_Kripto-B.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Mini-AES-Project_Kripto-B
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the program:
    ```bash
    streamlit run gui/streamlit_app.py
    ```


# Implementasi Mini-AES 16-bit 

Mini-AES adalah versi sederhana dari algoritma AES (Advanced Encryption Standard) yang dirancang untuk keperluan pembelajaran. Algoritma ini bekerja pada blok 16-bit (4 nibble) dan menggunakan kunci 16-bit.

- Representasi Data

State: Matriks 2x2 berisi 4 nibble (4-bit).

Plaintext & Key: Diberikan dalam bentuk 2 karakter (masing-masing 8-bit), dikonversi menjadi 16-bit.

- Struktur Rounds

Total 3 Rounds:

Round 0: AddRoundKey

Round 1: SubNibbles → ShiftRows → MixColumns → AddRoundKey

Round 2: SubNibbles → ShiftRows → AddRoundKey

- Operasi Inti

SubNibbles: Substitusi nibble menggunakan S-Box 4-bit.

ShiftRows: Tukar posisi nibble pada baris kedua.

MixColumns: Operasi matriks di medan hingga GF(2^4).

AddRoundKey: XOR state dengan round key.

- Ekspansi Kunci

Key expansion menghasilkan 3 round key dari kunci awal 16-bit:

Kunci dipecah menjadi dua bagian (word 8-bit)

Fungsi substitusi dan konstanta rcon1, rcon2 digunakan untuk menghasilkan word berikutnya.


Program dibuat menggunakan Python dan antarmuka berbasis Streamlit. Fitur yang tersedia:

1. Input plaintext dan key

2. Output dalam bentuk biner, heksadesimal, desimal, dan karakter

3. Proses per round ditampilkan secara detail

4. Pengujian otomatis terhadap test case

## Representasi plaintext dan key: 16-bit (4 nibble) 

Representasi plaintext dan key adalah 2 karakter (masing-masing 8-bit) yang dikonversi menjadi 16-bit melalui fungsi:

```
def chars_to_16bit(text):
    return (ord(text[0]) << 8) | ord(text[1])
``` 

Sudah diimplementasikan di main.py dan digunakan di seluruh proses enkripsi.

### SubNibbles (menggunakan S-Box 4-bit) 

Fungsi sub_nibbles() di aes_core.py menggantikan setiap nibble menggunakan s_box:
```
def sub_nibbles(state):
    return [[s_box[nibble] for nibble in row] for row in state]
```
### ShiftRows
Implementasi shift_rows() di aes_core.py menukar dua nibble di baris kedua:

```
def shift_rows(state):
    state[1][0], state[1][1] = state[1][1], state[1][0]
    return state
```

### MixColumns (dengan matriks sederhana pada GF(24)) 

Menggunakan perkalian di medan hingga dengan gf_mul() ada di aes_core.py:

```
def mix_columns(state):
    a, b = state[0][0], state[1][0]
    c, d = state[0][1], state[1][1]
    return [
        [a ^ gf_mul(4, b), c ^ gf_mul(4, d)],
        [gf_mul(4, a) ^ b, gf_mul(4, c) ^ d]
    ]
```

### AddRoundKey 

Operasi XOR antar state dan round key:

```
def add_round_key(state, key):
    return [[state[i][j] ^ key[i][j] for j in range(2)] for i in range(2)]
```

## Jumlah round: 3

Implementasi pada encrypt():

1. Round 0: AddRoundKey
2. Round 1: SubNibbles → ShiftRows → MixColumns → AddRoundKey
3. Round 2: SubNibbles → ShiftRows → AddRoundKey (tanpa MixColumns)

# Key Expansion (Round Key Generator)

##  Key awal: 16-bit 

Key diterima sebagai input 2 karakter (16-bit) dan diproses di: 
```
def key_expansion(key):
    w = [0] * 6
    w[0] = (key >> 8) & 0xFF
    w[1] = key & 0xFF
```

## Algoritma key expansion sederhana untuk menghasilkan round keys 

Ekspansi menghasilkan 3 round keys dari 16-bit input.

Menggunakan sub_word() dan konstanta rcon1 serta rcon2

```
 rcon1, rcon2 = 0x80, 0x30

    def sub_word(word):
        return ((s_box[(word >> 4) & 0xF] << 4) | s_box[word & 0xF])
```

# Program 
## Menerima input: plaintext & key (masing-masing 16-bit)

Melalui antarmuka streamlit sudah ada kode dengaan max_chars=2 : 
```
 with col1:
            plaintext = st.text_input("Plaintext (2 karakter):", max_chars=2, key="encrypt_plaintext")
```

## Mengeluarkan Output ciphertext 
Output ciphertext ditampilkan dalam berbagai format: 

![Image](https://github.com/user-attachments/assets/99dd53e7-76ec-42b6-b03e-e631dcceccbe)

## Minimal 3 test case dengan expected output benar
Ada 5 Test Case: 

![Image](https://github.com/user-attachments/assets/1144d05e-9044-4b37-ad91-980471975b1d)

## Tampilkan output proses tiap round
Sudah ada tampilan untuk setiap proses: 

![Image](https://github.com/user-attachments/assets/e2b70a04-7946-49b6-b916-42f4be55e0ab)

## Memiliki GUI, menggunakan Tkinter, Streamlit (web-based), dsb 
Sudah Menggunakan streamlit untuk tampilannya 

![Image](https://github.com/user-attachments/assets/67c7fd74-7a11-478f-b5ff-b0b748debb62)


# Flowchart Mini-AES dan Key Expansion 

### Mini-AES
![Image](https://github.com/user-attachments/assets/74fe7366-6803-4851-9195-5e753b8db14d)


### Key Expansion
![Image](https://github.com/user-attachments/assets/86476714-704f-408c-9460-c4ee35b481d0)

# Kelebihan dan keterbatasan Mini-AES

Kelebihan:

1. Sederhana dan mudah dipahami

2. Cocok untuk pembelajaran dasar kriptografi

Keterbatasan:

1. Tidak aman untuk penggunaan nyata

2. Ukuran blok dan key terlalu kecil

