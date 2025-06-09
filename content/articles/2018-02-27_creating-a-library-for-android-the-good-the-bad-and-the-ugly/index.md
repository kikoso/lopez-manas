---
title: "Creating a library for Android: The Good, the Bad and the Ugly"
author: "Enrique López-Mañas"
date: 2018-02-27T06:40:31.097Z
lastmod: 2025-06-09T09:49:00+02:00

description: ""

subtitle: "Software Development is like an Ouroboros. You end up going to the place you have previously resided, with requirements and knowledge…"

image: "/articles/2018-02-27_creating-a-library-for-android-the-good-the-bad-and-the-ugly/images/1.jpeg" 
images:
 - "/articles/2018-02-27_creating-a-library-for-android-the-good-the-bad-and-the-ugly/images/1.jpeg"


aliases:
    - "/creating-a-library-for-android-ea976983db1"

---

![image](/articles/2018-02-27_creating-a-library-for-android-the-good-the-bad-and-the-ugly/images/1.jpeg#layoutTextWidth)
Software Development is like an [Ouroboros](https://en.wikipedia.org/wiki/Ouroboros). You end up going to the place you have previously resided, with requirements and knowledge updated and refashioned. You might have started working on an initial prototype that began the journey as a basic _HelloWorld_, and it has evolved into one of those mythological Nordic monsters. Or maybe Greek monsters are more terrifying and frightening. I do not know.

At one of my projects we recently came up with the requirement of extracting some of the functionality well buried there to expose to third-party consumers. Our code connects to our API and performs some operations (authentication, managing our entities, etc…) that now were required to be used by another client. I have seen this frequently and previously at other workplaces — the need to create a MobileKit or MobileLibrary, you name it, that can be reused in different applications. Therefore, this functionality can be reused among applications at the same company, or they can be offered to third-party users to access their APIs.

There are different methods you can follow for the development and distribution of such components in the Android ecosystem. In this article, I want to outline them and give you the arguments to decide which one can adapt better to your particular scenario.

### Creating your Android library

Starting here, we have different approaches. Generally, if we are following a principle of isolation, I would concur with keeping from the beginning our library in its own BitBucket, GitHub or whatever repository. We want to fence off our components, and bring all the benefits from different software philosophies ([open/closed principle](https://en.wikipedia.org/wiki/Open/closed_principle), [software reuse](https://en.wikipedia.org/wiki/Code_reuse), etc). Maybe adding a sample to the same repository to showcase how to use and access the library is fine (this is, in fact, a very common state-of-the-art approach). In your Android Studio, it is very easy to add a new [library module](https://developer.android.com/studio/projects/android-library.html). Now the arduous task that we will flagrantly diminish starts: it is time to start and develop your own library, eventually with samples, documentation and anything you consider proper to include.

### **Providing access to your brand new library**

You are finished with your library, ready to publish a first beta version or glad about sharing with others for the first time your superb functionality. Now it is the time to provide access and distribution. There are different possibilities here, each of them providing an assorted handful of benefits and drawbacks.

#### Providing access to your library as a Git submodule

Git Android library project as a sub-module as a submodule means that you will be able to access the source code of the newborn library. The source code is checked out as the code of your main application, and it can be as well modified locally (eventually also committed directly from the main project). This might make sense is some particular contexts:

*   You work in the same organisation with people working on apps that require access to the same APIs that might needed to be changed by any team member.
*   The same people working on the apps are working as well on the library.
*   The tempo for developing the library is steady, your CI process cannot guarantee a continuous delivery of new versions of the library and you need to commit them as soon as possible to the repository.

The methodology to perform this it is straightforward. From your local git repository, you need to add your submodule:
`git submodule add [y](https://XXX@bitbucket.org/YYY/ZZZ.git)our-repository.git`

And update consequently your **settings.gradle** and **build.gradle** files.

Ah! There is something I always forget when I am cloning a directory with submodules. That is, you need to specify that the module you are cloning contains… submodules.
``git clone --recurse-submodules``

Any human mean of having this behavior as default by Git? Not that I am aware of. I remember I always clone the repository without the submodules, and then I have to download the submodules manually. It is one of those facts that always entail an issue left aside, such as adding an Activity to an Android project and forgetting to add the same Activity to the AndroidManifest.xml.

#### Distributing the new Android library in a self-contained file

You might be lacking the infraestructure to provide your library as a Git submodule, or you might want to choose another mean of distribution for different reasons:

*   Privacy and/or security: nobody needs to be aware of the code of the new library.
*   Better isolation: even if people work in the same organisation, they do not need to get involved with the technicality of the library and just access the source code.

I am not including in this section distribution through a Nexus Server, and I see reasons to keep it separately. For my aforementioned client, I suggested to keep the distribution of the library through a Nexus repository, and the argued reason was that the Nexus repository of the organisation was only accessible from the internal network, whereas most of the Mobile workforce was remote or partial remote.
> In any organisation you will encounter different truths, scenarios, complications, limitations and situations you need to deal with. Never take a single methodology as the Holy Grail. Instead, learn as many methodologies to solve a problem as you can, and decide which one applies better in your particular storyline.

So let’s return to our primal origin: distributing the Android library in a self-contained file. In the Green Droid realm, we can tackle mainly two file formats: **.aar** and .**jar**. The first one stands for Android archive, and the latter stands, unsurprisingly, for Java archive. They are both zipped files containing many classes, metadata and resources. It has been claimed that **.aar** can contain Android resources, whereas **.jar** cannot. This is not true: there is no actual limitation against the file types that a **.jar** file can contain (check the .jar file [overview](https://docs.oracle.com/javase/6/docs/technotes/guides/jar/jar.html) and [specification](https://docs.oracle.com/javase/6/docs/technotes/guides/jar/jar.html)).

As a de facto industry standard, if you are using Android Studio as a build and are aiming to target mainly Android clients, you are better off with a **.aar** file.

When you are creating your files, it is a good idea to upload the resulting libraries to your GitHub repository, keep your branches up-to-date, organising releases in Git and of course using [Git tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging).

#### Distributing through a Nexus repository

You have your library ready. You have versioned it, and you are ready for deployment (this might sound more appealing for people deploying rockets into orbit, but I can ensure the alluring feeling of finally unlock your software to third-parties after a long development period is equally enchanting). Now it is time to release it through a Nexus Repository.

A Nexus repository manages artifacts for download. You develop your software, upload it to a Nexus repository and make it public to the world. It is a very convenient way, and keeps every aspect of the development wheel quite framed in a domain. As I mentioned, there might exist limitations in your organisation, but this is, in my opinion, the most optimal option to release an artifact.

When you add a file from a Nexus repository, you typically include the following line in your Gradle script:
`implementation &#39;com.android.support:support-v4:27.0.2&#39;`

A Nexus repository can be public or private. As I mentioned in the case of my client, the Nexus repository was only accessible from their internal network, and it was therefore not an optimal solution. There are well-known public Nexus repositories, such as [Maven Central](https://search.maven.org/), which you are very likely already using, or [Sonatype](https://www.sonatype.com/nexus-repository-oss). If you are developing OSS this will be your instant choice, since the offer a free-tier and you can expose your work to the world. This can as well be automated, and therefore being uploaded automatically to a repository through a Gradle script:
`uploadArchives {  
   repositories {  
      mavenDeployer {  
         repository(url: “[http://localhost:8081/nexus/content/repositories/snapshots](http://localhost:8081/nexus/content/repositories/snapshots)&#34;) {  
 authentication(userName: “admin”, password: “admin123”)  
         }  
         pom.version = “1.0-SNAPSHOT”  
         pom.artifactId = “simple-project”  
         pom.groupId = “com.example”  
      }  
   }  
}`

### Conclusions

There will never exist an approach with no flaws to the needs of the software, organisation and product you are trying to build. For a standard OSS, the distribution through a Nexus repository (and having the obvious choice as well of cloning the library as a submodule) is an ideal alternative. For other scenarios, you need to balance all the requirements and take one decision that might mix some of the previously introduced elements.

I write my thoughts about Software Engineering and life in general in my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share it, ♥ it and/or leave a comment. This is the currency that fuels amateur writers.
