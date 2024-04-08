# This is an example of a plugin, it's just a regular function, but instead with a detailed and formatted docstring, and pointers telling the script what type of object should the parameter be.

def encode_message(message: str, shift: int = 1) -> str: # str and int are needed
    """
    Description: Encodes a given message by shifting each letter by a specified number of places down the alphabet. Wraps around the alphabet if the shift goes beyond 'z'. Ideal for simple encryption or obfuscating text. Non-alphabetic characters are left unchanged.
    
    Parameter Description for {message}: A string representing the message to be encoded. It is a required parameter.
    
    Parameter Description for {shift}: (Optional) An integer indicating how many places to shift each letter. Defaults to 1 if not specified.
    
    Required Parameters: {message}
    
    Main Function: Yes
    """
    print(f"[Miles is encoding {message} with a {shift} letter character shift...]") # You must have a print statement that follows this format: print(f"[Miles is EXAMPLE_REPLACE_WITH_YOUR_TEXT...]")
    encoded_message = []
    for char in message:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                start = ord('a')
            else:
                start = ord('A')
            new_char = chr((ord(char) - start + shift_amount) % 26 + start)
            encoded_message.append(new_char)
        else:
            encoded_message.append(char)
    return ''.join(encoded_message) # return it like normal

# You can include multiple functions, as long as each function has the correct docstring formatting, each function will be interpreted as it's own tool

# If you need a helper function (that you don't want to be considered a tool) you can leave out the docstring entirely, or leave out the formatted parts and it will be ignored

# You can import anything you want, add as many tools (functions) as you want, and do anything you want, there are no limitations (besides context length, but highly unlikely you'll reach that)