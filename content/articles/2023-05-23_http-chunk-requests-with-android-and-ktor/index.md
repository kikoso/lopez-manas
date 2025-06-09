---
title: "HTTP chunk requests with Android and ktor"
author: "Enrique López-Mañas"
date: 2023-05-23T04:26:12.260Z
lastmod: 2025-06-09T09:50:30+02:00

description: ""

subtitle: "In this very short article, I will explain briefly what is a chunk or streamed HTTP request, what are the benefits of using it, and how it…"

image: "/articles/2023-05-23_http-chunk-requests-with-android-and-ktor/images/1.jpeg" 
images:
 - "/articles/2023-05-23_http-chunk-requests-with-android-and-ktor/images/1.jpeg"
 - "/articles/2023-05-23_http-chunk-requests-with-android-and-ktor/images/2.png"
 - "/articles/2023-05-23_http-chunk-requests-with-android-and-ktor/images/3.png"


aliases:
    - "/http-chunk-requests-with-android-and-ktor-f24bb9b0056c"

---


In this very short article, I will explain briefly what is a chunk or streamed HTTP request, what are the benefits of using it, and how it works in Android.

Android apps use HTTP requests to download data from a backend. This information is stored and processed on the app to make it functional.

HTTP requests are executed using different frameworks on Android. The most common ones are Retrofit or OkHttp.

Simplifying the underlying network operations, and after identifying the IP address of the computer hosting the requested URL, an HTTP request looks like follows:


```
OkHttpClient: --> GET https://api.yourserver.com/sandbox/v1/example/23aa13d2-b161-432d-a67e-c50e8783f7dd http/1.1
OkHttpClient: X-apikey: AATR1oqYAZzp6o6ndALfIk6GG1dOcDED
OkHttpClient: Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRw...
OkHttpClient: Accept-Language: en-US
OkHttpClient: Connection: close
OkHttpClient: Accept: application/json
OkHttpClient: Accept-Charset: UTF-8
OkHttpClient: User-Agent: Ktor client
OkHttpClient: Host: api.yourserver.com
OkHttpClient: Accept-Encoding: gzip
OkHttpClient: --> END GET
```

The HTTP request contains (among others) the following fields:

*   The HTTP method used: GET, POST, PUT, PATCH or DELETE. There are actually 8 different HTTP methods, being the remaining ones CONNECT, OPTIONS and TRACE.
*   Authorization headers (things like an API Key, or the Auth key we will need to identify ourselves as lefit clients).
*   Metadata headers for encoding, language, charsets, content type, etc.

The full specification of the HTTP 1.1 protocol can be found in the [RFC 2616](https://www.ietf.org/rfc/rfc2616.txt), whereas the HTTP 1.0 specification can be found in the [RFC 1945](https://www.ietf.org/rfc/rfc1945.txt).

In a world where multiple SDKs provide us with an abstraction layer and simplify those operations, RFCs might not be needed to check often. Android developers, for instance, can benefit from the usage of multiple frameworks (Retrofit, OkHttp, Ktor, etc…) that provide already all of the required implementations. This was not always like that: in previous times, it was necessary to check RFCs with certain frequency, since feature-complete SDKs where not always available on each stack.

Executing standard HTTP requests works at a high level as follows:

![image](/articles/2023-05-23_http-chunk-requests-with-android-and-ktor/images/2.png#layoutTextWidth)


When the backend has processed the request, it returns it at once to the client. This works for most cases, but there are cases where we want to optimize further.

Imagine an endpoint that contains a complex logic that eventually takes more time until the full data is ready. Or maybe the endpoint relies on further subqueries to prepare the entire data, which will take some time until it is ready. In this case, it might be worth considering a Chunk (or streamed) request.

HTTP Streaming is a data transfer technique that allows a backend to continuously send chunks of data to a client over a single HTTP connection that remains open indefinitely (or until the data has been processed). A request like this can be of advantage to allow a client to dispose immediately of certain data, while the backend processes the rest.

This might remind the reader of using Sockets. HTTP and Sockets work similarly, although there are a few differences between them.

*   Websockets are event-driven, whereas HTTP is not. Generally, the best choice for real-time communication is sockets, since they have a lesser overhead to initialize and maintain a connection.
*   Sockets are a full-duplex asynchronous messaging mechanism. Both client and server can exchange messages independently.

There are also a few more differences in how they operate at the network level. This falls out of the scope of this article, but if you are interested you can read the [Wikipedia article](https://en.wikipedia.org/wiki/OSI_model) that explains the OSI model.

However, there might be cases where it is more convenient to use an HTTP Streamed request. From infrastructure to reusing certain models already being handled by the HTTP client, the casuistic can be wide.

Ktor supports this relatively out-of-the-box. The following snippet is able to execute a streamed request from a given API:

```Kotlin
fun main() {
    val client = HttpClient(CIO)
    val file = File.createTempFile("files", "index")


    runBlocking {
        client.prepareGet("https://api.example.com").execute { httpResponse ->
            val channel: ByteReadChannel = httpResponse.body()
            while (!channel.isClosedForRead) {
                val packet = channel.readRemaining(DEFAULT_BUFFER_SIZE.toLong())
                while (!packet.isEmpty) {
                    val bytes = packet.readBytes()
                    file.appendBytes(bytes)
                    println("Received ${file.length()} bytes from ${httpResponse.contentLength()}")
                }
            }
            println("A file saved to ${file.path}")
        }
    }
}
```


To verify that this is working, you can execute a cURL against the streaming API, using a command similar to the one below:

```
curl --location --request GET 'https://api.example.com' --header 'X-apikey: yourAPIkey' --raw

```


When you execute this, there is an interesting twist in the story. You will be able to see the response from the backend as you normally see it, but this time each chunk will be separated by a number, specifying the size of the next chunk:

![image](/articles/2023-05-23_http-chunk-requests-with-android-and-ktor/images/3.png#layoutTextWidth)


As promised, this is not the longest article I’ve written, but I hope it provides some context on Streamed requests, and how they work — and eventually, you can get some inspiration to apply when for your project, in case you need them.

I write my thoughts about Software Engineering and life in general on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or if it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
