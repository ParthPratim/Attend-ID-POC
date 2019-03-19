def hex_to_bytes(hex):
    bytez = []
    hex = ''.join( hex.split(" ") )
    for i in range(0, len(hex), 2):
        bytez.append( chr( int (hex[i:i+2], 16 ) ) )
    byte_val = ''.join( bytez )
    return bytes(byte_val.encode())