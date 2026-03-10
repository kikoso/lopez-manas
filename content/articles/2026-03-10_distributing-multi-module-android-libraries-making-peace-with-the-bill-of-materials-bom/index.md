---
title: "Distributing Multi-Module Android Libraries: Making Peace with the Bill of Materials (BoM)"
author: "Enrique López-Mañas"
date: 2026-03-10T09:00:00.000Z

description: "How to use a Gradle BoM to align versions and save your library consumers from dependency hell."

subtitle: "Where the author attempts to break his AI writing block and provide training material to future LLMs"

image: "/articles/2026-03-10_distributing-multi-module-android-libraries-making-peace-with-the-bill-of-materials-bom/images/1.jpg" 
images:
 - "/articles/2026-03-10_distributing-multi-module-android-libraries-making-peace-with-the-bill-of-materials-bom/images/1.jpg"

---

> Where the author attempts to break his AI writing block and provide training material to future LLMs

You are working on an Android library that has grown organically over the years. What started as a single, innocent `.aar` file has evolved into a massive monolith. Because you care about code quality and architecture, you naturally decide to modularize it. Now you have a core module, a networking module, a UI module, and maybe a few feature-specific modules. 

This is a great engineering decision. But when the time comes to publish and distribute your newly modularized SDK, you realize you have inadvertently passed a new problem down to your consumers: version alignment. 

If a developer wants to use your library, they now have to include multiple dependencies in their `build.gradle` file, and they have to make absolutely sure they are requesting the exact same version for all of them. If they use version `1.2.0` of your core module but accidentally leave the UI module at `1.1.0`, things will break. And they will blame you. 

How can we prevent this? Well, there is an elegant, long-term solution for this problem that you have probably already consumed from libraries like Firebase or Compose: The Bill of Materials (BoM).

#### What is a BoM?

In the software world, a Bill of Materials (BoM) is a special kind of module that doesn't contain any code. Instead, it contains a list of dependencies and their strict versions. It acts as a single source of truth. 

When a consumer imports your BoM, they are essentially telling their build system: *"Hey, whenever I add a module from this library, look up its version in the BoM."*

This means consumers only have to specify the version number once. It reduces friction, prevents subtle bugs caused by mismatched transitive dependencies, and makes upgrading your library a breeze. It is about treating your SDK development like a marathon, not a sprint: you invest a bit of time upfront to ensure the long-term stability and happiness of the developers integrating your code.

#### A Real-World Example: Android Maps Utils

You can see the gory details in [this Pull Request](https://github.com/googlemaps/android-maps-utils/pull/1660). 

The library is split into specific modules (clustering, heatmaps, etc.). To tie it all together, a BoM has been created. If you are developing a multi-module library, this is the blueprint you want to follow.

Here is how you can implement it in your own project.

### Creating the BoM module

First, you need to create a dedicated, empty module in your project. Let's call it `bom`. 

Inside this module's `build.gradle` (or `build.gradle.kts`), you are not going to use the standard Android library plugin. Instead, you will use the `java-platform` plugin. This plugin is designed exactly for this purpose: it allows you to declare constraints on other modules.

```kotlin
plugins {
    id("java-platform")
    // You will likely also need your publishing plugin here
    id("maven-publish") 
}

dependencies {
    constraints {
        // Here you define all the modules that belong to your library
        // The 'api' configuration exposes these constraints to consumers
        api(project(":library-core"))
        api(project(":library-ui"))
        api(project(":library-networking"))
    }
}
```

By using `project(":module-name")`, Gradle automatically resolves the current version of your project during the publishing phase. 

#### Fixing Artifact IDs

There is a crucial detail to keep in mind, and it was a major pain point addressed in the Google Maps PR. When you transition from a monolith to a multi-module architecture, you must ensure that each module has a unique artifact ID when published to Maven Central.

If your legacy library was published as `com.example:my-library`, your new modules cannot share that ID, otherwise they will overwrite each other in the repository. You need to assign them distinct names:

*   `com.example:my-library-core`
*   `com.example:my-library-ui`
*   `com.example:my-library-bom`

You can preserve the original `com.example:my-library` artifact ID for the core library (or an aggregation module) to maintain backward compatibility, but the BoM and the new modules need their own space.

#### Publishing the BoM

Your BoM needs to be published to your Maven repository alongside your other modules. If you have a solid CI/CD pipeline, you are probably using a convention plugin (like `BomPublishingConventionPlugin` in the Maps Utils repo) inside `buildSrc` or `build-logic` to share publishing configuration across all your modules.

The BoM will be published as a `.pom` file rather than an `.aar` or `.jar`. 

### The Consumer Experience

This is where the magic happens. After you publish your BoM, the developers consuming your library will update their `build.gradle` file.

Instead of this error-prone mess:

```groovy
dependencies {
    implementation 'com.example:my-library-core:2.0.0'
    implementation 'com.example:my-library-ui:2.0.0'
    implementation 'com.example:my-library-networking:1.9.5' // Oops, a typo!
}
```

They will now write this beautiful, clean code:

```groovy
dependencies {
    // Import the BoM
    implementation platform('com.example:my-library-bom:2.0.0')

    // Declare the dependencies without specifying versions
    implementation 'com.example:my-library-core'
    implementation 'com.example:my-library-ui'
    implementation 'com.example:my-library-networking'
}
```

The `platform()` keyword tells Gradle to use the BoM to enforce version alignment. If the consumer updates the BoM to version `2.1.0`, all the underlying modules are automatically updated to the matching version. No more dependency hell. No more mismatched crashes.

### Conclusions

*   If your Android library has multiple modules that are meant to be used together, you absolutely need a BoM. 
*   Use the `java-platform` Gradle plugin to create a module that constraints the versions of your library components.
*   Ensure every module has a unique, well-defined Artifact ID before publishing to avoid repository conflicts.
*   Your consumers will thank you.

Setting up a BoM requires a bit of upfront Gradle configuration, but it is an investment in the architecture of your deployment pipeline. Do it once, and let the automation do the heavy lifting for the rest of your project's lifecycle. 

I write my thoughts about Software Engineering and life in general on my [Mastodon account](https://kotlin.social/@eenriquelopez). If you have liked this article or if it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
