def PowNMod(base, power, mod):
    res = 1     # Initialize result
    # Update base if it is more
    # than or equal to mod
    base = base % mod
    if (base == 0):
        return 0
    while (power > 0):
        # If power is odd, multiply
        # base with result
        if ((power & 1) == 1):
            res = (res * base) % mod
        # power must be even now
        power = power >> 1      # power = power/2
        base = (base * base) % mod
    return res
