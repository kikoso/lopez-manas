---
title: "Uploading SARIF Reports to GitHub"
author: "Enrique López-Mañas"
date: 2024-10-23T06:08:25.588Z
lastmod: 2025-06-09T09:50:35+02:00

description: ""

subtitle: "Recently I wanted to add Lint reports to a repository on GitHub. The goal is to report potential Lint violations when new code is…"

image: "/articles/2024-10-23_uploading-sarif-reports-to-github/images/1.jpeg" 
images:
 - "/articles/2024-10-23_uploading-sarif-reports-to-github/images/1.jpeg"
 - "/articles/2024-10-23_uploading-sarif-reports-to-github/images/2.png"
 - "/articles/2024-10-23_uploading-sarif-reports-to-github/images/3.png"
 - "/articles/2024-10-23_uploading-sarif-reports-to-github/images/4.png"


aliases:
    - "/uploading-sarif-reports-to-github-91a8001e6794"

---

![image](/articles/2024-10-23_uploading-sarif-reports-to-github/images/1.jpeg#layoutTextWidth)
Recently I wanted to add Lint reports to a repository on GitHub. The goal is to report potential Lint violations when new code is committed, to make sure that all the committed code is lint-warning-free and pretty.

My first idea was to look for a GitHub action that could run ./gradlew lint and report it as a PR comment. After asking about ideas in the Android Study Group, [Carter Jernigan](https://www.linkedin.com/in/carterjernigan/) and [Justin Brooks](https://www.linkedin.com/in/jzbrooks) suggested me to upload directly the SARIF files into GitHub. I wasn’t aware this was possible.

#### What is a SARIF file?

SARIF is a standardized format to represent the result of static analysis. It contains some metadata regarding the static analysis tool that was used to create the report, active rules, and found violations. This is an excerpt from a SARIF file, representing a Lint violation (not targeting the latest Android version):




By default, the output of ./gradlew lint does not include a report in a SARIF format, but this can be easily added with the following block in a Gradle file:




After adding and syncing this line, running Lint will now generate a report in a SARIF format:

![image](/articles/2024-10-23_uploading-sarif-reports-to-github/images/2.png#layoutTextWidth)


One more problem that we may find here is that, if we have a multimodule project, this can result in several SARIF files that we need to merge and unify. This can easily be done via a GitHub action, which merges and upload the SARIF files:




Finally, GitHub will now post Lint violations on every PR, which you can check while reviewing it:

![image](/articles/2024-10-23_uploading-sarif-reports-to-github/images/3.png#layoutTextWidth)


Then the code scanning section in GitHub will be activated, and all the current Lint violations will be displayed under [https://github.com/ORG/REPO/security/code-scanning?query=pr%3A1406+is%3Aopen](https://github.com/googlemaps/android-maps-utils/security/code-scanning?query=pr%3A1406+is%3Aopen)

![image](/articles/2024-10-23_uploading-sarif-reports-to-github/images/4.png#layoutTextWidth)


This trick only works for open-source repositories, or those that use GitHub Advanced Security.

I share my thoughts about Software Engineering and life in general on my [Mastodon account](https://kotlin.social/@eenriquelopez). If you have liked this article or if it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.

Disclaimer: This article didn’t use Generative AI in its elaboration.
