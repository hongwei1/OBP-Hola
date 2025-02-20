from jwcrypto import jwk

with open("private_key.pem", "rb") as pem_file:
    key = jwk.JWK.from_pem(pem_file.read())

print(key.export_private())
