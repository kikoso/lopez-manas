---
title: "A short story of randomness (I)"
author: "Enrique López-Mañas"
date: 2021-04-04T07:17:45.529Z
lastmod: 2025-06-09T09:50:11+02:00

description: ""

subtitle: "I have always been fascinated by the above comic strip. A discussion on randomness and determinism becomes as much a philosophical issue…"

image: "/articles/2021-04-04_short-story-of-randomness-i/images/1.jpeg" 
images:
 - "/articles/2021-04-04_short-story-of-randomness-i/images/1.jpeg"
 - "/articles/2021-04-04_short-story-of-randomness-i/images/2.png"


aliases:
    - "/a-short-story-of-randomness-i-17ca0718ae52"

---

I have always been fascinated by the above comic strip. A discussion on randomness and determinism becomes as much a philosophical issue as it is a practical one. They are used in a variety of applications: from the obvious cryptography, gaming or gambling to the less evident politics or arts.

How can we be sure that a number is random? Will observing the process mine our efforts on generating the random number, similar to the observation of a cat inside a box with a decaying radioactive atom? Despite the potential complexity of generating random numbers, we can provide an initially simple method to generate them.

When I participate in meetups or conferences as an organizer, there is one simple game I like to practice at the end of the session, and it is developing a script together with the audience that selects a random participant eligible for a gift (a cup, a t-shirt, etc… any swag generally provided by the hosting organization). The list of participants usually comes in a .CSV file, and coming from the Java world live-coding this can be a daunting task: opening streams, closing them… Damn, I am myself scared of even trying this on stage. However, in Kotlin the solution is rather simple:

```Kotlin
File("path/to/file.csv").readLines().
                         get(Random.nextInt(File("path/to/file.csv").readLines().size)
```


(except the part of guessing how to specify the path, which is impossible to get right at the first try).

While playing this little game, very often the name of a participant comes up twice, so we jokingly express our doubts on whether the process is being truly random, or the randomness algorithm has been tweaked to favor one individual and let him/her go back home with all the swag. Developing on stage an algorithm that is able to provide a random number might require more time than using _java.util.Random_. However, we can dive into it before the stage event, and understand how randomness is implemented in Java.

[OpenJDK](https://hg.openjdk.java.net/jdk8/jdk8/jdk/file/tip/src/share/classes/java/util/Random.java) provides the open-source code of _java.util.Random_, and it is quite interesting to see how it works. It uses a [48-bit LCG generator](https://en.wikipedia.org/wiki/Linear_congruential_generator), based on the chapter of [The Art of Computer Programming](https://www.informit.com/articles/article.aspx?p=2221790) by Donald Knuth. An LCG generator uses a formula similar to the following one:

![image](/articles/2021-04-04_short-story-of-randomness-i/images/2.png#layoutTextWidth)
LCG generation formula



Let’s take a look at each component in this formula:

*   _Xn_ is our starting seed, which should be unpredictable enough. For instance, it could be the amount of time that has passed since our system started, or the amount of RAM currently being used, or a XOR of the current Date.
*   _a_ is a multiplier — randomly selected
*   _c_ is an increment- randomly selected
*   m is the number we use to execute the modulo operation- fixed and randomly selected

The selection of the previous values may affect the quality or randomness of the output, so we can go down the rabbit hole and increase the entropy for those selected values (by either making them random as well or using a more convoluted process to generate them). In fact, Java generates the above parameters from rand48, so they get as random as it is acceptable for most usages.

The following code excerpt is an implementation in Kotlin of a linear congruential generator:

```Kotlin
  fun generateRandomNumber(range: Int) : Int {
        val random = System.currentTimeMillis()
        val multiplier = 0x9393DL
        val increment = 0x8763
        return (((random*multiplier)+increment) % range).toInt()
    }

   fun main() {
        println(generateRandomNumber(9))
   }
```

LCG is fast and apt for most computers to be used. Require minimal memory, and it can execute fast. However, its usage is not intended in every field (for instance, cryptographic applications should use secure pseudorandom number generators for salt and key generation).

### Summary

Most of the randomness generators created since the early computing days use some sort of variation of the abovementioned mechanism. However, its usage is not apt for all systems. In the upcoming article, we will see which systems should use a different random numbers generator, and which algorithms are currently available for that.

I write my thoughts about Software Engineering and life in general on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
