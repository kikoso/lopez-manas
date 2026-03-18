---
date: '2014-01-29T11:53:57+00:00'
draft: false
slug: automatically-increasing-versioncode-with-gradle
title: Automatically increasing versionCode with Gradle
---

Continuous Integration means, above all, automatization. The user should not be in charge of the distribution or deployment process. Everything should be scripted!

While deploying new versions in Android, one of the common tasks is to increase the <a href="http://developer.android.com/tools/publishing/versioning.html" target="_blank">versionCode</a> to identify a particular build. Using the new Gradle system, this can also be automatized.
```java
def getVersionCodeAndroid() {
    println "Hello getVersionCode"
    def manifestFile = file("src/main/AndroidManifest.xml")
    def pattern = Pattern.compile("versionCode=\"(\\\\d+)\"")
    def manifestText = manifestFile.getText()
    def matcher = pattern.matcher(manifestText)
    matcher.find()
    def version = ++Integer.parseInt(matcher.group(1))
    println sprintf("Returning version %d", version)
    return version
}

task(''writeVersionCode'')  {     
    def manifestFile = file("src/main/AndroidManifest.xml")   
    def pattern = Pattern.compile("versionCode=\"(\\\\d+)\"")   
    def manifestText = manifestFile.getText()    
    def matcher = pattern.matcher(manifestText)     
    matcher.find()    
    def versionCode = Integer.parseInt(matcher.group(1))   
    def manifestContent = matcher.replaceAll("versionCode=\"" + ++versionCode + "\"")     
    manifestFile.write(manifestContent) 
} 

tasks.whenTaskAdded { task -&gt;
    if (task.name == ''generateReleaseBuildConfig'') {
        task.dependsOn ''writeVersionCode''
    }

    if (task.name == ''generateDebugBuildConfig'') {
        task.dependsOn ''writeVersionCode''
    }
}
```
In our defaultConfig, we will need to specify that the versionCode must be read from the newly added function:
```java
versionCode getVersionCodeAndroid()
```