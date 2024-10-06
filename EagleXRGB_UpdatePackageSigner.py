import os
import hashlib
import argparse
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

def generate_key_pair(private_key_path, public_key_path):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Save the private key
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save the public key
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"Key pair generated. Private key: {private_key_path}, Public key: {public_key_path}")

def sign_update_package(package_path, private_key_path, signature_path):
    # Load the private key
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    # Calculate the SHA-256 hash of the package
    sha256_hash = hashlib.sha256()
    with open(package_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    package_hash = sha256_hash.digest()

    # Sign the hash
    signature = private_key.sign(
        package_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Save the signature
    with open(signature_path, "wb") as f:
        f.write(signature)

    print(f"Update package signed. Signature saved to: {signature_path}")

def calculate_package_hash(package_path):
    sha256_hash = hashlib.sha256()
    with open(package_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EagleXRGB Update Package Signer")
    parser.add_argument("--generate-keys", action="store_true", help="Generate a new key pair")
    parser.add_argument("--sign-package", action="store_true", help="Sign an update package")
    parser.add_argument("--calculate-hash", action="store_true", help="Calculate hash of an update package")
    parser.add_argument("--private-key", help="Path to the private key file")
    parser.add_argument("--public-key", help="Path to the public key file")
    parser.add_argument("--package", help="Path to the update package file")
    parser.add_argument("--signature", help="Path to save the signature file")

    args = parser.parse_args()

    if args.generate_keys:
        if not args.private_key or not args.public_key:
            print("Error: Both --private-key and --public-key paths are required for key generation.")
            exit(1)
        generate_key_pair(args.private_key, args.public_key)

    elif args.sign_package:
        if not args.private_key or not args.package or not args.signature:
            print("Error: --private-key, --package, and --signature are required for signing.")
            exit(1)
        sign_update_package(args.package, args.private_key, args.signature)

    elif args.calculate_hash:
        if not args.package:
            print("Error: --package is required for hash calculation.")
            exit(1)
        package_hash = calculate_package_hash(args.package)
        print(f"Package hash (SHA-256): {package_hash}")

    else:
        print("Error: No action specified. Use --generate-keys, --sign-package, or --calculate-hash.")
        exit(1)