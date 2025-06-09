---
title: "Using Git Hooks to improve your development workflow"
author: "Enrique López-Mañas"
date: 2019-08-31T05:56:46.794Z
lastmod: 2025-06-09T09:49:26+02:00

description: ""

subtitle: "Recently, I was contributing for the first time to a new codebase. I extend some functionality that I needed. After thorough testing on my…"

image: "/articles/2019-08-31_using-git-hooks-to-improve-your-development-workflow/images/1.jpeg" 
images:
 - "/articles/2019-08-31_using-git-hooks-to-improve-your-development-workflow/images/1.jpeg"


aliases:
    - "/using-git-hooks-to-improve-your-development-workflow-8f5a1fb81ec7"

---

![image](/articles/2019-08-31_using-git-hooks-to-improve-your-development-workflow/images/1.jpeg#layoutTextWidth)
Recently, I was contributing for the first time to a new codebase. I extended and implemented some functionality that I needed. After thorough testing on my machine, where I checked that the functionality was properly working, I committed my contribution. Minutes after, our CI environment delivered a message:
> 4 Tests failed

This happens so often, even on the codebases we are used to work with. We tend to focus on developing the new features, and forget that there is a test that is covering them. Or that there is a new test that needs to be done, to cover the new features. This very fact is not a tragedy, but the workflow, in this case, can surely be improved. We can use Git Hooks to ameliorate them.

[Git Hooks](https://githooks.com/) are scripts that are executed before or after different Git events. For instance: commit, push, and receive. They are a built-in solution (no need to download any third-party addon) and they execute locally on your machine. The variety of scenarios we can apply them on is of considerable size.

Let’s consider the previous scenario. The modern tech world tends to move into solving problems into early stages of development. For instance, the entire Nullability promise is about delivering the error during the compiling process, rather than during the runtime. That has indubious positive consequences over the quality output. Analogously, if we can fail the tests on our machine, we will surely improve our workflow rather than having the test failing on the CI environment, with all the side implications (fixing the test on our machine, testing, re-pushing, running CI).

Let’s assume we are having an Android app running with Gradle — although any app running on Gradle will work out. When we are running the tests, we are basically running a command similar to the following one:
> ./gradlew clean test

We want this command to be executed before we actually push our code. In order to do that, we need to do the following:

1.  Go to the _.git/hooks_ folder of your repository.
2.  Create a file called _pre-push_
3.  Copy the following snippet:



Right now, any time before you push your code, tests will run locally. If there is any error, there will be no push (when the script is returning 1).

Note that you could decided to do this on each commit, instead of on each push. If that would be the case, you would have needed to modify the file _pre-commit_. I believe running the tests before the push is more effective than doing it before the commit, but you might need to see how this fits in your workflow.

There are some interesting ideas of aspects that we could automate using Git Hooks. For instance, one of those tasks that we might want to run is the static analysis with tools such as [lint](https://en.wikipedia.org/wiki/Lint_%28software%29) or [detekt](https://github.com/arturbosch/detekt). For this example, let’s use the former, and let’s store it on a _pre-commit_ file.


Full gist: [https://gist.github.com/kikoso/a46e6a2efd07ab66ed049b5f7b76ace5](https://gist.github.com/kikoso/a46e6a2efd07ab66ed049b5f7b76ace5)



We can actually combine both of them, if we want to execute them together on a _pre-push_ hook:


Full gist: [https://gist.github.com/kikoso/0a79740c7cde9174ffbafe19caa39306](https://gist.github.com/kikoso/0a79740c7cde9174ffbafe19caa39306)



In any process, there are some manual tasks we need to perform, and that are easy to forget. A Git Hook could ensure (or at least remind the user) that those taks should be performed before the commits are actually pushed:


Full gist: [https://gist.github.com/kikoso/d6024e455c733fb91798621ae487a375](https://gist.github.com/kikoso/d6024e455c733fb91798621ae487a375)



There are several ideas we can apply. For instance, depending on your flow you might want to create a release tag right after you have merged your develop branch into your master branch. This is easily achievable with Git Hooks:




This could in fact be further automated (instead of typing the tag on the console you could read it from your Gradle file, or from an environmental variable where you store it.

This is the full list of git hooks available. We will not elaborate further on each of them since the name is quite self-explanatory.

*   [**applypatch-msg**](https://github.com/git/git/blob/master/templates/hooks--applypatch-msg.sample)
*   [**pre-applypatch**](https://github.com/git/git/blob/master/templates/hooks--pre-applypatch.sample)
*   [**post-applypatch**](https://www.git-scm.com/docs/githooks#_post_applypatch)
*   [**pre-commit**](https://github.com/git/git/blob/master/templates/hooks--pre-commit.sample)
*   [**prepare-commit-msg**](https://github.com/git/git/blob/master/templates/hooks--prepare-commit-msg.sample)
*   [**commit-msg**](https://github.com/git/git/blob/master/templates/hooks--commit-msg.sample)
*   [**post-commit**](https://www.git-scm.com/docs/githooks#_post_commit)
*   [**pre-rebase**](https://github.com/git/git/blob/master/templates/hooks--pre-rebase.sample)
*   [**post-checkout**](https://www.git-scm.com/docs/githooks#_post_checkout)
*   [**post-merge**](https://www.git-scm.com/docs/githooks#_post_merge)
*   [**pre-receive**](https://www.git-scm.com/docs/githooks#pre-receive)
*   [**update**](https://github.com/git/git/blob/master/templates/hooks--update.sample)
*   [**post-receive**](https://www.git-scm.com/docs/githooks#post-receive)
*   [**post-update**](https://github.com/git/git/blob/master/templates/hooks--post-update.sample)
*   [**pre-auto-gc**](https://www.git-scm.com/docs/githooks#_pre_auto_gc)
*   [**post-rewrite**](https://www.git-scm.com/docs/githooks#_post_rewrite)
*   [**pre-push**](https://www.git-scm.com/docs/githooks#_pre_push)

#### Last notes

Git Hooks are a very efficient and flexible mechanism to improve our workflow. Since they are based on shell-scripting, the sky is almost the limit. We can perform almost any task that is not easy to do with other tools.

Keep in mind that Git Hooks need to be manually installed, they are not stored in a repository for all the users. I recommend you to create a _githooks/_ folder on your Git repository, and store the Git Hooks over there. You could even create a script that installs all of them when the repository is downloaded for the first time (even including a Git Hook that install all the hooks contained in that folder after the repository has been updated).

I write my thoughts about Software Engineering and Finance on my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share it, ♥ it and/or leave a comment. This is the currency that fuels amateur writers.
