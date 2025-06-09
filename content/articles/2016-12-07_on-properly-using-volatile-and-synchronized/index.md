---
title: "On properly using volatile and synchronized"
author: "Enrique López-Mañas"
date: 2016-12-07T09:53:03.689Z
lastmod: 2025-06-09T09:48:26+02:00

description: ""

subtitle: "In the last weeks I have been writing about the transient modifier and the different types of references available in Java. I want to hold…"

image: "/articles/2016-12-07_on-properly-using-volatile-and-synchronized/images/1.jpeg" 
images:
 - "/articles/2016-12-07_on-properly-using-volatile-and-synchronized/images/1.jpeg"


aliases:
    - "/on-properly-using-volatile-and-synchronized-702fc05faac2"

---

In the last weeks I have been writing about the [transient](https://medium.com/google-developer-experts/diving-deeper-into-the-java-transient-modifier-3b16eff68f42#.tes59mm9a) modifier and the different [types of references](https://medium.com/google-developer-experts/finally-understanding-how-references-work-in-android-and-java-26a0d9c92f83#.ixg2oyvhj) available in Java. I want to hold the topic of underused/misused topics in Java and bring you this week the **volatile** and **synchronized** modifiers .

Multithreading is an entire discipline that takes years to master and properly understand. We will keep a short introduction in this article.

In computing, a resource can be accessed from different threads concurrently. This can lead to inconsistency and corrupt data. A thread _ThreadA_ accesses a resource and modifies it. In the meantime, the thread _ThreadB_ starts accessing the same resource. Data may get corrupted since it is concurrently being modified. Let´s analyze an example without any kind of protection:




If you execute this command, the result is eclectic and non-deterministic. Each time you will end up with a different random output. That is because each thread execute in different instants.

```
Starting Thread 1 output:  
Starting Thread 2 output:  
Selected number is: 5  
Selected number is: 4  
Selected number is: 3  
Selected number is: 2  
Selected number is: 5  
Selected number is: 4  
Selected number is: 1  
Selected number is: 3  
Selected number is: 2  
Selected number is: 1  
Thread Thread 1 finishing.  
Thread Thread 2 finishing.
```

Both modifiers deal with multithreading and protection of code sections from threads accesses. My gut feeling is that **synchronized** is more widely used and understood than **volatile**, so I will start my article explaining how it works. We will need it as well later to understand the differences with **volatile**.

### synchronized modifier

The **synchronized** modifier can be applied to an statement block or a method. **synchronized** provides protection by ensuring that a crucial section of the code is never executed concurrently by two different threads, ensuring data consistency. Let´s apply the modifier **synchronized** in the previous example to see how it would be protected:




Note that in this example we have added **synchronized** to the section where the function **printCount()** runs. If you execute now this function, the result will always be the same:

```
Starting Thread 1  
Starting Thread 2  
Selected number is: 5  
Selected number is: 4  
Selected number is: 3  
Selected number is: 2  
Selected number is: 1  
Thread Thread 1 finishing.  
Selected number is: 5  
Selected number is: 4  
Selected number is: 3  
Selected number is: 2  
Selected number is: 1  
Thread Thread 2 finishing.
```

Now that **synchronized** has been explained, let´s take a look on **volatile**.

### volatile modifier

We have mentioned before that **synchronized** modifier could apply to blocks and methods. The first difference between them is that **volatile** is a modifier that can be applied to fields.

A small note on how Java memory and multithreading work. When we are working with multithreading environments, each thread creates its own copy on a local cache of the variable they are dealing with. When this value is being updated, the update happens first in the local cache copy, and not in the real variable. Therefore, other threads are agnostic about the values that other threads are changing.

Here **volatile** changes the paradigm. When a variable is declared as **volatile**, it will not be stored in the local cache of a thread. Instead, each thread will access the variable in the main memory and other threads will be able to access the updated value. Let´s compare all the methods for a proper understanding:

```Java
int firstVariable;  
int getFirstVariable() {
    return firstVariable;
}  

volatile int secondVariable;  
int getSecondVariable() {
    return secondVariable;
}  

int thirdVariable;  
synchronized int getThirdVariable() {
    return thirdVariable;
}
```

The first method is non-protected. A thread T1 will access the method, create its own local copy of _firstVariable_ and play with it. In the meantime, T2 and T3 can also access _firstVariable_ and modify its value. T1, T2 and T3 will have their own values of _firstVariable_, which might not be the same and that have not been copied to the Main memory of java, where the real results are hold.

_getSecondVariable()_, on the other hand, accesses a variable that has been declared as **volatile**. That means, each thread is still able to access the method or block since it has not been protected with **synchronized**, but they will all access the same variable from the main memory, and will not create their own local copy. Each thread will be accessing the same value.

And as we can imagine from the previous examples, getThirdVariable() will only be accessed from one thread at a time. That ensures that the variable will remained synchronized throughout all the threads executions.

### Usefulness of volatile and synchronized

After reading this short article, a question will likely pop-up in your mind. I understand the theoretical implications, but what are the practical ones? **synchronized** will probably be easier to understand at this point, but when it is useful to apply the **volatile** modifier? I like to showcase always an example to provide a better understanding.

Think of a _Date_ variable. The _Date_ variable always need to be the same, seems it updates on a regular pace. Each Thread accessing a _Date_ variable that has been declared as **volatile** will always show the same value.

There are two main aspects regarding thread safety. One is execution control, and the other one is memory visibility. Whereas **volatile** provides memory visibility (all threads will access the same value from the main memory) there is no guarantee of execution control, and this latest can only be achieved via **synchronized**.

Also, in Java all read and write operations will be atomic for a **volatile** variable (including _long_ and _double_ variables). Many platforms perform the operations in _long_ and _double_ in two steps, writing/reading 32 bytes at a time, and allowing two threads to see two different values. This can be avoided by using **volatile**.

Thanks [Erik Hellman](https://twitter.com/erikhellman) for your code and article review, you rock.

I write my thoughts about Software Engineering and life in general in my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share and/or leave a comment. This is the currency that fuels amateur writers.
