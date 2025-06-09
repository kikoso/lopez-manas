---
title: "A Comprehensive Introduction to Perform an Efficient Android Code Review"
author: "Enrique López-Mañas"
date: 2015-12-09T12:08:20.697Z
lastmod: 2025-06-09T09:47:55+02:00

description: ""

subtitle: "You are working in a team that cares about code quality. You have been doing -or thinking of doing- some code pairing. Your team regularly…"

image: "/articles/2015-12-09_comprehensive-introduction-to-perform-an-efficient-android-code-review/images/1.png" 
images:
 - "/articles/2015-12-09_comprehensive-introduction-to-perform-an-efficient-android-code-review/images/1.png"
 - "/articles/2015-12-09_comprehensive-introduction-to-perform-an-efficient-android-code-review/images/2.png"


aliases:
    - "/a-comprehensive-introduction-to-perform-an-efficient-android-code-review-75975ccaa20a"

---

You are working in a team that cares about code quality. You have been doing -or thinking of doing- some code pairing. Your team regularly carry out hacking events to talk and present new technologies, or to talk about the personal discoveries of each member. And you are trying to devise the perfect code review process for your organisation. Is this situation familiar to you?

Code reviews are hard to implement. A team is composed of **N** people, each of them having its own agenda and priorities. Some people might be more perfectionist and might have a different acceptance criteria for the code reviews. Some others truly believe the reviews should be something at the top of each new feature or fix, and completely voluntary. As in any team, convincing needs to be done rather than imposing.

#### What is the purpose of a code review?

After a few years applying it (and more specially, comparing it with the time I did not use them) I can only think of code reviews in positive terms. If they are properly implemented, there is no single disadvantage about them, and is all about benefits. This is a cheat list I once wrote to convince other team members of why should we apply code reviews:

*   **Education of other developers:** software systems are complex. You will likely be working in extensive platforms knowing a 5%, maybe a 10% of the total global. You do not know what is going on in the other side, and this is a big limitation. Time is limited and pressure is normally vast enough to stop you from free-wandering around other modules. A code review can introduce you here the other part of the platforms without taking a significative amount of time — and yes, this is an amazing introductory method for new members in a team. Code reviews are a tool for _knowledge transfer_.
*   **Improving code quality:** programming puts you in a mental flow where you isolate from external influences and focus on a single target. It makes you biased, since you are thinking _“how do I make this work?”_. An external developer will think “_how can I break this, and where can I find weak points?”_. This is the reason why developers should never test their code, and also why we have specialized QA testers. Introducing a third person to review will very likely find bugs that otherwise will go
unnoticed.
*   **Creating a developing culture:** we all have work with coding guidelines and style. We all have our own oddities and crazes we have acquired during years of development, but in an organisation we want to make all fit in the same developing culture. _“But what happens with our team creativity!”_ I have heard many times when exposing this argument. There is a Japanese proverb, 出る釘は打たれる, _“A nail that sticks out will be hammered”_. We do not need to hammer any nail here. We can take the finest from the Western and Eastern philosophies to create a radically cool process, taking the best of each world.
*   **Confidence:** if you are working alone, you are coding for yourself. You do not care if the code is readable by another person and this will in detriment of your quality. A person should never work alone in any team: he/she will burn out, the quality of the code will decline and the project will perish). If you know a third person will read and analyse your code, your inner-code will put an extra effort to make it clear, concise and readable. Is like a very cheap tool for static code analysis.

### How a code review should be done for Android?

Those are general reasons and arguments to support code reviews, but you have read at the beginning of this article in the title the word Android. So how can we efficiently review Android code? Well, there a few tools and techniques that we can specially apply in our green platform.

