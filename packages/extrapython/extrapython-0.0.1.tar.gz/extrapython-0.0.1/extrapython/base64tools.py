import base64

def encode_base64(message: str) -> str:
    """
    Encodes a given string into its Base64 representation.

    Args:
        message (str): The string to be encoded.

    Returns:
        str: The Base64 encoded string.
    """
    
    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('utf-8')

def decode_base64(base64_message: str) -> str:
    """
    Decodes a Base64 encoded string.

    Args:
        base64_message (str): The Base64 encoded string to decode.

    Returns:
        str: The decoded string.
    """

    base64_bytes = base64_message.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')