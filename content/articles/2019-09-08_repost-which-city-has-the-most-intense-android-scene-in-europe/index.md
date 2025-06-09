---
title: "Re-post: Which city has the most intense Android scene in Europe?"
author: "Enrique López-Mañas"
date: 2019-09-08T02:20:53.802Z
lastmod: 2025-06-09T09:49:29+02:00

description: ""

subtitle: "I wrote this post originally 5 years ago. For a side project, I had to use the StackExchange data explorer again, so I decided to revisit…"

image: "/articles/2019-09-08_repost-which-city-has-the-most-intense-android-scene-in-europe/images/1.jpeg" 
images:
 - "/articles/2019-09-08_repost-which-city-has-the-most-intense-android-scene-in-europe/images/1.jpeg"
 - "/articles/2019-09-08_repost-which-city-has-the-most-intense-android-scene-in-europe/images/2.png"
 - "/articles/2019-09-08_repost-which-city-has-the-most-intense-android-scene-in-europe/images/3.png"


aliases:
    - "/re-post-which-city-has-the-most-intense-android-scene-in-europe-643361d0a058"

---

I wrote this post originally 5 years ago. For a side project, I had to use the StackExchange data explorer again, so I decided to revisit it and update the numbers.

[StackExchange Data Explorer](http://data.stackexchange.com/) is an open-source tool to run SQL queries against public data from [StackOverflow](http://stackoverflow.com/). Since StackOverflow is the biggest development forum of the world, there is surely a lot of information that companies can actually retrieve from their system in order to take some business decision (this is actually a brilliant place to apply [BigData](http://en.wikipedia.org/wiki/Big_data))

Moving now to different issues: I was discussing back in time with some event organizers the possibility of bringing an Android event from the USA to Europe. Since I do live in Munich I was trying to convince them that Munich was the choice. They were resilient about it, so I needed to prove with some data that Munich would be a really nice choice.

At this time, I was thinking about how could I use Data Explorer and BigData to support my thesis. I remember two times I used it before, to display the most active developers from [Barcelona](https://twitter.com/eenriquelopez/status/384946205320437761) (the city I lived before), [Munich](https://twitter.com/eenriquelopez/status/384949033136955392), and [the two cities](https://twitter.com/eenriquelopez/status/384964337934163968) combined. Something similar could be a valid approach. In the previous SQL queries, I was clustering the top developers from each city based on their contribution to questions tagged with the token “_android_“. So I could possibly group all the developers&#39; contribution from a certain city with questions tagged with the same token. I come over with this script:


[https://gist.github.com/kikoso/f7900d00b34ed15a987e1e5ade475b31](https://gist.github.com/kikoso/f7900d00b34ed15a987e1e5ade475b31)



I decided to search in Germany, Spain, Holland/Netherlands, France, Italy, United Kingdom, Poland and Sweden (not that Sweden is a big country in terms of population, but at that time I used to work with a bunch of Swedish colleagues and it was perfect timing to tease them). I did some little experiments to get rid of some nomenclature errors and statistical noise. After some refining, I came with the following result:

![image](/articles/2019-09-08_repost-which-city-has-the-most-intense-android-scene-in-europe/images/2.png#layoutTextWidth)

![image](/articles/2019-09-08_repost-which-city-has-the-most-intense-android-scene-in-europe/images/3.png#layoutTextWidth)


There is a major preponderance of cities from Germany and the UK, with 6 cities from different countries in the first 20 cities against 8 British cities and 6 Germans. Is not my purpose here to give a full sociologic analysis (i.e., many cities are from UK since StackOverflow is an English based community and there are other local communities in different countries — although 80% of the Internet documentation is English based), neither any sort of scientifical study. But it is fun to drag some conclusions.

Now we have a bunch of cities with some numbers. We still need to go through a normalization process (i.e., cities with more population will always have more UpVotes than cities with less population). Since StackOverflow does not provide statistics for cities population (is not either their task) I will correlate this values manually. Thus, I will assign to each city the factor that determines the relationship between UpVotes and population. To get the population value, I mostly used Wikipedia.

1.  London (🇬🇧): 4.891.062 / 8.136.000 = 0.60
2.  Berlin (🇩🇪): 1.856.766 / 3.748.148 = 0.49
3.  Paris (🇫🇷): 1.420.781 / 10.354.675 = 0.13
4.  Reading (🇬🇧): 1.420.037 / 218.705 = 6.4
5.  Munich (🇩🇪): 827.613 / 1.471.508 = 0.56
6.  Amsterdam(🇳🇱): 741.014 / 821.752 = 0.90
7.  Warsaw (🇵🇱): 620.152 / 1.777.972 = 0.34
8.  Cambridge (🇬🇧): 611.197 / 123.900 = 4.9
9.  Madrid(🇪🇸): 444.636 /3.223.334 = 0.13
10.  Hamburg (🇩🇪): 426.707 / 1.822.445 = 0.23
11.  Forest of Dean (🇬🇧): 381.560 / 85.957 = 4.4
12.  Lyon (🇫🇷): 361.775 / 513.275 = 0.70
13.  Frankfurt (🇩🇪): 355.810 / 736.414 = 0.48
14.  Barcelona(🇪🇸): 333.880 / 1.620.343 = 0.20
15.  Manchester (🇬🇧): 323.506 / 547.627 = 0.59
16.  Edinburgh (🇬🇧): 270.455 / 482.005 = 0.56
17.  Oxford (🇬🇧): 231.829 / 154.600 = 1.49
18.  Karlsruhe (🇩🇪): 226.842 / 307.055 = 0.73
19.  Ulm (🇩🇪): 225.458 / 122.636 = 1.83
20.  Bristol (🇬🇧): 189.779 / 535.907 = 0.35

And if we now sort it by the coefficient:

1.  Reading (🇬🇧): 6.4
2.  Cambridge (🇬🇧): 4.9
3.  Forest of Dean (🇬🇧): 4.4
4.  Ulm (🇩🇪): 1.83
5.  Oxford (🇬🇧): 1.49
6.  Amsterdam(🇳🇱): 0.9
7.  Karlsruhe (🇩🇪): 0.73
8.  Lyon (🇫🇷): 0.70
9.  London (🇬🇧): 0.60
10.  Manchester (🇬🇧): 0.59
11.  Munich (🇩🇪): 0.56
12.  Edinburgh (🇬🇧): 0.56
13.  Berlin (🇩🇪): 0.49
14.  Frankfurt (🇩🇪): 0.48
15.  Bristol (🇬🇧): 0.35
16.  Warsaw (🇵🇱): 0.34
17.  Hamburg (🇩🇪): 0.23
18.  Barcelona(🇪🇸): 0.20
19.  Madrid(🇪🇸): 0.13
20.  Paris (🇫🇷): 0.13

There is some very interesting information in this graph:

*   The result of UK cities is brilliant. [Reading](http://en.wikipedia.org/wiki/University_of_Reading), [Cambridge](http://en.wikipedia.org/wiki/University_of_Cambridge) and [Oxford](http://en.wikipedia.org/wiki/University_of_Oxford), famous for their universities, are all in the top 5. The top 3 is entirely occupied by British cities.
*   The Forest of Dean, a small region in England, scores third in the ranking. It would be interesting to determine the reasons, since there is no known university or industry in the town. Probably a top user from StackOverflow explains it.
*   For most of the cities, a value between 0 and 1 seems the norm.

After this sampling, Munich scores very average (although better in absolute terms). There are, however, a bunch of other different reasons to choose a place for a certain event (proximity to other places, infrastructures, communication, hosting prices, the global number of possible attendants, etc). But after this little experiment, I can only suggest to organizers to move to the Forest of Dean (even if I still think that Munich offers a great beer).

I write my thoughts about Software Engineering and Finance on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share it, ♥ it and/or leave a comment. This is the currency that fuels amateur writers.
