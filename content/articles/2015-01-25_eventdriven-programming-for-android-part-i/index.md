---
title: "Event-driven programming for Android (part I)"
author: "Enrique López-Mañas"
date: 2015-01-25T21:19:35.256Z
lastmod: 2025-06-09T09:47:46+02:00

description: ""

subtitle: "(This is the first article in a three-part series)"

image: "/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/1.png" 
images:
 - "/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/1.png"
 - "/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/2.png"
 - "/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/3.png"
 - "/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/4.png"


aliases:
    - "/event-driven-programming-for-android-part-i-f5ea4a3c4eab"

---

(This is the first article in a three-part series)

Although Android includes some event-driven features in its development, it is far away from being a pure event-driven architecture. Is this something good or bad? As in every issue with software development the answer is not easy: it depends.

First, let’s establish a definition for event-driven development. This is a programming paradigm where the flow of execution is determined by events triggered by actions (such user interaction, messaging from other threads, etc). In this sense, Android is partially event-driven: we all can think of the onClick listeners or the Activity lifecycle, which are events able to trigger actions in an application. Why I said it is not a pure event-driven system? By default, each event is bound to a particular controller, and it is difficult to operate besides it (for example, the onClick events are defined for a view, having a limited scope).

Wait, you are talking about a new programming paradigm. Adopting frameworks or methodologies has always a cost, could this bring any advantage? I say yes, and to show it I want to present some limitations with traditional Android development.

In many scenarios it will be easy to end up with a structure as the following diagram is showing:

![image](/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/1.png#layoutTextWidth)


_Activities_ can communicate with _Fragments_, _Fragments_ can send messages to another _Fragments_ and _Services._ There is a tight coupling of components, and applying changes can be expensive(*). This leads frequently to boilerplate code, interfaces that implement functions that need to callback and propagate through different layers… you probably know where I want to go. As the amount of code increases, the maintainability and good software engineering practices are decreasing.

How does event-driven programming apply here? Let’s represent another system proposal:

![image](/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/2.png#layoutTextWidth)


Conceptually, the represented system have an event bus. There are different entities subscribed to the Event Bus, and posting events or listening to events — being respectively a producer or a consumer. Any subscriber can perform an action without knowing the logic. Think about it. Think about particular possibilities: a Fragment could render again and update its screen without knowing the logic behind any operation, just knowing that an event took place. Think about the possibilities of decoupling code and having a clean, compartmentalized architecture.

Is this paradigm supported in Android? Well, partially. As mentioned, the SDK offers natively a reduced set of event handling techniques, but we we want to go further. There are some names I want to mention here:

*   [EventBus](https://github.com/greenrobot/EventBus/), from [greenrobot](http://greenrobot.de/). This library has been optimized for Android, and has some advanced features like delivery threads and subscriber priorities.
*   [Otto](http://square.github.io/otto/), from [Square](https://squareup.com/global/en/register). Originally a fork from [Guava](https://code.google.com/p/guava-libraries/), it has evolved and being refined to the Android platform.

Having tried both I prefer EventBus over Otto. Greenrobot [claims](https://github.com/greenrobot/EventBus/blob/master/COMPARISON.md) that EventBus is significantly better at performing than its pair, and provides an extra amount of features.

![image](/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/3.png#layoutTextWidth)

![image](/articles/2015-01-25_eventdriven-programming-for-android-part-i/images/4.png#layoutTextWidth)


The next article will explore how to implement basic functions in EventBus

(*) I deliberately like to use the word “expensive” when referring to “lot of time”. Thinking in economical terms is frequently more effective.
