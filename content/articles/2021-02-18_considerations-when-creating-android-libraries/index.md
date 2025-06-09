---
title: "Considerations when creating Android libraries"
author: "Enrique López-Mañas"
date: 2021-02-18T13:39:09.931Z
lastmod: 2025-06-09T09:49:57+02:00

description: ""

subtitle: "If you are an Android developer, chances are you might have been working on your own Android libraries. A library is a useful way to…"

image: "/articles/2021-02-18_considerations-when-creating-android-libraries/images/1.png" 
images:
 - "/articles/2021-02-18_considerations-when-creating-android-libraries/images/1.png"
 - "/articles/2021-02-18_considerations-when-creating-android-libraries/images/2.png"


aliases:
    - "/considerations-when-creating-android-libraries-c80940d79ae"

---

If you are an Android developer, chances are you might have been working on your own Android libraries. A library is a useful way to create a reusable set of features that need to be integrated through different apps (or even different libraries).

A library is a self-contained package including code and resources required to execute some functionality. Importing a library in our Android app is the same process as importing a .JAR file in a Java app, except that for Android the library file has the extension .AAR, which extends for Android archive (however, Android apps can also import libraries with a .JAR extension). There are detailed guides on the Internet on how to create Android libraries, but in this article I would like to focus on some aspects that are more subjective, and not always defined in every guide. We will discuss today the following aspects:

*   Keeping in mind exposed functionality
*   Kotlin/Java interaction
*   Exposing resources
*   Transitive dependencies and strategies to solve them

### Keep in mind which functionality will be exposed

A library likely offers an interface to the user to access its functionality. Regardless of whether the particular library encapsulates UX functionality, some interface towards an API… there will also be some classes and methods that are not relevant to the end-user, and that they will likely be exposed. How to prevent this?

