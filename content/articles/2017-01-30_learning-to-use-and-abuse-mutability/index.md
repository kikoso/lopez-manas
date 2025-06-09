---
title: "Learning to use and abuse Mutability"
author: "Enrique López-Mañas"
date: 2017-01-30T10:12:37.224Z
lastmod: 2025-06-09T09:48:35+02:00

description: ""

subtitle: "I am an old Java man, I never allocated many of my thoughts to reflect on the philosophy of mutability. In Java, unlike in other languages…"

image: "/articles/2017-01-30_learning-to-use-and-abuse-mutability/images/1.jpeg" 
images:
 - "/articles/2017-01-30_learning-to-use-and-abuse-mutability/images/1.jpeg"
 - "/articles/2017-01-30_learning-to-use-and-abuse-mutability/images/2.jpeg"


aliases:
    - "/learning-to-use-and-abuse-mutability-b4c71576299"

---

I am an old Java man, I never allocated many of my thoughts to reflect on the philosophy of mutability. In Java, unlike in other languages, there is no precise control over what is mutable and immutable. I never thought of Java objects as having this feature. Instead, I would always refer to them as _“that Java class that has no setter”_. _“That Java class that cannot be modified once the value has been set up”_. A very non-scientific wording in an almost scientific world. Mutability is the default in imperative languages, and we just do not think a lot about it. There is a lack of awareness, and our minds work inertially on the paradigm we have learned.

![image](/articles/2017-01-30_learning-to-use-and-abuse-mutability/images/2.jpeg#layoutTextWidth)


Through my career I saw that many languages could distinguish between the mutability of a class. And this was cool, but since I never used it so much (I do have mostly worked on Android and J2EE) I let it go. It was not in my sphere of influence.

A year ago I started working with Kotlin. It has been a bright light in how I develop, and I use it and advocate for it when I can (I do also curate the [Kotlin Weekly](http://kotlinweekly.net), if you want to subscribe for a weekly dose). If you happen to develop for Android, you are likely doing it in Java. The version 1.0 of Java [was released in 1995](http://www.oracle.com/technetwork/java/javase/overview/javahistory-index-198355.html). That is right, 22 years ago. The world was a very different place back then, and Java was designed to tackle the challenges of that time. Smartphones did not exist as we know them. Neither phones were so commercially available as they are nowadays. When Java was released, Windows 95 was not even available to the public (yes, so old is Java). eBay just started.

I like to think of the IT wold as an analogy to the Stock Market. In the 1960s, General Motors was the dominant company, and nobody could compete against them. The US government even thought of forcing its breakup into small parts to avoid a huge monopoly. Today, General Motors survives thanks to a huge bailout as a walking zombie. In 1990s, nobody would have bet a dime on Apple. Today, Apple is the single largest global company.
> Today’s stars are tomorrow’s wrecks. Today’s fallen are tomorrow’s exciting turnarounds — J.L.Collins, [The Simple Path to Wealth](http://amzn.to/2kKBGB9)

Java has evolved through many patches and updates. I am not criticising the language: I do make a living by speaking Java — although I do not restrict myself only to it. But in the meantime, new stars are arising, and here I think of Kotlin. Straight to the point, Kotlin distinguishes between mutable and immutable collections. Out-of-the-box.

Recently, my colleague in the [Google Experts](https://developers.google.com/experts/) program [Mike Nakhimovich](https://medium.com/u/6ebfb5fe99f9) wrote the following in Twitter:

> [](https://twitter.com/refugeeMikhail/status/821427906878537729)


That also put my brain to work. I wrote recently a blog post, [“On properly using volatile and synchronized”](https://medium.com/google-developer-experts/on-properly-using-volatile-and-synchronized-702fc05faac2#.nitcvxkfz). I realised then Threading and Synchronization are hard. Oh man, many edge cases, many concepts colliding, so much abstraction. And this solution is an out-of-the-box solution. I used it sometimes, and I always saw it as a hack.

After this introduction, let’s explore the world of mutability in Java and all its perks. In order to tackle the problem more efficiently, let’s provide the following definition as an axiom:
> An immutable class is a class whose state cannot be changed once it has been created.

Easy peasy. If you are in the Java arena, now you can come up with a few clues of how to make a class immutable.

*   **All fields must be private**. This is another axiom of the OO programming paradigm. If a field is private, cannot be externally changed. If, as a bonus, is also final, you cannot accidentally change them.
*   **Do not provide a setter**. Combine this with the previous point. If the fields are private and there is no setter provided, this class fields will always remain the same.
*   **Subclasses should not be able to override methods**. Otherwise they can trick on our immutability. This is easy. Just declare the class as final.

Check in this example how it can look like:

```Java
public final class Star {

  /**
   * Final and private attributes
   */
  private final double mass;
  private final String name;
  private final Date dateOfDiscovery;
    
  public Star (double aMass, String aName, Date aDateOfDiscovery) {
     mass = aMass;
     name = aName;
     dateOfDiscovery = new Date(aDateOfDiscovery.getTime());
  }

  public double getMass() {
    return mass;
  }

  public String getName() {
    return name;
  }

  public Date getDateOfDiscovery() {
    return new Date(dateOfDiscovery.getTime());
  }
}
```


We have covered the theoretical part. Now we have formally put the knowledge in paper. What can we do now with this?

#### The good

*   Immutable objects can make life easier. An immutable object is automatically thread-safe, and it has no synchronization issues. Wow, big pro! They make concurrent programming safer and cleaner. Have you ever debugged a concurrent programming issue? Most of the bugs are due to sharing state between threads. Imaging just getting rid of it in a glimpse. Worth trying.
*   Immutable objects do not need a copy constructor or an implementation of clone. For the sake of simplicity.
*   Have you heard of the term failure atomicity, coined by Joshua Bloch in [Effective Java](http://amzn.to/2jJoq1V)? It means that when an immutable object throws any exception, it will never result with the object left in an indeterminate state. Big kudos.

#### The ugly

*   Making copies of objects in order to mutate them can drain our resources, specially when dealing with complex data structure. Also, changing objects with a distinct identity can be also more intuitive.
*   Our perception of the model world is based on mutable objects.

### What should I do?

I have heard that “mutability is the source of all evil”. I like to have multiple options, and not taking anything as a dogma. Multiple options means generally that you have a wider range of options to choose from.

In Effective Java, Joshua Block writes:
> “Classes should be immutable unless there’s a very good reason to make them mutable. If a class cannot be made immutable, limit its mutability as much as possible.”

Immutability can solve many problems and make your life easier, specially when it comes to working in a concurrent environment. However, it can over-engineer and make things more complex if you use it by default. So know your war, and apply the solution that fits more.

Thanks [Xavier Jurado](https://twitter.com/xavierjurado) and [David González](https://twitter.com/dggonzalez) for your input on the article!

I write my thoughts about Software Engineering and life in general in my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share it, like it and/or leave a comment. This is the currency that fuels amateur writers.
