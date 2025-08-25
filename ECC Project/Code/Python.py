P = 2 ** 255 - 19
_A = 486662

def _point_add(point_n, point_m, point_diff):
    """Given the projection of two points and their difference, return their sum"""
    (xn, zn) = point_n
    (xm, zm) = point_m
    (x_diff, z_diff) = point_diff
    x = (z_diff << 2) * (xm * xn - zm * zn) ** 2
    z = (x_diff << 2) * (xm * zn - zm * xn) ** 2
    return x % P, z % P

def _point_double(point_n):
    """Double a point provided in projective coordinates"""
    (xn, zn) = point_n
    xn2 = xn ** 2
    zn2 = zn ** 2
    x = (xn2 - zn2) ** 2
    xzn = xn * zn
    z = 4 * xzn * (xn2 + _A * xzn + zn2)
    
    return x % P, z % P

def _const_time_swap(a, b, swap):
    """Swap two values in constant time"""
    index = int(swap) * 2
    temp = (a, b, b, a)
    return temp[index:index + 2]

def _raw_curve25519(base, n):
    """Raise the point base to the power n"""
    zero = (1, 0)
    one = (base, 1)
    mP, m1P = zero, one
    for i in reversed(range(256)):
        bit = bool(n & (1 << i))
        mP, m1P = _const_time_swap(mP, m1P, bit)
        mP, m1P = _point_double(mP), _point_add(mP, m1P, one)
        mP, m1P = _const_time_swap(mP, m1P, bit)

    x, z = mP
    inv_z = pow(z, P - 2, P)
    
    return (x * inv_z) % P
def diffie_hellman(alice_private_bytes,bob_private_bytes):
    # Generate public keys from private keys
    alice_public_key = _raw_curve25519(9,alice_private_bytes)
    bob_public_key = _raw_curve25519(9,bob_private_bytes)

    print(f"Alice Private Key: {hex(alice_private_bytes)}")
    print(f"Alice Public Key:  {hex(alice_public_key)}")
    print(f"Bob Private Key:   {hex(bob_private_bytes)}")
    print(f"Bob Public Key:    {hex(bob_public_key)}")
    # Both compute the shared secret
    alice_shared_secret = _raw_curve25519(bob_public_key, alice_private_bytes)
    bob_shared_secret = _raw_curve25519(alice_public_key, bob_private_bytes)

    print(f"Alice Shared Secret: {alice_shared_secret}")
    print(f"Bob Shared Secret:   {bob_shared_secret}")

alice_private =456789; # Alice's private key
bob_private = 200  # Bob's private key

if __name__ == "__main__":
    diffie_hellman(alice_private,bob_private)
