---
title: "From Java to Kotlin and back (I): Java calling Kotlin"
author: "Enrique López-Mañas"
date: 2021-02-27T14:15:22.129Z
lastmod: 2025-06-09T09:50:00+02:00

description: ""

subtitle: "Android developers are generally aware that Java can interact with Kotlin relatively seamlessly. Kotlin has been designed from the…"

image: "/articles/2021-02-27_from-java-to-kotlin-and-back-i-java-calling-kotlin/images/1.jpeg" 
images:
 - "/articles/2021-02-27_from-java-to-kotlin-and-back-i-java-calling-kotlin/images/1.jpeg"
 - "/articles/2021-02-27_from-java-to-kotlin-and-back-i-java-calling-kotlin/images/2.png"


aliases:
    - "/from-java-to-kotlin-and-back-i-java-calling-kotlin-9abfc6496b04"

---

This article is part of a series. You can find the remaining article of the series here:

[From Java to Kotlin and back (II): Calling Kotlin from Java](https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-ii-calling-kotlin-from-java-3bdf72da6e52)

[From Java to Kotlin and back (III): Calling Java from Kotlin](https://enriquelopezmanas.medium.com/from-java-to-kotlin-and-back-iii-calling-java-from-kotlin-f33f5c246d69)

I am currently working on a multi-module project that combines a variety of Java and Kotlin code, so I decided to publish my thought and notes as an article series. It will likely help me as a journaling practice, and hopefully can help other potential readers that end up here trying to find some tips while they are facing the same problem.

Android developers are generally aware that Java can interact with Kotlin relatively seamlessly. Kotlin has been designed from the beginning to fully interoperate with Java, and both JetBrains and Google have pushed in that direction. For instance, IntelliJ and Android Studio allow users to convert files from Java to Kotlin. The conversion is not always problem-free, but it generally does a good job.

![image](/articles/2021-02-27_from-java-to-kotlin-and-back-i-java-calling-kotlin/images/2.png#layoutTextWidth)
Converting from Java to Kotlin in IntelliJ-based IDEs.



Interoperability rules are key when we are working on projects that will require both languages to interact with each other. In Android, this is likely to happen frequently.

A typical example is an SDK, whose API might be called from a variety of apps. The SDK developers might want to write the library in Kotlin to take full advantage of the language, but End Users may be integrating the SDK into an app written in Java.

Another example is a single App with a diverse codebase. Since both Java and Kotlin can coexist on the same codebase, it is possible to have Kotlin and Java code coexisting for an undetermined period of time. This is especially possible given the trend towards modularisation in the Android ecosystem, where modules are developed by multiple teams which, although they are working on the same product, are operating independently from each other, all the way down to choice of language.

The interaction can happen in both directions: Kotlin code calling Java code, and Java code calling Kotlin code. Hence, it is important to keep some rules in mind to make the system work properly in both directions. In this first article of the series, I will focus on some tips we need to keep in mind when we are working on our Kotlin code and exposing it to Java (or when Java is accessing Kotlin code)

#### Use JvmName annotation

Let’s take a look at the following file, declaring a class and a function in Kotlin:


```Kotlin
package org.example

class MyClass

fun myFunction() {  }
```



When this file gets accessed from Java (and since myFunction is a top-level function), the required code must be written as follows:


```Kotlin
new org.example.MyClass();
org.example.FileKt.myFunction();
```



The class can be referenced using the package name, but the function must be referenced using the original file name with the suffix Kt (for instance, if the file is called File, we are referencing static methods of a Java class named FileKt, since top-level functions do not exist in Java).

Of course, this is uncomfortable. By using the annotation **JvmName**, we can make sure that we define the name of the resulting Java file:

```Kotlin
@file:JvmName("DemoFile")
package org.example

class MyClass

fun myFunction() {  }
```


Make sure you are properly using JvmName if you have a top-level function on a Kotlin file that will be potentially exposed to Java users.

JvmName is also interesting to avoid signature classes, which might happen when we are doing [type erasure](https://en.wikipedia.org/wiki/Type_erasure). For instance, check out the following piece of code:


```Kotlin
fun List<String>.transform(): List<String>
fun List<Int>.transform(): List<Int>
```

In Java those functions cannot be defined side by side, since the JVM signature is the same: same return type, belonging to the List class, same name (filterValid(Ljava/util/List;)Ljava/util/List;). The manual solution is to write different names, but the better solution is to use JvmName to change the name when it compiles to JVM:

```Kotlin
@JvmName("transformAString")
fun List<String>.transform(): List<String>
@JvmName("transformAnInt")
fun List<Int>.transform(): List<Int>
```


#### Use **JvmMultifileClass**

Another issue we might face frequently is to have multiple files being generated with the same Java name (think of common names such as Utils for a class). The compiler does not like this, and will throw an error. However, the annotation **JvmMultifileClass** allows the compiler to merge multiple classes into a single one with the same name. If you are working with a class that you believe will collide with the namespace of other classes when the Java file is generated, consider using **JvmMultifileClass.**


```Kotlin
@file:JvmName("Demo")
@file:JvmMultifileClass

package org.example

fun myFunction() { }
```


```Kotlin
@file:JvmName("Demo")
@file:JvmMultifileClass

package org.example

fun anotherFunction() { }
```

```Kotlin
// calling on Java
org.example.Demo.myFunction();
org.example.Demo.anotherFunction();
```



#### Using JVMOverloads

Kotlin includes a few nice features that allow us to write more idiomatic code. For instance, we can define default parameters, so the user does not need to specify them. Together with the parameter naming, names of functions are now much easier to read, and less error-prone. For instance, let’s check the following and hypothetical constructor for some sort of custom HTTP service:


```Kotlin
class Service constructor(
		private val name: String,
		private val host: String,
		private val clientId: String,
		private val redirectUri: String,
		private val basicAuth: String?,
		private val checkSSL: Boolean,
		private val authIntentBuilder: AuthIntentBuilder = MAuthCustomTabIntentBuilder(),
		private val randomGenerator: RandomGenerator = MSecRandomGenerator(),
		private val base64Coder: MBase64Coder = MBase64UrlSafeCoderImpl(),
		private val pkce: MPKCE = MPKCEImpl(randomGenerator)
)
view raw
```

Fields like name, host, etc… are likely to be unique for each instantiation of the constructor, but some others might not, and they might be as well complex to initialise (and we can’t always apply Dependency Injection to solve this problem). By declaring default parameters, we just need to specify the attributes without default values.

However, Java does not support default parameters, so a file in Java interacting with our Service will need to declare all the parameters. What a waste of time.

The annotation JvmOverloads comes here to the rescue:


```Kotlin
class MLoginService @JvmOverloads constructor(
		private val name: String,
		private val host: String,
		private val clientId: String,
		private val redirectUri: String,
		private val basicAuth: String?,
		private val checkSSL: Boolean,
		private val authIntentBuilder: MAuthIntentBuilder = MAuthCustomTabIntentBuilder(),
		private val randomGenerator: MRandomGenerator = MSecRandomGenerator(),
		private val base64Coder: MBase64Coder = MBase64UrlSafeCoderImpl(),
		private val pkce: MPKCE = MPKCEImpl(randomGenerator)
```



JvmOverloads orders the Kotlin compiler to generate overloads for this function that substitute default parameter values.

Of course, JvmOverloads works as well with functions:

```Kotlin
@JvmOverloads fun bar(integerVar : Int = 0, doubleVar: Double =0.0, stringVar : String = "A value"){
    println("integerVar=$integerVar, doubleVar=$doubleVar, stringVar = $stringVar")
}
```



If your Kotlin functions might be used in Java and you have default parameters, consider using JvmOverloads.

#### Visibility equivalence

In my [previous article](https://medium.com/google-developer-experts/considerations-when-creating-android-libraries-c80940d79ae), I wrote about considerations when developing libraries, and one of the topics that came up was the Strict Library mode in Kotlin 1.4. This method forces visibility modifiers if the default visibility means they will be public. You are probably well equipped if you activate this mode when you are developing a library in Kotlin, but nonetheless, you should be aware of the visibility equivalencies between Kotlin and Java.

*   `private` members in Kotlin are compiled into`private` members in Java
*   A top-level `private`declaration will be compiled into package-local declarations
*   `protected` stays as `protected`
*   `internal` declarations are`public` in Java.
*   `public` remains `public`

#### Exceptions

Unlike Java, Kotlin does not have checked exceptions. There are no checked exceptions at the JVM level. Let’s check the following file in Kotlin:

```Kotlin
package example

fun myFunction() {
    throw IOException()
}
```

From Java, we will call with a statement similar to the following one:


```Java
try {
  example.File.myFunction();
} catch (IOException e) { 
 //... 
}
```


This will drop a compile error in Java. Our function, `myFunction()` , does not declare anytime a `IOException`or any other sort of exception. If we want it to work in Java, we need to use the `[@Throws](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-throws/index.html)` annotation in Kotlin:

```Kotlin
@Throws(IOException::class)
fun myFunction() {
    throw IOException()
}
```

Bonus: It could be that a Kotlin function may throw any exception types, include catched exceptions independently from the `@Throws` annotations use. Check out [this article](https://jonnyzzz.com/blog/2018/11/22/proxy/) by my rocket scientist and colleague Eugene where he explores potential side effects.

#### Companion functions in Kotlin

We write companion functions in Kotlin when we need to write a function that can be called without requiring an instance of the class, but still having access to the internals of the same class. For instance, take a look at the following class:

```Kotlin
class MyKotlinClass {
    companion object {
        fun myFunction() {
        }
    }
}
```


If we need to use it in Java, the result is as follows:

```Kotlin
public final class MyJavaClass {
    public static void main(String... args) {
        MyKotlinClass.Companion.myFunction();
    }
}
```

If we use the `@JvmStatic` annotation, it will be exposed as a static method.

```Kotlin
class MyKotlinClass {
    companion object {
        @JvmStatic fun myFunction() {
        }
    }
}
```

And the resulting Java code:

```Kotlin
public final class MyJavaClass {
    public static void main(String... args) {
        MyKotlinClass.myFunction();
    }
}
```



If you are using companion functions, remember to tag them with the `@JvmStatic`annotation.

#### Companion constants

Related to the previous section, in the case of companion constants is better to use the annotation`@JvmField`, since `@JvmStatic`creates a weird getter. For instance, consider the following companion constant:


```Kotlin
class KotlinClass {
    companion object {
        const val PI = 3.14
    }
}
```



Annotating the companion value with `@JvmField`will result again in a Java code much more comprehensive:


Companion constant in Java



If you wonder how this looks like if we use the `@JvmStatic`annotation, this is the generated access for Java:


Companion constant using JvmStatic annotation



#### Summary

The following article presents some tips for interoperability between Java and Kotlin from the Kotlin perspective (i.e., how Kotlin code must prepare itself in order to facilitate efficient access to the Java side of things. In the upcoming article we will keep exploring what do we need to do on our Kotlin code.

Thanks [Eugene Petrenko] (https://twitter.com/jonnyzzz?lang=en)and [Nick Skelton](https://twitter.com/nshred) for your lovely feedback.

I write my thoughts about Software Engineering and life in general on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
