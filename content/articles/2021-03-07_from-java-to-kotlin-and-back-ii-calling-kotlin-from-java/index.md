---
title: "From Java to Kotlin and back (II): Calling Kotlin from Java"
author: "Enrique López-Mañas"
date: 2021-03-07T03:54:01.508Z
lastmod: 2025-06-09T09:50:08+02:00

description: ""

subtitle: "In the previous article, we explored how Java and Kotlin can interact with each other, and some considerations in this regard. In this…"

image: "/articles/2021-03-07_from-java-to-kotlin-and-back-ii-calling-kotlin-from-java/images/1.jpeg" 
images:
 - "/articles/2021-03-07_from-java-to-kotlin-and-back-ii-calling-kotlin-from-java/images/1.jpeg"


aliases:
    - "/from-java-to-kotlin-and-back-ii-calling-kotlin-from-java-3bdf72da6e52"

---

![image](/articles/2021-03-07_from-java-to-kotlin-and-back-ii-calling-kotlin-from-java/images/1.jpeg#layoutTextWidth)
This article is part of a series. You can find the remaining article of the series here:

[From Java to Kotlin and back (II): Calling Kotlin from Java](https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-ii-calling-kotlin-from-java-3bdf72da6e52)

[From Java to Kotlin and back (III): Calling Java from Kotlin](https://enriquelopezmanas.medium.com/from-java-to-kotlin-and-back-iii-calling-java-from-kotlin-f33f5c246d69)

In the previous article, we explored how Java and Kotlin can interact with each other, and some considerations in this regard. In this second edition, we will keep reflecting on some relevant aspects to consider when Java is calling Kotlin.

### Properties in classes

Likely the first Kotlin feature highlighted when we heard about the language, data classes. Data classes are mainly thought to hold data with some extra functionality allowed, and hence called Data classes. We like them because they automatically generate some functions (getters, setters, `toString()`, `copy()`, `equals()` and `hashCode()`), which otherwise we need to manually create. For instance, a data class containing just `var name : String` will compile into the following in Java:


Data class compiled in Java



If the name of the var starts with is, then the resulting getter will start with the prefix is. For instance. if we have `var isYoung: Boolean`, the resulting setter will be:


Resulting setter of an “is” attribute



Keep in mind that this does not only work for boolean types, but for any type.

### Naming with JvmName

We explored in the previous article some usages for `@JvmName`, and I would like to provide some more ideas.

For instance, whereas Kotlin supports Optional values, in Java we do not really name it that way. So if we are designing extension functions that might be called for Java, we might want to provide them a different name so they are idiomatic enough for our Java code. Let’s check the following code:


Kotlin class with idiomatic naming



`asOptional `will likely confuse our Java peers, and what they are looking for underneath is whether a variable is potentially nullable or not. Hence, we specify `@JvmName(“ofNullable”)`, to change the resulting JVM name. This will be called as follows in Java:


Java calling JvmName function



Note also that Java can access the different types of the sealed class.

### Default methods in Java interface

Since Java 1.8, Java interfaces can contain default methods. Without getting too much into detail, they enable you to add new functionality to an existing interface, ensuring compatibility with code written for older versions of those mentioned interfaces. The [following link](https://docs.oracle.com/javase/tutorial/java/IandI/defaultmethods.html) explains in detail how they work.

If we want to make all non-abstract members of a Kotlin interface becoming default for any Java class that implements them, we need to compile the code with the following option:

`-Xjvm-default=all`

Let’s see this in practice. Consider the following interface with a default method and that we are compiling with `-Xjvm-default=all`:


Default interface Kotlin



This will be implemented in a Java class as follows:


Java class implementing default interface



And of course, Java will be able to call all the functions of the interface:


Java class calling default methods



An interesting tweak is that, of course, Java can also override all the default functions. So if in our example, `functionA()`needs to have a custom implementation in the class implementing it, we can safely override it.

### Getter and Setter renaming

Occasionally we might want to rename our getters and setters. A typical case is when returning an attribute can be composed by operations on some other attributes (for instance, something like returning a name with `getName()` that adds some sort of prefix or evaluation to determine the complete string being returned). We can easily do it with the annotations `@get:JvmName` and `@set:JvmName`as follows:


Changing getters and setters



### Null-safety

Kotlin is null-safe, Java is not null safe. When we are calling Kotlin functions from Java we can always pass a `null` as a non-null parameter. Kotlin generates runtime checks for all public functions that expect non-nulls. This provokes a `NullPointerException` in the Java code immediately. Be mindful when defining nullable and non-nullable parameters in functions, since what in Kotlin is a pleasant experience might become a party of runtime Exceptions in your Java code.

### Using the type Nothing in Java

Or technically, not using it, since there is no natural counterpart in the Java world. In fact, it is interesting because java Void accepts null, but Nothing doesn’t. It is in fact a complex problem in Computer Science that we can philosophically tackle in another tackle, since we are trying to represent nothing with something, and we are biological creatures that deal with physical manifestation of items in our world. Leaving nothingness aside, the Nothing type gets represented with a raw type in Java, so keep this in mind when working with Nothing:


Nothing in Java



### Summary

This article has explored some more tips on calling Kotlin code from Java. The following article of the series will explore the reverse side of the river, and we will learn how Kotlin can code with legacy Java code, and which considerations we need to keep in mind.

I write my thoughts about Software Engineering and life in general on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