*   Use properly visibility modifiers. If you are using Java, tend to prioritise the default modifier **package private**. If you are using Kotlin, lend towards [**internal**](https://kotlinlang.org/docs/reference/visibility-modifiers.html) **** (this means that it will be visible for the module).
*   Sometimes, packages need to be transitively exposed. For instance, think of the following setup for a library we are working with:
![image](/articles/2021-02-18_considerations-when-creating-android-libraries/images/2.png#layoutTextWidth)
Library structure including a module using an internal model



**My library** has a dependency on **My module**, which is an internal module used by the library. My library needs to access some data from the module (let’s say, some internal models). We need to declare them as public. But then, every class that integrates the library will be able to access those models, which is rather uncomfortable.

You could name the package of the model as internal (for instance, **my.package.internal.models**). This is a common industry practice, and it *should* discourage the usage of those classes. For instance, [Retrofit] (https://github.com/square/retrofit/search?q=internal)or [OkHttp] (https://github.com/square/okhttp/search?q=internal)have the same naming for their internal classes.

Since Kotlin 1.4 there is an Explicit API mode, that enforces to operate on a short of library mode. In order to activate it, write the following on your Gradle file:
`kotlin {      
    // for strict mode       
    explicitApi()       
    // or     
    explicitApi = **&#39;strict&#39;**       

    // for warning mode      
     explicitApiWarning()       
    // or  
   explicitApi = **&#39;warning&#39;**   
}`

The setup is fairly straightforward: one mode will be strict and trigger errors, and the less strict mode will trigger warnings.

When the Explicit API mode is activated, visibility modifiers are required for declarations if the default visibility means they will be public. This will enforce visibility to be specifically declared.

### Kotlin/Java interaction

Kotlin should not be a strange word for you anymore. And this means that you should be aware of how Kotlin and Java interact with each other, and keep this in mind to ensure that the library can be called seamlessly. This means: you might be calling your Kotlin library from a Java codebase, or you might be calling your Java library from a Kotlin codebase. In those cases you will need to put an extra dose of attention, to improve the experience of the users implementing your library.

#### Package level functions

Since Java does not allow standalone functions outside classes, all the standalone functions or properties that you declare in a file **file.kt** will be compiled as static methods of a class called org.file.FileKt:
`// file.kt  
package org.file``class MyUtils``fun getLocale()`

This would compile in a Java class like the following:
`new org.file.MyUtils();  
org.file.AppKt.getLocale();`

Of course, having the classes automatically named is something that we want to avoid. By using the annotation `[@JvmName](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.jvm/-jvm-name/index.html) `we can specify the name of the destination class:


Using JvmName annotation



You can also use `file:JvmMultifileClass` to combine the top-level members from multiple files into a single class.

#### Instance fields

If you need to expose any underlying property in Kotlin to a Java class, use the annotation `[@JvmField](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.jvm/-jvm-field/index.html)`. This will make the property accessible from your Java class.

#### Functions with default parameters

When you define a function in Kotlin with default parameters, you don’t need to continuously pass them when you are calling that function. If they are not specified, the default value is taken.

Java does not support default parameters, so what happens when we call these functions in Java? By default, we need to specify all the parameters, and this does not scale well if you have been using default parameters in Kotlin. This is where we can use `@JvmOverloads`

Let’s consider the following fictional function in Kotlin:


Using JvmOverloads annotation



The function is using the annotation `@JvmOverloads,`and it also has two default parameters as arguments. From a Java point of view, this function will compile as follows:


How the function compiles in Java when using JvmOverloads



The advantages are obvious when we are dealing with long constructors that are using some default parameters, and that we do not need to specify again in our Java classes.

#### Nothing generics in Kotlin

A Kotlin type with a generic parameter `Nothing` is exposed as a raw type in Java. This should be avoided, since raw types are rarely used in Java.

#### Companion functions and constants

When Companion functions and constants are rawly compiled and accessed from Java, they are only available as instance methods on a static Companion field. For instance, the following Kotlin class:
`class KotlinClass {  
    companion object {  
        fun function() {``        }  
    }  
}`

is exposed as follows in Java:
`public final class JavaClass {  
    public static void main(String... args) {  
        KotlinClass.Companion.function();  
    }  
}`

Using a `@JvmStatic` annotation for the function makes the compiled code cleaner:
`public final class JavaClass {  
    public static void main(String... args) {  
        KotlinClass.function();  
    }  
}`

For companion constants, is better to use the annotation`@JvmField`, since `@JvmStatic`creates a weird getter. For instance, consider the following companion constant:
`class KotlinClass {  
    companion object {  
        const val PI = 3.14  
    }  
}`

Annotating the companion value with `@JvmField`will result again in a Java code much more comprehensive:
`public final class JavaClass {  
    public static void main(String... args) {  
        System.out.println(KotlinClass.PI);  
    }  
}`

### Exposing resources

Something that some folks are not aware of is that, by default, all the resources in an Android library are public! This means that everything that is included in your **res** folder (images, drawables, strings…). It is somehow a convoluted and counterintuitive method, but in order to make all your resources private, you should define at least one resource as public.

A good practice is to make public only a string specifying the library name. Do this when you start developing your app, and you will not have to worry about the external visibility of your resources anymore (that is, unless you really want to make them public).


Exposing resources via XML



### **Be aware of transitive dependencies**

Libraries might depend on external dependencies, and ideally you want to deliver all of them within the same .AAR. Otherwise, the user will need to manually include them, and this is complicated to handle.

On the other hand, we might be enforcing the user to include certain libraries that might conflict with the ones included at their app level.

There is no silver bullet here, and a few strategies to solve this issue.

#### Include all the transitive dependencies

A. AAR file can be generated including all the dependencies it needs. This is not done automatically out of the box by the .AAR file, and needs to be somehow hacked.

You can add and call a Gradle task that copies all the dependencies into the .AAR when this is packed:
``task copyLibs(type: Copy) {  
    from configurations.compile  
    into &#39;libs&#39;  
}``

There is a facilitation plugin, [fat-aar](https://github.com/kezong/fat-aar-android), that ameliorates this task. It does a few more things, but I found it a bit unstable (by the time I have to release a new library version, a new Gradle version is also available that generally breaks the plugin).

#### Strategies to force or remove dependencies

Also known as hell. Let’s say that your main app includes a **RandomLibrary** version 2.1. The app needs to include your **FancyLibrary**, which includes the version 3.1 of **RandomLibrary**, with a lot of breaking changes. You might need to force the resolution of a particular version, or remove some libraries from the build. In projects heavily modularised this can exponentially increase the complexity of your build script.

The following Gradle lines can exclude a library from the build:
``implementation(&#39;com.package.fancylibrary:1.0.0&#39;) {  
  exclude group: &#39;com.package.randomlibrary&#39;, module: &#39;randommodule&#39;  
}``

**Summary**

Designing and writing a library is more than packaging a few classes. Ideally, a phase of design needs to take place where you think about the structure and classes’ organization. Your company structure will affect this heavily as well (Do you have different teams working on different modules? Do you have an open repository policy? Do you have any restrictions to use external libraries? How much politics influence your development work?)

Thanks [Florina Muntenescu](https://medium.com/u/d5885adb1ddf), [Marton Braun](https://medium.com/u/ec2087b3c81f) and [Marius Budin](https://medium.com/u/a8c7d12ff9c1) for the review, you rock.

I write my thoughts about Software Engineering and life in general on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