**Disclaimer/50% spam**: I wrote some time ago an article on [automating Android development](https://medium.com/google-developer-experts/automating-android-development-6daca3a98396#.njcyjponb), providing a model for branching and committing to a Git repository. Adopting a branching and development model is crucial in order to implement a code review process. All the code reviews must be done before a branch is actually merged into another one. In my particular model, the code reviews are done in the following sections:

*   When a feature has been finished, and needs to be merged into alpha.
*   When a bug has been discovered during the bug fixing sprint, and needs to be merged into beta/alpha.
*   When a hotfix has been finished, and needs to be merged again.
![image](/articles/2015-12-09_comprehensive-introduction-to-perform-an-efficient-android-code-review/images/1.png#layoutTextWidth)
In the model proposed in the previous post, this is where you apply the code reviews



UPDATE: My colleague [Nick Skelton](https://twitter.com/nshred), who presented this topic with me in different conferences, posted also [his own article](http://www.androidshortcuts.com/a-scaleable-git-branching-strategy-for-android/) with ideas and a further extension of the model. I can totally recommend to check it out.

#### Getting started

First of all, this is a model I have used in my previous company and now as an independent contractor. It worked for me. It specially worked when it comes to Android development. But do not forget that there is nothing dogmatic in Software Engineering. Theories must be adapted to each scenario, so take what you like from here and feel free to modify it.

When I have a branch in one of three previously mentioned cased that needs to be merged, I open a Pull Request and assign at least one (and preferably two) other developers to check the code. Inexplicably, some environments only allow one reviewer per PR (Good morning [GitHub](https://github.com)!), so this process needs to be done manually (when reviewer **A** is finished, he should assign the review to the reviewer **B**). Optimally one reviewer must be from the development team (they are aware of restrictions and status of the project), and the second one will be from an alien team (we want to share knowledge with this individual).

Reviewers have veto power. They both need to agree on merging the branch. This arises team spirit, since everybody is a little bit responsive of each feature being committed into our system, even if they are not direct contributors. When there are disagreements they need to be argued and solved in our PR Dashboard, until we reach a consensus. If a referee figure is absolutely required, the Team Lead or a similar figure should have a decision power — although in all my years of experience, I never had a problem with a PR being blocked due to lack of agreement of brilliant jerks!

A proper PR starts with downloading locally the branch and compiling it in our emulator or device. Why is this required? Well, Android is a fragmented platform with a rich ecosystem of plugins and versions. 99% of these problems can be avoided by reproducing the environment on a different computer and device/emulator.

I also advocate for an informal test of the new feature or bug. Due to our acquired bias we tend to miss trivial points while we develop because we focus on our functionality. Another big percentage of errors can be detected by this simple step: asking for the functional requirements and test that the application follows them.
> To connect Functional Requirements with branches and PR easily, is a good strategy to name our branches as our issue ticket (for instance, PROJECT-123). Most of the environments allow us to connect a PR with the Ticket repository containing description of the ticket and functional requirements, so is less of a hassle for the reviewer to access it fast.

#### When should we do them?

We should avoid interruptions. Unless it is a Hotfix, I normally do code reviews after my lunch break, or I start during a Pomodoro break. That way I ensure they do not interfere with my own development, but is done in a more relaxed moment.

A code review should also not take more than 30 minutes, but this is heavily connected to how granular the features you are implementing are. If you find yourself continuously busy for more than 30 minutes doing code reviews, is a good moment to talk with your project manager and discuss whether the dimension of the features you are implementing is adequate or not.

### Code analysis

So we have the feature in our computer. It has compiled, it meets the functional requirements and now we have to start analyzing the code. Where can we start? Which questions can we ask to the code?

#### Architecture patterns

*   Is this code following our architectural pattern? MVP, MVC, MVVM, Event-Bus?
*   Is there any operation being performed in a wrong class? (i.e., data logic in a Fragment)

#### Testing

*   Is there a test created for the feature or bug? Have the previous tests being updated?
*   Are there all the tests types implemented? Unit tests, integration tests and UI tests.
*   Are the new tests currently working?

#### Static Code analysis

One of my favorites! In Android we can use [Lint](http://developer.android.com/tools/help/lint.html) to make an static analysis of our source code. Some of those comments might make sense, and some other not (for instance, I get a lot of warnings of “spelling mistakes”… because I mainly work with German teams that tend to use German names, leading to variable names such as _datenbankVerbindung_. If you have legacy code and no resources for a refactor you might want to disable the warnings for deprecation.

As a rule of thumb: I apply Lint in all the new added files and the previous modified files. I do manually check that the Lint warnings make sense, and notify when they do and the code can be improved.

Lint can be very handy. It notifies possible bugs and memory leaks. It also notifies of deprecated code, style issues and naming conventions. It can be a powerful educational tool.

#### Code styling

Every organisation should have a coding guideline of its own (and if you do not have one, is time for you to start defining one). During my time working at Sixt we open-sourced our [coding guidelines](https://speakerdeck.com/kikoso/android-coding-guidelines). Android has some [coding guidelines for contributors](https://source.android.com/source/code-style.html) that you can use as an inspiration for your own ones. And of course, the [Clean Code](http://bit.ly/1SNR4Yp) bible has an extensive set of recommendations on clean coding and code styling — a must book if you have not read it yet.

### Automation baby!

From the previous steps, a few ones can be very easily automated. Lint can be easily set up in Jenkins to be executed with each build. We first need to install the [Lint plugin](https://wiki.jenkins-ci.org/display/JENKINS/Android+Lint+Plugin) in our Jenkins CI server. Then we just need to activate it in our job configuration:

![image](/articles/2015-12-09_comprehensive-introduction-to-perform-an-efficient-android-code-review/images/2.png#layoutTextWidth)
Now we are applying and saving our Lint results!



As a useful rule, you should deactivate Lint in your Gradle file to prevent the application from stop building. This can be easily done with the following code snippet:
`android {  
    // ...  

    lintOptions {  
        // Don&#39;t abort if Lint finds an error, otherwise the Jenkins build  
        // will be marked as failed, and Jenkins won&#39;t analyse the Lint output  
        abortOnError false  
    }  
}`

I prefer to mark Lint builds as unstable rather than failed, and to check the output manually (again, this will depend on your company policies). Jenkins can even be set up to run Lint when a PR is open! I can’t stop saying how much using Jenkins makes the life of everybody at the office easier, but I am still surprised how many people is still not using it — my random guess after asking it at many conferences is probably a third of the companies.

Coding Guidelines and styling can also be automatically checked in Android. You can use [Checkstyle](http://checkstyle.sourceforge.net/) (a development tool to ensure that a coding style is being fulfilled) and run it against your code. Checkstyle has plugins for [Android Studio](https://plugins.jetbrains.com/plugin/1065), [Jenkins](https://wiki.jenkins-ci.org/display/JENKINS/Checkstyle+Plugin) and definitely other platforms. Depends on the strictness you follow you might want to make the build fail or mark it as unstable. I personally like sending an automatic report to the committer mentioning the flaws in its coding style.

### Conclusions

Performing a code review is like cooking: is a personal process where only a main guidelines must be followed, and the final procedure tend to branch and differ from the initial seed. However, after reading this post you should have a more clear idea on how to start and how to check-and likewise, if you are an experienced developer I hope you were able to get a few ideas an inspirations.

There are a few more points I would like to remark before finishing the article:

*   Code reviews are about the code, not about the person. This must be a clear point to each team member, to avoid taking it personally. The purpose is to ship a high-quality code, not to increase ego.
*   Good things must also be pointed out. When I find something clever or brilliant, I learn from it and I let it know to the developer.

I always think that live demos are way better than a theoretical post, so I plan to post a few more articles with particular ideas and code reviews. If you are interested in the topic, feel free to subscribe or to follow me on [Twitter](http://twitter.com/eenriquelopez)! If you like the article, click on the little heart at the bottom to recommend it and feel free to share it :-)

Thanks [Corey Latislaw](https://medium.com/@colabug) for your feedback, you rock!
