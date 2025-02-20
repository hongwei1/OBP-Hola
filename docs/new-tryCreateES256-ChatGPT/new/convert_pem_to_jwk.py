from jwcrypto import jwk
import json

# Load private key
with open("private_key.pem", "rb") as f:
    pem_data = f.read()

key = jwk.JWK.from_pem(pem_data)

# Convert to JWK format
private_jwk = key.export_private()

# Print JWK keys
print("Private JWK:", json.dumps(json.loads(private_jwk), indent=4))

# Save JWK keys
with open("private_key.jwk", "w") as f:
    f.write(private_jwk)



# Load private key
with open("public_key.pem", "rb") as f:
    pem_data = f.read()

key = jwk.JWK.from_pem(pem_data)

# Convert to JWK format
public_jwk = key.export_public()

# Print JWK keys
print("public JWK:", json.dumps(json.loads(public_jwk), indent=4))

# Save JWK keys
with open("public_key.jwk", "w") as f:
    f.write(public_jwk)
