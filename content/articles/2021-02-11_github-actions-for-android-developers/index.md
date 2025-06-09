---
title: "GitHub Actions for Android developers"
author: "Enrique López-Mañas"
date: 2021-02-11T09:26:21.540Z
lastmod: 2025-06-09T09:49:53+02:00

description: ""

subtitle: "If you are developing Android apps, chances are you have confronted any sort of CI at some point in your career. If you thought Android…"

image: "/articles/2021-02-11_github-actions-for-android-developers/images/1.png" 
images:
 - "/articles/2021-02-11_github-actions-for-android-developers/images/1.png"
 - "/articles/2021-02-11_github-actions-for-android-developers/images/2.png"


aliases:
    - "/github-actions-for-android-developers-6b54c8a32f55"

---

![image](/articles/2021-02-11_github-actions-for-android-developers/images/1.png#layoutTextWidth)
If you are developing Android apps, chances are you have confronted any sort of CI at some point in your career. If you thought Android fragmentation was a thing, the wide availability of CI systems will be familiar to you.

GitHub Actions was released around November 2019, and since then it has proved itself to be reliable for a production environment (one of our requirements before committing to any software system). Like many other CI/CD systems, GitHub actions ultimately let us define a workflow for our apps to automatically build, test and deploy them.

One of the shiniest aspects of GitHub Actions is its integration with GitHub. For repositories that are already hosted in GitHub, GitHub Actions allows us to automate the process in one single platform, without having to rely upon any external tools. Your code is on GitHub, your CI/CD runs on GitHub, and you can have also your distribution on GitHub if you wish.

Now, GitHub Actions provides thoughtful guides and documentation, although jumping initially onto it might be overwhelming for folks without previous experience with it. The documentation provides an example of a basic set-up for Android developers, but you might be wondering _“where can I get some inspiration on things I can do with GitHub Actions?”_. This post aims to provide a few answers based on my personal experience using GitHub Actions. I have been using it for an Android project, and hence my experience (and this post) is limited to this platform. Without any further delay, let’s go.

#### The structure of our config file

GitHub Actions requires a .yml file specifying all the steps for the CI/CD. YAML files are uncomfortable, especially when they become large (indentation problems might become unnoticed, and support from IDEs is rare). The files are stored in the folder `.github/workflows/file.yml`. A minimal example of how they look is the following:
`# Workflow name  
name: Build``on:  
# When it will be triggered  
# And in which branch  
  pull_request:  
  push:  
    branches:  
      - main  

``# Where will they run  
jobs:  
  build:  

    runs-on: ubuntu-latest`

#### Actions

Actions are a particular type of step that help us with the task of automating our CI/CD. Anybody can publish their Action as open-source, and they are browsable [via GitHub](https://github.com/actions). Many of the functionality we might want to implement is likely already here, so it is worth taking a look to avoid reinventing the wheel. And of course, it is possible to [fork and modify existing actions or create](https://docs.github.com/en/free-pro-team@latest/actions/creating-actions) our own ones.

Now, here is a list of some suggestions of operations we can perform in Android. As the name CI/CD, we typically want to start building and deploying apps, but there are some goodies that we can apply (notify certain channels or platforms, etc). Let’s get started.

#### Setting up our Android app

Initially, we will set up our environment, and in order to do that, we need to check out our project and set up our JDK. We will be using our first Action here, [Checkout v2](https://github.com/actions/checkout) to do a `git checkout` of our repository, and [setup-java](https://github.com/actions/setup-java) to prepare our Java environment.
`_## Checkout our repository ###  
_- name: Checkout  
  uses: actions/checkout@v2.3.3  

- name: Set up our JDK environment  
  uses: actions/setup-java@v1.4.3  
  with:  
    java-version: 1.8`

#### Building our artifacts

The foundation of every project is to compile all our artifacts to be uploaded and/or distributed. Android has often a particularity, and is that we might generate several APKs based on our Flavor or BuildTypes. Some of them are relevant (our release artifact that might go directly to our test team), some of them less relevant (our test artifacts that are just for development use) depending on your team structure. Luckily, we can call directly Gradle commands and generate the number of artifacts that are relevant. We will use the Action [gradle-command-action](https://github.com/eskatos/gradle-command-action) to execute our Gradle command. An example can be the following:
`_## Build all our Build Types at once ##  
_- name: Build all artifacts  
  id: buildAllApks  
  uses: eskatos/gradle-command-action@v1.3.3  
  with:  
    gradle-version: current  
    wrapper-cache-enabled: true  
    dependencies-cache-enabled: true  
    configuration-cache-enabled: true  
    arguments: assembleRelease`

The line `arguments: assembleRelease` is the relevant one here. We can easily substitute it with the Gradle command we want to execute.

#### Testing

There are several tests or analysis tool we might want to run on our CI/CD environment. Luckily, with GitHub actions we can directly run our Gradle commands. Starting for instance our tests or Lint can be done easily by directly calling the relevant Gradle command:
``- name: Run Kotlin Linter  
  run: ./gradlew ktlintStagingDebugCheck  

- name: Run Unit Tests  
  run: ./gradlew testStagingDebugUnitTest``

We can also run our Espresso Tests on GitHub Actions. There are several actions that allow us to trigger them, we will showcase [android-emulator-runner](https://github.com/ReactiveCircus/android-emulator-runner) by [Reactive Circus:](https://github.com/ReactiveCircus)
``uses: reactivecircus/android-emulator-runner@v2  
    with:  
      api-level: 23  
      target: default  
      arch: x86  
      profile: Nexus 6  
      script: ./gradlew connectedCheck --stacktrace``

#### Signing artifacts

Signing artifacts is the next natural step while creating our Android artifact, so they can be installed on a device.
`_## Sign our artifact##  
_- name: Sign artifact  
  id: signArtifact  
  uses: r0adkll/sign-android-release@v1.0.1  
  with:  
    releaseDirectory: app/build/outputs/apk/ourbuildtype/release  
    alias: ${{ secrets.KEYALIAS }}  
    signingKeyBase64: ${{ secrets.KEYSTORE }}  
    keyStorePassword: ${{ secrets.KEYSTORE_PASSWORD }}  
    keyPassword: ${{ secrets.KEY_PASSWORD }}  

- name: Upload our APK  
  uses: actions/upload-artifact@v2.2.0  
  with:  
    name: Release artifact  
    path: app/build/outputs/apk/ourbuildtype/release/app-artifact-*.apk`

Some further explanation of what is going on here:

The task named “Sign artifact” uses the [sign-android-release](https://github.com/r0adkll/sign-android-release) Action. This is pretty straight-forward: we need to specify the information related to the key, so the APK gets signed. It is possible to specify different tasks if we need them (for instance, because we need to sign APKs with different keys).

The task “Upload our APK” uploads artifacts from our workflow, allowing us to share data between jobs and store data once a workflow is complete. It uses the Action [upload-artifact](https://github.com/actions/upload-artifact). Note that on the path field we are using a wildcard `app-artifact-*.apk`.

With Gradle we can customize our configuration file to determine the name of our resulting APK. This results in a much more readable output, rather than always using the default APK name. For instance, the following code block changes the name of our Gradle file to a more readable format (app-{flavor}-{buildName}-{versionName}.apk:
`android.applicationVariants.all **{** variant **-&gt;  
** variant.outputs.all **{  
** outputFileName = &#34;app-$**{**variant.productFlavors[0].name**}**-$**{**variant.buildType.name**}**-$**{**variant.versionName**}**.apk&#34;  
    **}  
}**`

#### **Create Release**

Something interesting offered in GitHub is the possibility to create a Release in GitHub itself, which we can later use to distribute our artifacts. For instance, see how the Release page for [the version 1.4.2](https://github.com/Kotlin/kotlinx.coroutines/releases/tag/1.4.2) of the Kotlin coroutines looks like:

![image](/articles/2021-02-11_github-actions-for-android-developers/images/2.png#layoutTextWidth)


Each of those releases can contain a number of artifacts, source code, documentation, etc. It is also possible to publish some CHANGELOG or notes for a particular release (more on creating this automatically later). It is certainly useful to have this automatically created with the entire process. This is the relevant section that will create the release in GitHub.
`- name: Create Release  
  id: create_release  
  uses: actions/create-release@v1  
  env:  
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  
  with:  
    tag_name: ${{ github.ref }}  
    release_name: Release ${{ github.ref }}  
    draft: false  
    prerelease: false`

#### Upload our assets to GitHub

With the release being created, it is time to upload our own assets. We are going to use an auxiliary task in order to gather our APK names and paths (supposing we are having custom names for them, as explored before).
`- name: Save name of our Artifact  
  id: set-result-artifact  
  run: |  
    ARTIFACT_PATHNAME_APK=$(ls app/build/outputs/apk/ourbuildtype/release/*.apk | head -n 1)  
    ARTIFACT_NAME_APK=$(basename $ARTIFACT_PATHNAME_APK)  
    echo &#34;ARTIFACT_NAME_APK is &#34; ${ARTIFACT_NAME_APK}  
    echo &#34;ARTIFACT_PATHNAME_APK=${ARTIFACT_PATHNAME_APK}&#34; &gt;&gt; $GITHUB_ENV  
    echo &#34;ARTIFACT_NAME_APK=${ARTIFACT_NAME_APK}&#34; &gt;&gt; $GITHUB_ENV`

Note a couple of relevant points in this code block:

*   We are setting the name of our PATH and the artifact in environment variables, which are later on saved on GitHub. This is a fantastic way to store information in GitHub Actions.
*   We are running a command to determine the name of the APK (`ls app/build/outputs/apk/ourbuildtype/release/*.apk | head -n 1`). This is highly versatile, since we can essentially use Unix/Mac commands to determine a variety of things (and later on, store them on our PATH and reuse them in other steps).

With the names and PATHs already stored on an environment variable, we will now proceed to upload them to our release page. This uses the action [upload-release-asset](https://github.com/actions/upload-release-asset):
`- name: Upload our Artifact Assets  
  id: upload-release-asset  
  uses: actions/upload-release-asset@v1  
  env:  
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  
  with:  
    upload_url: ${{ steps.create_release.outputs.upload_url }}  
    asset_path: ${{ env.ARTIFACT_PATHNAME_APK }}  
    asset_name: ${{ env.ARTIFACT_NAME_APK }}  
    asset_content_type: application/zip`

This has created our artifacts on GitHub, and we are ready to distribute them. There are a bunch of notification mechanisms we can use. For instance, if we have a Slack group we could notify a particular channel that our release is ready, using [act10ns/slack](https://github.com/act10ns/slack):
`- name: Notify on Slack  
  uses: act10ns/slack@v1.0.9  
  with:  
    status: ${{ job.status }}  
    steps: ${{ toJson(steps) }}  
    if: always()`

There is a good number of options already available as GitHub actions, including notifications on [Telegram](https://github.com/appleboy/telegram-action), via [E-Mail](https://github.com/marketplace/actions/send-email) or [Discord](https://github.com/Ilshidur/action-discord). If you can think of a particular platform you need, there is likely a GitHub action that covers it.

We could give it a last touch, and this would be to automatically fill the CHANGELOG taking some information that is already available. As you can imagine, there is already a [GitHub action](https://github.com/marketplace/actions/git-release) that solves this. This one takes the information from a CHANGELOG.md file according to [keepchangelog.com](https://keepachangelog.com/en/1.0.0/), but it would not be hard to do it using **git log --pretty=oneline**, or a similar format.

### Summary

GitHub Actions is one more CI/CD engine in the market. If you are using GitHub already, it provides a very decent integration with your code, issues and release workflow. It is highly customizable, providing APIs to create your own actions as you need them, or accessing them from the [GitHub marketplace](https://github.com/marketplace?type=actions). As with any cloud based solution (or any tech solution, for what it matters), there are several factors to weigh in before deciding on whether it makes sense to adopt it, or not. I believe it is a comfortable solution that works out a wide range of requirements.

Thank you [Marton](https://twitter.com/zsmb13), [Jossi](https://twitter.com/jossiwolf), [Ubiratan](https://twitter.com/ubiratanfsoares) and [Wajahat](https://twitter.com/wajahatkarim?lang=en) for your kind and helpful review, you rock!

I write my thoughts about Software Engineering and life in general on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
