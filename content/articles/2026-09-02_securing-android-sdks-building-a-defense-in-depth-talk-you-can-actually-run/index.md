---
title: "Securing Android SDKs: Building a Defense-in-Depth Talk You Can Actually Run"
author: "Enrique López-Mañas"
date: 2026-09-02T09:00:00.000Z

description: "Notes on preparing a conference talk on Android SDK security, and the runnable companion code that came out of it."

subtitle: "Four layers, one request, and a repo to prove none of it is just slides."

---

I have spent the last few days polishing a conference talk called "Securing Android SDKs: A Defense-in-Depth". It is one of those subjects that sounds narrow until you start pulling the thread, and then you realize half the industry treats a single static API key as its entire security model.

The premise of the talk is simple. There is no single control that stops a determined attacker from reverse engineering your SDK, replaying your requests, or automating your endpoints with a fleet of emulators. What actually works are layering weak controls until the cost of breaking all of them exceeds what any rational attacker is willing to pay.

#### Four layers, one request

The talk walks through four layers, in order of how much they cost an attacker to defeat.

Obfuscation is the cheapest and buys the least. ProGuard, R8, or a commercial tool like DexGuard will rename your classes and strip constant strings out of the obvious places, but a patient reverse engineer with Frida attached to a live processes will eventually see everything a legitimate client sees. Obfuscation delays. It does not authenticate.

Request signing is the next step. An HMAC over a canonical string, including a nonce and a timestamp, proves a request was not tampered with in transit and rejects an exact replay. It does not prove the request came from your real app though, only that whoever holds the secret produced it, and a secret embedded in an APK is not really a secret.

Device attestation, on Android that means the Play Integrity API, is the layer that actually prove the client is real. I had to fix my own slide on this one after a first draft got the field semantics wrong. `deviceRecognitionVerdict` is a list, not a single tier, and a clean device can carry `MEETS_BASIC_INTEGRITY`, `MEETS_DEVICE_INTEGRITY`, and `MEETS_STRONG_INTEGRITY` at once. Checking it with `equals` instead of `contains` is a bug I have seen more than once.

Attestation is expensive to run on every request though, so the fourth layer, short lived session tokens, exist to spend that expensive proof once and let it pay for a whole session instead of a single call.

#### Slides are not proof

Halfway through building the deck I got tired of drawing boxes and arrows that claimed a replayed request gets rejected. I wanted something a person in the audience could clone and actually watch reject a replay, so I wrote `security-demo`, a small Kotlin JVM project with no Android SDK or emulator dependency at all.

```Kotlin
val goodRequest = RequestSigner.sign("POST", "/v1/event", body, secret)
println(RequestSigner.verify(goodRequest, secret, seenNonces))
println(RequestSigner.verify(goodRequest, secret, seenNonces)) // same nonce, rejected
```

`./gradlew run` spin up a real `HttpServer` on localhost, walks through a signed request, a replay, a session token that expires after five seconds, and a re-attest that gets a fresh one. Play Integrity itself obviously cannot run outside a real device with Google Play Services, so that one layer represented by an interface and a mock, with the real Android client code sitting uncompiled in a reference file for anyone who wants to lift it directly later. The repo is Apache 2.0 and public, on my [GitHub](https://github.com/kikoso/security-demo) if you want to try and break it yourself.

#### The popup that would not open

The deck itself has a small feature I am fond of: a presenter mode. Press a key and a second window opens with your speaker notes, a running clock, and a preview of what is comming, synced live to whatever slide is on the main screen, the same trick Keynote and Google Slides do across two monitors.

I wired this with `window.open` and the browser's `storage` event, tested it locally, and it worked beautifully. Then I published it, clicked the button in the actual viewer, and absolutely nothing happened. No error, no console warning, just silence. It turns out the sandboxed iframe that host a published artifact blocks popups unconditionally, script triggered or not, link click or not, right click included. There was no workaround from inside the page. The fix was to hand myself the raw HTML file and open it as a normal local page, where a browser behaves like a browser again.

It was a good reminder that a demo environment and a production environment are rarely the same thing, even when the code underneath is identical.

#### Conclusions

*   Obfuscation buys time. It does not buy trust.
*   Signing proves a request was not altered, not that it came from real client.
*   Attestation is the expensive proof that the client is real. Spend it once per session, not per request.
*   If you are going to claim a security property in a talk, write the code that let someone in the audience disprove you.

I write my thoughts about Software Engineering and life in general on my [Mastodon account](https://kotlin.social/@eenriquelopez). If you have liked this article or if it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
