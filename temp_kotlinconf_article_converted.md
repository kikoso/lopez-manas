The first day of the KotlinConf 2024 is over, and there has been a significant amount. After 5 years the conference happened again at The Bella Center in Copenhagen, a fantastic venue close to the historical center of the Danish capital.

The last two weeks have been intense, with the Google I/O announcing another set of relevant features for Android and Kotlin developers. Most notably, Google is now supporting KMP for Android development. This is not a surprise move, since Google has been slowly pushing KMP for many of their libraries and products. Having official support is, however, a confirmation of a direction that makes Android developers happy. We are no longer relying on uncertainty. Quite the opposite, we know that putting our time and effort on Kotlin Multiplatform is likely to pay dividends over the upcoming years.

Despite the sometimes errant strategy of Google supporting technology stacks, everything related to Kotlin and JetBrains has been fairly stable. Google announced support for Kotlin as a first citizen in the Google I/O 2017, and nowadays it is hard to understand Android development without Kotlin in the picture. Similarly, since the advent of Android Studio, Eclipse and other alternatives have quickly dissipated. We anticipate that Kotlin Multiplatform is going to follow a similar path, given previous trajectories, the investment Google is taking on, and the inherent advantages of Kotlin Multiplatform over other multiplatform frameworks.

Arguing why Kotlin Multiplatform is a better alternative for the foreseeable future deserves an entire article, so we will not *delve* too much into it (note: the usage of delve here has not been suggested by AI).

Without expanding ourselves too much, here is a sneak peek of some of the most relevant announcements today.

### The advent of Kotlin 2.0.0

This is the worst-kept secret by JetBrains, Kotlin 2.0.0 is now stable and released. The final artifact was uploaded this week to GitHub, and we had our fair share of beta announcements for a few months. Kotlin 2.0.0 comes with a bunch of goodies, and our attention is directed to the following:

#### New Compose and Gradle plugin

The Jetpack Compose compiler has now been merged into the Kotlin repository. There has been some speculation about the final reasons, but the most direct implication is that we do no longer need to juggle anymore to get the right version applied. The Compose Gradle plugin will be equal to the Kotlin version.

#### Visibility changes in Gradle

The new *@KotlinGradlePluginDsl* annotation will prevent the exposure of the Kotlin Gradle plugin DSL functions and properties to places where they should not be available.

#### Bumped minimum supported AGP version

Time to update your minimum AGP version to 7.1.3.

#### New JSON output format for build reports

Build reports now support a JSON format to analyze better compiler performance and other metrics. Easier to integrate it with other tools and in CI/CD environments.

#### Changes in the standard library

Like with other previous Kotlin versions, the standard library now is more stable and brings improved functionality.

For full information on the release, check out the [official page for announcements](https://kotlinlang.org/docs/whatsnew20.html#install-kotlin-2-0-0) and the [GitHub release page](https://github.com/JetBrains/kotlin/releases/tag/v2.0.0) with all the commits included.

### K2 compiler

Faster, shinier, more beautiful and more performant. A small step for humankind, a big step for us. If you haven’t tried yet K2 on your application it is time to use it now.

[View Gist on Medium](https://medium.com/media/09e269db94ff74734d3572116bdf9b36/href)

### Internal adoption of Kotlin at Google, Amazon, Meta and others

Google internal adoption of Kotlin is growing exponentially. Meta is moving relentlessly in its adoption after 5 years. Amazon keeps increasing the traffic from Kotlin SDKs. At this point you do not need formal proof of Kotlin being a relevant actor, but it is good to get a reminder that this is still the right choice in such a volatile world like the tech world.

![](https://cdn-images-1.medium.com/max/1024/1*Q7uOycYkZP5Gq-fUmO-_KA.jpeg)

### Compose Multiplatform gets more stable

Compose Multiplatform for iOS is now in Beta, whereas Compose Multiplatform for Web is now in Alpha. It has not yet hit the stable breaking point, but it is progressing towards it. Adopting a new technology is a long-term strategy from a planning standpoint: you do not want to start today with a framework or technology that it is going to be deprecated in a number of years. Despite Kotlin Multiplatform being officially a technology that supports the business layer, given JetBrains track I feel more confident using Compose Multiplatform than most of the other UI multiplatform frameworks in the market for a variety of reasons that we could well cover in another article.

### Fleet

Fleet is looking great, and we believe it might not be getting all the attention that it probably deserves. It is now incorporating cross-platform features, like debugging through multiple stacks (namely, combined Swift+Kotlin codebases), previews for Composables, etc. JetBrains is the company behind AppCode, an IDE that was able to refactor Swift Code while Xcode was unable to do it. Probably an IDE to keep an eye on.

### New Kotlin LLM

If you live in this world, you might have observed the rise of the AI. There are reasons to believe that there is part of a hype that might not live up to expectations. Especially clear was the case of the Google I/O, which should have been renamed to Google A/I. Most of the announcements were related to AI.

We specially like that JetBrains is moving in the AI space, but not falling into the all-AI trend. JetBrains has been training a new Kotlin LLM that will be integrated into a Power AI assistant and the demo we saw at the KotlinConf was great: code explanation, documentation, code improvement, bug fixing… It really seemed like a powerful tool. And again, it seemed also to fit perfectly well in the midst of other non-AI-related announcements.

This is our handpicked selection of topics for the KotlinConf 2024. We are looking forward to the second day.

Disclaimer: this article did not use AI and was written by humans
