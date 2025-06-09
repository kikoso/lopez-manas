---
title: "Using the Signature class to verify data"
author: "Enrique López-Mañas"
date: 2020-10-26T19:34:11.196Z
lastmod: 2025-06-09T09:49:51+02:00

description: ""

subtitle: "When there is an exchange of information happening, we often want to verify that the origin of the data is the right one. This can be used…"

image: "/articles/2020-10-26_using-the-signature-class-to-verify-data/images/1.jpeg" 
images:
 - "/articles/2020-10-26_using-the-signature-class-to-verify-data/images/1.jpeg"
 - "/articles/2020-10-26_using-the-signature-class-to-verify-data/images/2.png"


aliases:
    - "/using-the-signature-class-to-verify-data-ff1add1da348"

---

When there is an exchange of information happening, we often want to verify that the origin of the data is the right one. This can be used to ensure that the right clients are having access to our resources.

For instance, let’s imagine that we want to ensure that an authorized device is querying a file with sensitive information from our backend. An immediate solution could be to use a X-Api-Token in our device. I wrote [previously](https://medium.com/google-developer-experts/a-follow-up-on-how-to-store-tokens-securely-in-android-e84ac5f15f17) about how we can store tokens securely in Android: ideally, the X-Api-Token should not be stored in plain text, since everything delivered as plain-text in an Android app can be considered open source. One more twist to the story could be to have a local function that generates the token, and that is understood by the server as well.

However, we can actually link this verification to a concrete resource, to provide an additional layer of security. Conceptually: if I want to access the file XZY, I will generate accordingly a verification to access that file — maybe even together in combination with the X-Api-Token. If we want to do that in Android, we can use the Signature class to generate the signature.

I had to do this recently, and in the security field we often walk a desert realm with a few desultory StackOverflow posts, trying to join the pieces. Hence the current article — if anybody benefits from its content, mission accomplished.

The [Signature](https://developer.android.com/reference/java/security/Signature) class in Android exists since its first version, although it has had a few additions through Android history. Most notably, since API Level 23 we have access to a few more encryption algorithms, including _SHA512withRSA/PSS_. SHA512withRSA/PSS is probably as secure as it gets for most commercial applications.

This algorithm produces a signature from a digest length of 512 bits. PSS stands for [Probabilistic Signature Scheme](https://web.archive.org/web/20040713140300/http://grouper.ieee.org/groups/1363/P1363a/contributions/pss-submission.pdf). RSA is itself not an encryption algorithm, but a family of permutations which obscure the code, but are not useful in isolation. PSS adds an encryption schema.

Android does not really support PKCS1, so we need to generate first a PKCS key. We can easily do this using openssl:
```
openssl genpkey -out rsakey.pem -algorithm RSA -pkeyopt rsa_keygen_bits:2048
```

With this key already generated, we need to send it to the device. One option would be to deliver the APK with the private key included in the assets folder, but everything that is delivered in the Android APK can be considered open source. A solution would be to send it via SSL — not an infallible solution, but eliminates some risk.

With this already done, we need to do a few adjustments to the key. We need to strip first the **BEGIN PRIVATE KEY** and **END PRIVATE KEY** since otherwise the Signature class will not work. When we have achieved that, we can proceed to calculate the signature:

```Kotlin
val signatureSHA256 = Signature.getInstance("SHA256withRSA/PSS")
signatureSHA256.setParameter(PSSParameterSpec("SHA-256", "MGF1", MGF1ParameterSpec.SHA256, 32, 1))
val privateKey = loadPrivateKey("MY_KEY")
signatureSHA256.initSign(privateKey)
val data: ByteArray = "name_of_the_file".toByteArray()
signatureSHA256.update(data)
var finalSignature = signatureSHA256.sign()
```

The method that strips the irrelevant content from the key is the following:
```Kotlin
private fun loadPrivateKey(key: String): PrivateKey {
    val readString = key.replace("-----BEGIN PRIVATE KEY-----\n", "").replace("-----END PRIVATE KEY-----", "")
    }

    val encoded = Base64.decode(readString, Base64.DEFAULT)
    return KeyFactory.getInstance("RSA")
            .generatePrivate(PKCS8EncodedKeySpec(encoded))
}
```


Another twist would be to convert the resulting signature into hexadecimal code. In Android, we can easily do it with a Kotlin extension:

```Kotlin
fun ByteArray.toHexString() = joinToString("") { "%02x".format(it) }
```

Now we are ready. We can send the request to our server specifying the file we want to access, and the signature associated with it. The server needs to do the opposite procedure (convert from hexadecimal to text, and then apply the signature verification). This is how our request would look like:

![image](/articles/2020-10-26_using-the-signature-class-to-verify-data/images/2.png#layoutTextWidth)


Now, the backend needs to do the verification, and ensure that the data is properly verified. There are a few changes to the previous code — essentially, this time we are aiming to work with the public key, and use the method _verify(data)_, which will ultimately verify that the data has been sent by the appropriate client:

```Kotlin
val signatureSHA256 = Signature.getInstance("SHA256withRSA/PSS");
signatureSHA256.setParameter(PSSParameterSpec("SHA-256", "MGF1", MGF1ParameterSpec.SHA256, 32, 1));
val privateKey = loadPublicKey("MY_KEY")
signatureSHA256.initSign(privateKey);
val data: ByteArray = "name_of_the_file".toByteArray()
signatureSHA256Java.verify(data)
```


### **The extra mile**

The downloaded certificate can be also easily intercepted by a potential attacker using [Charles](https://www.charlesproxy.com/). There is also a library called [Objection](https://github.com/sensepost/objection), which totally bypasses certificate pinning. If you are not using certificate pinning in Android, this should be your next Pull Request tomorrow: it is really easy, and certainly avoid problems. You just need to add a _network_security_config.xml_ file with the following content:

```Xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config>
        <domain includeSubdomains="true">example.com</domain>
        <pin-set expiration="2018-01-01">
            <pin digest="SHA-256">7HIpactkIAq2Y49orFOOQKurWxmmSFZhBCoQYcRhJ3Y=</pin>
            <!-- backup pin -->
            <pin digest="SHA-256">fwza0LRMXouZHRC8Ei+4PyuldPDcf3UKgO/04cDM1oE=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

Android can also generate a pair of pub/private keys on the device. This needs to be of course handled, but also adds another world of possibilities — if the keys are created in real-time, then we are slightly on the safer side. Of course, we are still handling problems with the transmission of the keys and securing them, but we have probably removed a few existential threats from the equation:


```Kotlin
private lateinit var keyPair: KeyPair

private fun generateKey() {
    val startDate = GregorianCalendar()
    val endDate = GregorianCalendar()
    endDate.add(Calendar.YEAR, 1)
    
    val keyPairGenerator: KeyPairGenerator = KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_RSA, ANDROID_KEYSTORE)

    val parameterSpec: KeyGenParameterSpec = KeyGenParameterSpec.Builder(KEY_ALIAS,
        KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY).run {
            setCertificateSerialNumber(BigInteger.valueOf(777))       //Serial number used for the self-signed certificate of the generated key pair, default is 1
            setCertificateSubject(X500Principal("CN=$KEY_ALIAS"))     //Subject used for the self-signed certificate of the generated key pair, default is CN=fake
            setDigests(KeyProperties.DIGEST_SHA256)                         //Set of digests algorithms with which the key can be used
            setSignaturePaddings(KeyProperties.SIGNATURE_PADDING_RSA_PKCS1) //Set of padding schemes with which the key can be used when signing/verifying
            setCertificateNotBefore(startDate.time)                         //Start of the validity period for the self-signed certificate of the generated, default Jan 1 1970
            setCertificateNotAfter(endDate.time)                            //End of the validity period for the self-signed certificate of the generated key, default Jan 1 2048
            setUserAuthenticationRequired(true)                             //Sets whether this key is authorized to be used only if the user has been authenticated, default false
            setUserAuthenticationValidityDurationSeconds(30)                //Duration(seconds) for which this key is authorized to be used after the user is successfully authenticated
            build()
    }

    //Initialization of key generator with the parameters we have specified above
    keyPairGenerator.initialize(parameterSpec)

    //Generates the key pair
    keyPair = keyPairGenerator.genKeyPair()
}
```

### Conclusions

As I stated in my previous article, absolute security does not exist. We are aiming to slow the inevitable process of a security breach, and in most economics we can’t pour unlimited resources to achieve security close to 100%. It always comes to a trade-off — invest reasonable resources to ensure a reasonable degree of protection.

I write my thoughts about Software Engineering and life in general in my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share it, ♥ it and/or leave a comment. This is the currency that fuels amateur writers.
