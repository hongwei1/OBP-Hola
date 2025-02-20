# this is not right:
oauth2.jws_alg=ES256K
need this, but it is not working for keycloak
error: Cannot deserialize value of type `org.keycloak.jose.jws.Algorithm` from String "ES256K": not one of the values accepted for Enum class: [ES384, HS384, ES256, HS256, HS512, PS384, RS384, PS256, RS256, EdDSA, RS512, none, Ed448, Ed25519, ES512, PS512]






https://techdocs.akamai.com/iot-token-access-control/docs/generate-ecdsa-keys

create the private key and  public key, when import the keys, we get the following errors:

2025-02-18 22:07:10,499 ERROR [org.keycloak.services.error.KeycloakErrorHandler] (executor-thread-201) Uncaught server error: java.lang.RuntimeException: org.keycloak.common.util.PemException: java.security.spec.InvalidKeySpecException: encoded key spec not recognized: failed to construct sequence from byte[]: corrupted stream - out of bounds length found: 126 >= 119
at org.keycloak.models.utils.KeycloakModelUtils.getPublicKey(KeycloakModelUtils.java:182)
at org.keycloak.services.resources.admin.ClientAttributeCertificateResource.updateCertFromRequest(ClientAttributeCertificateResource.java:206)
at org.keycloak.services.resources.admin.ClientAttributeCertificateResource.uploadJksCertificate(ClientAttributeCertificateResource.java:175)
at org.keycloak.services.resources.admin.ClientAttributeCertificateResource$quarkusrestinvoker$uploadJksCertificate_62d135313d8c52032b6783eec5ca70e1fff2cc65.invoke(Unknown Source)
at org.jboss.resteasy.reactive.server.handlers.InvocationHandler.handle(InvocationHandler.java:29)
at io.quarkus.resteasy.reactive.server.runtime.QuarkusResteasyReactiveRequestContext.invokeHandler(QuarkusResteasyReactiveRequestContext.java:141)
at org.jboss.resteasy.reactive.common.core.AbstractResteasyReactiveContext.run(AbstractResteasyReactiveContext.java:147)
at io.quarkus.vertx.core.runtime.VertxCoreRecorder$14.runWith(VertxCoreRecorder.java:635)
at org.jboss.threads.EnhancedQueueExecutor$Task.doRunWith(EnhancedQueueExecutor.java:2516)
at org.jboss.threads.EnhancedQueueExecutor$Task.run(EnhancedQueueExecutor.java:2495)
at org.jboss.threads.EnhancedQueueExecutor$ThreadBody.run(EnhancedQueueExecutor.java:1521)
at org.jboss.threads.DelegatingRunnable.run(DelegatingRunnable.java:11)
at org.jboss.threads.ThreadLocalResettingRunnable.run(ThreadLocalResettingRunnable.java:11)
at io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)
at java.base/java.lang.Thread.run(Thread.java:1583)
Caused by: org.keycloak.common.util.PemException: java.security.spec.InvalidKeySpecException: encoded key spec not recognized: failed to construct sequence from byte[]: corrupted stream - out of bounds length found: 126 >= 119
at org.keycloak.common.crypto.PemUtilsProvider.decodePublicKey(PemUtilsProvider.java:92)
at org.keycloak.crypto.def.BCPemUtilsProvider.decodePublicKey(BCPemUtilsProvider.java:78)
at org.keycloak.common.util.PemUtils.decodePublicKey(PemUtils.java:65)
at org.keycloak.models.utils.KeycloakModelUtils.getPublicKey(KeycloakModelUtils.java:180)
... 14 more
Caused by: java.security.spec.InvalidKeySpecException: encoded key spec not recognized: failed to construct sequence from byte[]: corrupted stream - out of bounds length found: 126 >= 119
at org.bouncycastle.jcajce.provider.asymmetric.util.BaseKeyFactorySpi.engineGeneratePublic(Unknown Source)
at org.bouncycastle.jcajce.provider.asymmetric.rsa.KeyFactorySpi.engineGeneratePublic(Unknown Source)
at java.base/java.security.KeyFactory.generatePublic(KeyFactory.java:345)
at org.keycloak.common.util.DerUtils.decodePublicKey(DerUtils.java:69)
at org.keycloak.common.crypto.PemUtilsProvider.decodePublicKey(PemUtilsProvider.java:90)
... 17 more


# try the rest calls, we set this client-id to signed-jwt mode, so can not use it this way.
https://www.keycloak.org/docs-api/latest/rest-api/index.html#_clients
POST /admin/realms/{realm}/clients/{client-uuid}/certificates/{attr}/upload-certificate



## get the accessToken
export ACCESS_TOKEN=$(curl -X POST "http://localhost:7070/realms/master/protocol/openid-connect/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "client_id=admin-cli" \
-d "username=admin" \
-d "password=admin" \
-d "grant_type=password" | jq -r .access_token)


## get the client-uuid
curl -X GET "http://localhost:7070/admin/realms/master/clients?clientId=jwt-client" \
-H "Authorization: Bearer $ACCESS_TOKEN" | jq .


## upload the Pem key
https://github.com/keycloak/keycloak/issues/37066#issuecomment-2636716959
curl -v -H "Authorization: Bearer $ACCESS_TOKEN" \
-F "keystoreFormat=Public Key PEM" \
-F "file=/Users/zhanghongwei/Documents/GitHub-Tower/OBP-Hola/src/main/resources/cert/new-tryCreateES256-weblink/ec-secp256k1-pub-key.pem" \
"http://localhost:7070/admin/realms/master/clients/61d7fc36-fc45-45bd-a6b7-a9035c26da53/certificates/jwt.credential/upload-certificate"


curl -v -H "Authorization: Bearer $ACCESS_TOKEN" \
-F "keystoreFormat=Public Key PEM" \
-F "file=/Users/zhanghongwei/Documents/GitHub-Tower/OBP-Hola/src/main/resources/cert/new-tryCreateES256-ChatGPT/public_key.pem" \
"http://localhost:7070/admin/realms/master/clients/61d7fc36-fc45-45bd-a6b7-a9035c26da53/certificates/jwt.credential/upload-certificate"


curl -v -H "Authorization: Bearer $ACCESS_TOKEN" \
-F "keystoreFormat=Public Key PEM" \
-F "file=/Users/zhanghongwei/Documents/GitHub-Tower/OBP-Hola/src/main/resources/cert/new-tryCreateES256-weblink/12/ec-p256-cert.pem" \
"http://localhost:7070/admin/realms/master/clients/61d7fc36-fc45-45bd-a6b7-a9035c26da53/certificates/jwt.credential/upload-certificate"


## upload the JWK. from ChatGPT -- this is wrong
curl -X PUT "http://localhost:7070/admin/realms/master/clients/61d7fc36-fc45-45bd-a6b7-a9035c26da53" \
-H "Authorization: Bearer $ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"publicKey": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAESwVKyTZGAdhjIFbzU6farTxw5LVyZYx9\nMzX8ZrSrhqhz1sTS62OKwr3X5EhIWfJ7AlVjY4sXu2vvAmt0l7MrFg==\n-----END PUBLIC KEY-----"
}'

# check the exiting public keys
curl -X GET "http://localhost:7070/admin/realms/master/clients/61d7fc36-fc45-45bd-a6b7-a9035c26da53" \
-H "Authorization: Bearer $ACCESS_TOKEN" | jq .publicKey



