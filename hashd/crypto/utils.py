# slices integer value into a 4byte array to ensure correctness when constructing the block
def sliceOp(op):
    opB = bytearray(4)
    for i in range(4):
        opB[i] = op >> (24 - i * 8) & 255
    return opB
