---
title: "Event-driven programming for Android (part III)"
author: "Enrique López-Mañas"
date: 2015-02-08T18:32:14.129Z
lastmod: 2025-06-09T09:47:50+02:00

description: ""

subtitle: "(This is the third article in a three-part series)"

image: "/articles/2015-02-08_eventdriven-programming-for-android-part-iii/images/1.png" 
images:
 - "/articles/2015-02-08_eventdriven-programming-for-android-part-iii/images/1.png"
 - "/articles/2015-02-08_eventdriven-programming-for-android-part-iii/images/2.png"
 - "/articles/2015-02-08_eventdriven-programming-for-android-part-iii/images/3.png"


aliases:
    - "/event-driven-programming-for-android-part-iii-3a2e68c3faa4"

---

(This is the third article in a three-part series)

Previously, I have given an introduction to Event Driven programming with Android, and show some code to create a _HelloWorld Event-Driven_ application.

Now we are likely facing another problem: how can we easily scale an application using Event-Driven development without falling into a messy and unorganised code? In this article, I will provide a proposal architecture that serves to scale an application based on Event-Driven development, but that can also be used to create a more general type of applications.

I have been using this architecture for a while, and it has made a change. Using Events and an MVP pattern ensures that I can easily add features to an application. I have also reduced the period between refactoring and rewriting, so the software I write can actually live longer and with a better quality.

### A first term: MVP

MVP stands for Model View Presenter, and is a programming pattern that defines three basic entities to be implemented within a software system:

The **Model**: what to render

The **View**: how to render

The **Presenter**: handles the communication between the model and the view. The presenter updates the view with content from the model, abstracting the view of any complexity underneath.

![image](/articles/2015-02-08_eventdriven-programming-for-android-part-iii/images/1.png#layoutTextWidth)
Courtesy of WikiMedia



MVP (as well as other programming patterns) is a concept rather than a concept solid framework, so there are no strict rules about it. Android does not implement a pure MVP pattern, but contains some elements:

*   The user interface (Views) are defined in XML files.
*   We extend classes (Activity, Fragment) that inflate the views, and update them.

From all the components of the MVP pattern, the _presenter_ has no direct representation in Android. This is however an important component: imagine that tomorrow we need to retrieve our data from a web service rather than a database. If we have followed a MVP approach, this change would be rather trivial to implement.

### An Event-Driven supporting architecture

The following architecture aims to make easier the implementation of an Event-Driven based applications. It also has some other advantages, such as a high modularity and easiness for testing.

We are going to create our own instance of _Application_. This instance will host an EventBus Registry, which is a class that contains a comprehensive list of all the subscribers to the bus (more on this later). Our _Application_ will register all the subscribers and de-register them when it has been terminated.

#### The EventBusRegistry

This class is basically a register containing all the subscribers to the bus. I ended up naming my subscribers as PluginControllers, since you can plug them in and out and the application will keep working (of course, if they are not plug in they will not listen to events). I understand this naming can confuse the reader, so I will name then as Subscribers in this article.

The EventBus Registry keeps a reference to the EventBus (which is a static class), so it can register the subscribers.

![image](/articles/2015-02-08_eventdriven-programming-for-android-part-iii/images/2.png#layoutTextWidth)
Conceptually: the Application will contain a EventBus Registry with references to the different subscribers, so they can be registered or unregistered. The EventBus is a static instance in the application.



#### The Subscribers

The Subscribers will be the only class able to listen to events. This classes will always contain one or more _OnEvent()_ method. The Subscribers will perform actions after they received an Event. A basic example: you can have a subscriber that performs a call when receives the “PerformCallEvent”.

Subscribers can also post events into the EventBus as a response to an incoming Event.

#### Presenters

The presenters take actions. The Views give them orders, and they act in consequence. They can also post events into the EventBus.

This architecture uses a single Activity. There are arguments in favour and against this, but since we will be using different Fragments to represent the screens, using a single Activity makes things easier (and remember, as a developer your main target should be to program less).

I have uploaded to [GitHub](https://github.com/kikoso/Event-Bus-Architecture) a sample project that includes a login screen, that triggers event to perform the login and loads a different fragment after it. Take a look at the project structure:

![image](/articles/2015-02-08_eventdriven-programming-for-android-part-iii/images/3.png#layoutTextWidth)


There are base classes for the EventBus Registry, the Activities and the Subscriber (you might want to add a base Fragment class depending on your project needs). The Application, EventBus and EventBus registry have been customized for the project (thus the ED prefix).

Extending this application into new features will basically require new events, subscribers and a presenter and view per feature. Following this pattern ensures that the application is scalable, the code is decoupled and therefore easy to test and understand.
