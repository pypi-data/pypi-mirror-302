from ipywidgets import  GridBox, Layout, Label, Text, Textarea, Button

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

    key_label = Label(
        value='Key:',
        layout=Layout(width='auto', grid_area='key'),
    )
    key_input = Text(
        value='',
        placeholder='Enter encryption key',
        description='',
        continuous_update=False,
        layout=Layout(width='auto', grid_area='keyv')
    )

    # 2. Label to show the text_to_bytes of the key in real-time
    key_bytes_label = Label(
        value='Key Bytes:',
        layout=Layout(width='auto', grid_area='kb')
    )
    key_bytes = Textarea(
        value='',
        disabled=True,
        layout=Layout(width='auto', grid_area='kbv')
    )

    # 3. Text input for message
    message_input_label = Label(
        value='Plain Text:',
        layout=Layout(width='auto', grid_area='pt')
    )
    message_input = Textarea(
        value='',
        placeholder='Enter message',
        continuous_update=False,
        disabled=False,
        layout=Layout(width='auto', grid_area='ptv')
    )

    
    # 4. Label to show the text_to_bytes of the message in real-time
    message_bytes_label = Label(
        value='Plain Text Bytes:',
        layout=Layout(width='auto', grid_area='ptb')
    )
    message_bytes = Textarea(
        value='',
        disabled=True,
        layout=Layout(width='auto', grid_area='ptbv')
    )

    # 5. Encryption button
    btn_encrypt = Button(
            description="Encrypt",
            button_style='success',
            layout=Layout(width='auto', grid_area='btn')
        )

    # 6. Label to show the cipher bytes (output of RC4 function)
    cipher_bytes_label = Label(
        value='Cipher Bytes:',
        layout=Layout(width='auto', grid_area='ctb')
    )

    cipher_bytes = Textarea(
        value='',
        disabled=True,
        layout=Layout(width='auto', grid_area='ctbv')
    )

    cipher_message_label = Label(
        value='Cipher Text:',
        layout=Layout(width='auto', grid_area='ct')
    )
    cipher_message =  Textarea(
        value='',
        disabled=True,
        layout=Layout(width='auto', grid_area='ctv')
    )


    gb = GridBox(children=[
        key_label, key_input,
        key_bytes_label, key_bytes,
        message_input_label, message_input,
        message_bytes_label, message_bytes,
        btn_encrypt,
        cipher_bytes_label, cipher_bytes,
        cipher_message_label, cipher_message

        ],
        layout=Layout(
            width='80%',
            grid_template_rows='auto auto auto auto auto auto auto',
            grid_template_columns='25% 75%',
            grid_template_areas='''
            "key keyv"
            "kb kbv"
            "pt ptv"
            "ptb ptbv"
            "btn btn"
            "ctb ctbv"
            "ct ctv"
            ''')
       )
    # Function to update the cipher_bytes and decrypted_message when message_input changes
    def update_cipher_and_decrypted(change):
        # Get the new message and key values
        # message = change['new']
        key = key_input.value
        message = message_input.value
        

        key_bytes.value = f"{text_to_bytes(key)}"

        # Convert message and key to byte arrays
        message_byte_array = text_to_bytes(message)
        key_byte_array = text_to_bytes(key)
        
        # Update the message bytes label
        message_bytes.value = f"{message_byte_array}"
        
        # Encrypt using RC4
        cipher_byte_array = RC4(key_byte_array, message_byte_array)
        
        # Update the cipher bytes label
        cipher_bytes.value = f"{cipher_byte_array}"
        
        cipher_message.value = f"{bytes_to_text(cipher_byte_array)}"
        
        # Decrypt the cipher bytes back to text
        # decrypted = bytes_to_text(RC4(key_byte_array, cipher_byte_array))
        
        # Update the decrypted message label
        # decrypted_message.value = f"Decrypted Message: {decrypted}"

    # Link the key_input text change to update the key_bytes label
    key_input.observe(update_cipher_and_decrypted, names='value')

    # Link the message_input text change to update cipher_bytes and decrypted_message
    message_input.observe(update_cipher_and_decrypted, names='value')

    btn_encrypt.on_click(update_cipher_and_decrypted)


    # Display the widgets
    display(
        gb,
        # key_input,
        # key_bytes,
        # message_input,
        # message_bytes,
        # btn_encrypt,
        # cipher_bytes,
        # cipher_message,
        # decrypted_message,
        )
