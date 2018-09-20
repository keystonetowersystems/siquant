abbreviations = ('kg', 'm', 's', 'k', 'a', 'mol', 'cd')

def SIDimensions(kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
    return (kg, m, s, k, a, mol, cd)

def dim_mul(dims1, dims2):
    return (
        dims1[0] + dims2[0],
        dims1[1] + dims2[1],
        dims1[2] + dims2[2],
        dims1[3] + dims2[3],
        dims1[4] + dims2[4],
        dims1[5] + dims2[5],
        dims1[6] + dims2[6]
    )

def dim_div(dims1, dims2):
    return (
        dims1[0] - dims2[0],
        dims1[1] - dims2[1],
        dims1[2] - dims2[2],
        dims1[3] - dims2[3],
        dims1[4] - dims2[4],
        dims1[5] - dims2[5],
        dims1[6] - dims2[6]
    )

def dim_pow(dims, exp):
    return (
        dims[0] * exp,
        dims[1] * exp,
        dims[2] * exp,
        dims[3] * exp,
        dims[4] * exp,
        dims[5] * exp,
        dims[6] * exp
    )

def dim_str(dims):
    return '*'.join(
        '%s**%g' % (unit_abbreviation, power)
        for unit_abbreviation, power in zip(abbreviations, dims)
        if power != 0
    )

