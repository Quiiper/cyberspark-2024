from jwcrypto import jwk

JWT_SECRET_KEY = jwk.JWK.generate(kid="shopifyKey",kty='RSA', size=4096)

with open('./jwt_secret_key.pem', 'wb') as f:
    f.write(JWT_SECRET_KEY.export_to_pem(private_key=True, password=None))