"""
Test script to verify Argon2 password hashing implementation
"""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize Argon2 password hasher
ph = PasswordHasher()

def test_hash_password():
    """Test password hashing"""
    password = "TestPassword123!"
    hashed = ph.hash(password)
    print(f"✓ Password hashing works")
    print(f"  Original: {password}")
    print(f"  Hashed: {hashed[:50]}...")
    return hashed

def test_verify_password(hashed_password):
    """Test password verification"""
    # Test correct password
    try:
        ph.verify(hashed_password, "TestPassword123!")
        print(f"✓ Password verification works (correct password)")
    except VerifyMismatchError:
        print(f"✗ Password verification failed (should have succeeded)")
        return False

    # Test incorrect password
    try:
        ph.verify(hashed_password, "WrongPassword")
        print(f"✗ Password verification failed (should have rejected wrong password)")
        return False
    except VerifyMismatchError:
        print(f"✓ Password verification correctly rejects wrong password")

    return True

def test_rehash_check(hashed_password):
    """Test rehash checking"""
    needs_rehash = ph.check_needs_rehash(hashed_password)
    print(f"✓ Rehash check works (needs rehash: {needs_rehash})")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Argon2 Password Hashing Implementation")
    print("=" * 60)

    hashed = test_hash_password()
    print()

    if test_verify_password(hashed):
        print()
        test_rehash_check(hashed)
        print()
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("Some tests failed! ✗")
        print("=" * 60)
