---
title: "From Java to Kotlin and back (III): Calling Java from Kotlin"
author: "Enrique López-Mañas"
date: 2021-03-14T07:41:42.797Z
lastmod: 2025-06-09T09:50:10+02:00

description: ""

subtitle: "This article is part of a series. You can find the remaining article of the series here:"

image: "/articles/2021-03-14_from-java-to-kotlin-and-back-iii-calling-java-from-kotlin/images/1.jpeg" 
images:
 - "/articles/2021-03-14_from-java-to-kotlin-and-back-iii-calling-java-from-kotlin/images/1.jpeg"


aliases:
    - "/from-java-to-kotlin-and-back-iii-calling-java-from-kotlin-f33f5c246d69"

---

This article is part of a series. You can find the remaining article of the series here:

[From Java to Kotlin and back (I) — Calling Kotlin from Java](https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-i-java-calling-kotlin-9abfc6496b04)

[From Java to Kotlin and back (II): Calling Kotlin from Java](https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-ii-calling-kotlin-from-java-3bdf72da6e52)

In this last chapter of the series, we will evaluate consideration when calling Java code from Kotlin.

One could argue that even in this situation happens often, keeping considerations in mind for some code that might legacy is not that practical. Kotlin has also been designed with interoperability in mind, so Java code from Kotlin is much more “callable” than the other way around, since the design has been in mind since its conception. However, there are a few points that you can keep in mind when working on your Java code, and we would like to explain them in this article.

### Annotations

Since Java lacks a few of the powerful features we already have on Kotlin, we will rely significantly on some annotations that can prepare our Java code to interface with Kotlin.

#### Nullability

Whereas nullability is one of the core features in Kotlin, Java does not provide out-of-the-box support for it. Every parameter in Java should always have a nullability annotation. Otherwise, they are understood as “[platform types](https://p5v.medium.com/platform-types-in-kotlin-5caceeb556ad)”, which have an ambiguous way to determine nullability and can trigger runtime errors, pretty much what Kotlin nullability aims to avoid. For example, consider the following piece of code:




If we try to call the function _doNotUseAnnotation_ with false, the code will trigger an Exception. Because we didn’t add any annotation, Kotlin implies that the function is not nullable. In Java, we would be setting up the nullability as follows:




The most common ones that we will find are @Nullable and @NotNull, present in the package _org.jetbrains.annotation_ but also in _com.android.annotation_ and others, such as Lombok.

Generally, Java code that has not been properly annotated can lead to unpredictable behavior. If you have some experience in the Android realm, where the framework is written in Java, you will be constantly relying on annotations that are not all the time where they should be.

If you are working on Java code that will be potentially exposed to Kotlin, remember to use Nullability annotations to facilitate the lives on the other side of the fence.

#### @UnderMigration annotation

The @UnderMigration annotation is pretty useful when we are maintaining some Java code, and we want to inform our potential clients of its current status (please note that the annotation can be found in a separate artifact, _kotlin-annotations-jvm_)

@UnderMigration status can have three different values, similar to the [explicit API mode](https://blog.jetbrains.com/kotlin/2020/06/kotlin-1-4-m2-released/#explicit-api-mode) introduced in Kotlin 1.4:

*   `MigrationStatus.STRICT` will deliver a compilation error when there is a misusage of an annotation, causing the code to fail.
*   `MigrationStatus.WARN`: similar to the previous one, but just dropping a warning
*   `MigrationStatus.IGNORE` ignores completely the usage of the annotations.

### Getters and setters in Java

Kotlin uses property access instead of getters and setters, like Java. The definition of a getter is a no argument with a name starting with _get_, and the definition of a setter is a one-argument method with a name starting with _set_. Boolean getters start with is, so we can use a more natural human language to ask for the value of the property (_isClosed_, is _Finished_, etc). Keep this in mind when designing your Java class, although this is pretty much standard. Interestingly, if your attribute provides only a setter it will not be visible as a property, since Kotlin does not support set-only properties (and this is generally an [anti-pattern](https://softwareengineering.stackexchange.com/questions/50554/why-it-is-not-recommended-to-have-set-only-property)).

The following Java class:




will be accessed like the following block in Kotlin:




### Kotlin keywords

Kotlin has a few hard keywords that we should not be using in our Java code, since the Kotlin counterpart will need backticks to call them.




Protip: these backticks can be used all around when naming methods and variables in Kotlin, not only in the case of hard keywords or tests.




### Summary

This last article presents tips to design and work on our Java code when it will be later on consumed in Kotlin. Java code can expose code to Kotlin with lesser effort than the other way around, but the points explored will be able to help you achieve a more efficient interoperable code.

I write my thoughts about Software Engineering and life in general on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
