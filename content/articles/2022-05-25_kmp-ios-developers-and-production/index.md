---
title: "KMP, iOS Developers and Production"
author: "Enrique López-Mañas"
date: 2022-05-25T11:25:07.751Z
lastmod: 2025-06-09T09:50:19+02:00

description: ""

subtitle: "Kotlin Multiplatform (or KMP, KMM Mobile, etc) has been widely used for a number of years in applications that are currently in production…"

image: "/articles/2022-05-25_kmp-ios-developers-and-production/images/1.jpeg" 
images:
 - "/articles/2022-05-25_kmp-ios-developers-and-production/images/1.jpeg"
 - "/articles/2022-05-25_kmp-ios-developers-and-production/images/2.png"
 - "/articles/2022-05-25_kmp-ios-developers-and-production/images/3.png"
 - "/articles/2022-05-25_kmp-ios-developers-and-production/images/4.png"
 - "/articles/2022-05-25_kmp-ios-developers-and-production/images/5.png"
 - "/articles/2022-05-25_kmp-ios-developers-and-production/images/6.png"
 - "/articles/2022-05-25_kmp-ios-developers-and-production/images/7.png"


aliases:
    - "/kmp-ios-developers-and-production-c754fa958d38"

---


Kotlin Multiplatform (or KMP, KMM Mobile, etc) has been widely used for a number of years in applications that are currently in production. JetBrains [compiled a website](https://kotlinlang.org/lp/mobile/case-studies/) listing some of the companies that are currently using KMP.

Since the advent of the mobile platforms we enjoy today, there has always been a certain market interest to push multiplatform technologies, such as Cordova, Xamarin, and others. With more or less success, those technologies aimed to provide a unified framework to develop multiple codebases, mostly focusing on the aspect of pricing (create code once, deploy multiple times).

![image](/articles/2022-05-25_kmp-ios-developers-and-production/images/2.png#layoutTextWidth)
Some of the frameworks that have paved the way for KMP in the past



There are however multiple considerations as to why the cost is not the only aspect that can benefit from maintaining a single codebase:

*   Quality increase: a single codebase is easier to maintain and audit. We do not longer need to develop several of them to be deployed on multiple platforms, so certain tasks tend to get easier, such as bug maintenance.
*   One single tech stack: hiring in tech is generally an arduous task. Senior engineers are difficult to find, and it is harder to convince them to change between companies unless a decent offer is provided. Keeping a single tech stack allows your company to focus on a tech stack that can be hired and maintained.
*   Feature teams: a common approach in mobile is to separate teams by platform (iOS, Android). Instead, an interesting approach is to create feature teams, that can focus on a given feature and develop know-how on how it works. This is an interesting long-term approach that can be considered under certain companies’ circumstances. Using a single technology stack makes this approach feasible.

KMP has a nice adoption curve in Android teams since the language and most of the tooling is shared. In fact, JetBrains carried out a [survey on KMP usage](https://blog.jetbrains.com/kotlin/2021/10/multiplatform-survey-q1-q2-2021/) during the first semester of 2021, and the results are quite satisfying. From the above-mentioned survey, these are my personal takeaways:

![image](/articles/2022-05-25_kmp-ios-developers-and-production/images/3.png#layoutTextWidth)
Almost half of KMM users (48.4%) share more than half of their codebase.


![image](/articles/2022-05-25_kmp-ios-developers-and-production/images/4.png#layoutTextWidth)
Satisfaction is close to 99%.



It would have been interesting to have a breakdown of the satisfaction based on the platform where KMP was used, where I suspect numbers would have differed. Particularly, iOS developers seem to have a harder time working with KMP for a variety of reasons.

This post aims to provide the drawbacks of currently applying KMP on production from the iOS side. KMP is a dynamic technology that evolves constantly (and JetBrains is a company that listens to its user base when releasing new software), so if you end up reading this article, keep in mind the date when this was written. Without any other prolegomenon, here there is a non-exhaustive list of some of the main challenges when using KMP on the iOS side of things:

### Debugging iOS

Currently, we have mainly two options to debug code on iOS: we can either use the [Xcode Kotlin Plugin](https://github.com/touchlab/xcode-kotlin/) from Touchlab (which can be installed on Xcode) or the [Kotlin Multiplatform Mobile for AppCode](https://plugins.jetbrains.com/plugin/17098-kotlin-multiplatform-mobile-for-appcode) (which can be installed on AppCode).

Touchlab is a fantastic company that has been doing a lot of good for the Kotlin and KMP communities. The Xcode Kotlin Plugin is not perfect, and nobody expects it to be. There are currently [reported issues](https://github.com/touchlab/xcode-kotlin/issues) with autocompletion, crashes with different Xcode versions, and more. This is intrinsic to the nature of being a third-party plugin developed for a language and stack that is not natively supported by Apple on its framework (and it will probably never be).

AppCode is the JetBrains IDE to develop Swift applications, and it is arguably a better IDE than the one provided by Apple. Until not too long ago, Xcode was unable to refactor Swift code, whereas AppCode was able to do it. It has better tooling, interface, and more. On the other side, it is not the official IDE from Apple, and it lacks some other things, like proper Interface design. As it stands today, no solution is perfect, and debugging KMP on iOS is still painful.

### Interoperability via Objective-C

KMP interacts with iOS via Objective-C, not Swift. The tool being used for that effect is [Cinterop](https://kotlinlang.org/docs/native-c-interop.html). This means that, if something is not supported on Objective-C, it does not matter whether Swift supports it or not. And there is a good number of examples of this. For instance, Exhaustive Enums, Default Arguments and others.

#### Exhaustive enums

Enums in Objective-C are represented as Integers, vs. reference types in Kotlin. If you try to switch over Enums on Swift, it would be like applying a switch on any other class: Swift is not aware that there is a finite number of numbers of instances for that Enum, as Kotlin does. There is a Feature Request filled for this [at YouTrack](https://youtrack.jetbrains.com/issue/KT-48068), so if you have interest feel free to take a look at it.

#### Default arguments

Default arguments (or arguments) in Swift are possible. For instance, the following function provides a default argument:

![image](/articles/2022-05-25_kmp-ios-developers-and-production/images/5.png#layoutTextWidth)


If we do not specify the parameter nice, the default will be taken instead:

![image](/articles/2022-05-25_kmp-ios-developers-and-production/images/6.png#layoutTextWidth)


Now, why can’t we use it on KMP, if Swift supports default arguments? Because (again), the interoperability happens via Objective-C. So default arguments cannot be used when using a KMP-generated artifact on iOS. Instead, arguments need to be specified.

### Lack of support from certain APIs

Codable is an API introduced with Swift 4 and used to serialize and deserialize data, for instance into or from a JSON format.

[kotlinx.serialization](https://github.com/Kotlin/kotlinx.serialization) provides this functionality for Kotlin, but you can’t directly generate a Codable implementation when exporting Kotlin classes to Swift (again, with a [YouTrack entry here](https://youtrack.jetbrains.com/issue/KT-48081)). Whereas it is technically possible to use [kotlinx.serialization](https://github.com/Kotlin/kotlinx.serialization) all along, it would be reasonable to expect a Codable implementation when using KMP, being the framework of reference on iOS. You can imagine a team of Swift developers having certain doubts about adopting KMP when they will not be unable to use Codable.

### Support for native dependencies is limited

Kotlin/Native provides integration with the [CocoaPods dependency manager](https://cocoapods.org/), via the CocoaPods plugin and Cinterop tool. However, if you have a dependency that is as well dependent on another library, this is currently not supported by KMP ([YouTrack ticket](https://youtrack.jetbrains.com/issue/KT-38749)).

### Complex concurrency model

The [concurrency and memory model](https://kotlinlang.org/docs/multiplatform-mobile-concurrency-overview.html) at KMP is complex, and it eventually feels that it is mutually exclusive between iOS and Android. It is not uncommon to have changes that make one or the other platform crash. Until very recently, coroutines were in fact Single Threaded, and this only changed with the advent of 1.6.1-native-mt a month ago.

The issue of how frozen objects work, and how to work with immutable objects and so escalates quickly, and it can soon become a daunting task.

### Is then KMP ready for production?

KMP is ready for production, and the case studies of JetBrains prove it.

![image](/articles/2022-05-25_kmp-ios-developers-and-production/images/7.png#layoutTextWidth)


Like with any other technology at the edge of possibility, an exercise of caution is always positive. KMP relies on too many edges and platforms over which JetBrains have no control at all, so expect versions to get broken when new Android or iOS versions are released, as well as with new Swift versions. Over time, I got to collect a checklist that I aim to apply on any project before going too wild on KMP:

*   **Use it with caution:** there is no need to go 100% KMP. A modularized project will allow you to perform experiments on smaller modules and evaluate whether you can benefit from KMP or not.
*   **Shared components:** very likely your purpose to use KMP is to share components between platforms, so before starting using it check which components are more convenient to share in your project. Identifying a codebase that can be shared (and subsequently, determine whether KMP has been useful or not) is a gentle and thoughtful approach.
*   **Keep versioning in mind:** Kotlin/Native changed its versioning at some point in history, and now it is bonded to the version of Kotlin itself. However, JetBrains [maintains a website](https://kotlinlang.org/docs/components-stability.html) with the current stability of Kotlin Components, and as of today some of the Kotlin/Native components are Beta. Apply your own casuistry here, and determine whether the stability of KMP is good enough for your organization.

Thanks to the JetBrains crew from Munich that is always so helpful with feedback and support, and specifically [Eugene Petrenko](https://medium.com/u/bb64abb34cdb) and [Sebastian Sellmair](https://medium.com/u/5f96be1c477d). Like always, thanks [Marton Braun](https://medium.com/u/ec2087b3c81f) for your review. You guys rock!

I write my thoughts about Software Engineering and life in general on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
