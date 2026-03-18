---
date: '2014-01-29T00:02:24+00:00'
draft: false
slug: testing-asynchronous-tasks-on-android
title: Testing Asynchronous Tasks on Android
---

Recently, at <a href="http://www.sixt.de/" target="_blank">Sixt</a> we have been migrating our development environment from <a href="http://www.eclipse.org/" target="_blank">Eclipse</a> to <a href="http://developer.android.com/sdk/installing/studio.html" target="_blank">Android Studio</a>. This has meant we have also moved to the new build system, <a href="http://www.gradle.org/ target=">Gradle</a>, and applying <a href="http://en.wikipedia.org/wiki/Test-driven_development" target="_blank">TDD</a> and <a href="http://en.wikipedia.org/wiki/Continuous_integration" target="_blank">CI</a> to our software development process. This is not the place to discuss the benefits of applying CI to a software development plan, but to talk about a problem arising when testing tasks running on different threads from the UI in Android.

&nbsp;

A test in Android is (broad definition) an extension of a <a href="http://junit.org/" target="_blank">JUnit</a> Suitcase. They do include setUp() and tearDown() for initialization/closing the tests, and infer using reflection the different test methods (starting with JUnit 4 we can use annotations to specify the priority and execution of all the tests). A typical test structure will look like:
```java
public class MyManagerTest extends ActivityTestCase {

	public MyManagerTest(String name) {
		super(name);
	}

	protected void setUp() throws Exception {
		super.setUp();
	}

	protected void tearDown() throws Exception {
		super.tearDown();
	}

	public void testDummyTest() {
		fail("Failing test");
	}

}
```
This is a very obvious instance: in a practical case we would like to test things such as HTTP requests, SQL storage, etc. In Sixt we follow a Manager/Model approach: each Model contains the representation of an Entity (a Car, a User...) and each Manager groups a set of functionality using different models (for example, our LoginManager might require of models Users to interact with them). Most of our managers perform HTTP  requests intensively in order to retrieve data from our backend. As an example, we would perform the login of a user using the following code:

&nbsp;
```java
mLoginManager.performLoginWithUsername("username", "password", new OnLoginListener() {
		@Override
		public void onFailure(Throwable throwable) {
			fail();
		}

		Override
		public void onSuccess(User customer) {
		//..
		}
	});
```
When it comes to applying this to our own test suitcase, we just make the process fail() when the result does not work as we were expecting. We can see why in the method onFailure() we call fail().

However, even if I was using a wrong username the test was still passing. Wondering why, it seemed that the test executed the code sequentially, and did not wait until the result of the callbacks came back. This is certainly a bad approach, since a modern application makes intense usage of asynchronous tasks and callback methods to retrieve data from a backend!. Tried applying the @UiThreadTest but still didn't work.

I found the following working method. I simply use CountDownLatch signal objects to implement the wait-notify mechanism (you can use synchronized(lock){... lock.notify();}, however this results in ugly code). The previous code will look as follows:
```java
final CountDownLatch signal = new CountDownLatch(1);
	mLoginManager.performLoginWithUsername("username", "password", new OnLoginListener() {
		@Override
		public void onFailure(Throwable throwable) {
			fail();
			signal.countDown();
		}

		Override
		public void onSuccess(User customer) {
			signal.countDown();
		}
	});
	signal.await();
```
&nbsp;