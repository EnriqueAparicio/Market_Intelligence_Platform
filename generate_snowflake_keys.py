"""Generate RSA key pair for Snowflake authentication."""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Save private key
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open("claves/rsa_key.p8", "wb") as f:
    f.write(private_pem)

# Save public key
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("claves/rsa_key.pub", "wb") as f:
    f.write(public_pem)

print("✅ Claves generadas exitosamente:")
print("  📄 claves/rsa_key.p8     (PRIVADA - guardar en secreto)")
print("  📄 claves/rsa_key.pub    (PUBLICA - para Snowflake)")
print("\n📋 COPIA LA CLAVE PUBLICA EN SNOWFLAKE:")
print("=" * 70)
print(public_pem.decode())
print("=" * 70)
