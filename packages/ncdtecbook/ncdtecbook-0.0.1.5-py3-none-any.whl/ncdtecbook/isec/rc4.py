import ipywidgets as widgets
from IPython.display import display

# Step 1: Key Scheduling Algorithm (KSA)
def KSA(key, s_length=8):
    key_length = len(key)
    S = list(range(s_length))  # Initialize S array with 0 to s_length
    j = 0
    
    # Scramble the S array using the key
    for i in range(s_length):
        j = (j + S[i] + key[i % key_length]) % s_length
        S[i], S[j] = S[j], S[i]  # Swap values
    
    return S

# Step 2: Pseudo-Random Generation Algorithm (PRGA)
def PRGA(S):
    s_length = len(S)
    i = 0
    j = 0
    while True:
        i = (i + 1) % s_length
        j = (j + S[i]) % s_length
        S[i], S[j] = S[j], S[i]  # Swap values
        # Output keystream byte
        K = S[(S[i] + S[j]) % s_length]
        yield K


# Utility function to convert text to byte array
def text_to_bytes(text):
    return [ord(char) for char in text]


# Step 3: Encryption and Decryption using RC4
def RC4(key, plaintext):
    S = KSA(key)  # Key Scheduling
    keystream = PRGA(S)  # Pseudo-Random Generation
    
    ciphertext = []
    for char in plaintext:
        ks_byte = next(keystream)  # Get keystream byte
        ciphertext.append(char ^ ks_byte)  # XOR plaintext with keystream
    
    return ciphertext


# Convert back to string (for printing decrypted text)
def bytes_to_text(byte_array):
    return ''.join(chr(byte) for byte in byte_array)


def example_rc4():
    # Creating the widgets

    # 1. Text input for key
    key_input = widgets.Text(
        value='',
        placeholder='Enter encryption key',
        description='Key:',
    )

    # 2. Label to show the text_to_bytes of the key in real-time
    key_bytes = widgets.Label(value="Key Bytes: ")

    # 3. Text input for message
    message_input = widgets.Text(
        value='',
        placeholder='Enter message',
        description='Plain Text:',
    )

    # 4. Label to show the text_to_bytes of the message in real-time
    message_bytes = widgets.Label(value="Plain Text Bytes: ")

    # 5. Label to show the cipher bytes (output of RC4 function)
    cipher_bytes = widgets.Label(value="Cipher Bytes: ")

    cipher_message = widgets.Label(value="Cipher Text: ")

    # 6. Label to show the decrypted message (output of bytes_to_text on the cipher bytes)
    # decrypted_message = widgets.Label(value="Decrypted Message: ")

    # Function to update the cipher_bytes and decrypted_message when message_input changes
    def update_cipher_and_decrypted(change):
        # Get the new message and key values
        # message = change['new']
        key = key_input.value
        message = message_input.value
        

        key_bytes.value = f"Key Bytes: {text_to_bytes(key)}"

        # Convert message and key to byte arrays
        message_byte_array = text_to_bytes(message)
        key_byte_array = text_to_bytes(key)
        
        # Update the message bytes label
        message_bytes.value = f"Plain Text Bytes: {message_byte_array}"
        
        # Encrypt using RC4
        cipher_byte_array = RC4(key_byte_array, message_byte_array)
        
        # Update the cipher bytes label
        cipher_bytes.value = f"Cipher Bytes: {cipher_byte_array}"
        
        cipher_message.value = f"Cipher Text: {bytes_to_text(cipher_byte_array)}"
        
        # Decrypt the cipher bytes back to text
        # decrypted = bytes_to_text(RC4(key_byte_array, cipher_byte_array))
        
        # Update the decrypted message label
        # decrypted_message.value = f"Decrypted Message: {decrypted}"

    # Link the key_input text change to update the key_bytes label
    key_input.observe(update_cipher_and_decrypted, names='value')

    # Link the message_input text change to update cipher_bytes and decrypted_message
    message_input.observe(update_cipher_and_decrypted, names='value')

    # Display the widgets
    display(
        key_input,
        key_bytes,
        message_input,
        message_bytes,
        cipher_bytes,
        cipher_message,
        # decrypted_message,
        )
