---
title: "Diving deeper into the Java transient modifier"
author: "Enrique López-Mañas"
date: 2016-11-25T09:26:10.318Z
lastmod: 2025-06-09T09:48:24+02:00

description: ""

subtitle: "Last week I published an article to help you understand how references do work in Java. It had a great acceptance, and I got a lot of…"

image: "/articles/2016-11-25_diving-deeper-into-the-java-transient-modifier/images/1.jpeg" 
images:
 - "/articles/2016-11-25_diving-deeper-into-the-java-transient-modifier/images/1.jpeg"


aliases:
    - "/diving-deeper-into-the-java-transient-modifier-3b16eff68f42"

---

![image](/articles/2016-11-25_diving-deeper-into-the-java-transient-modifier/images/1.jpeg#layoutTextWidth)
Nothing is tied forever. Neither are transient variables.

Last week I published an article to help you understand [how references do work in Java](https://medium.com/google-developer-experts/finally-understanding-how-references-work-in-android-and-java-26a0d9c92f83). It had a great acceptance, and I got a lot of constructive feedback. That is why I love the software community.

Today I want to present you another article diving into a topic that it is not widely used: the **transient** modifier. Personally, when I started using it I recall I was able to quickly grasp the theoretical aspect of it, although applying was a question of a different nature. Let´s gonna check closer

### The transient modifier
> A **transient** modifier applied to a field tells Java that this attribute should be excluded when the object is being serialized. When the object is being deserialized, the field will be initialized with its default value (this will typically be a _null_ value for a reference type, or _zero_/_false_ if the object is a primitive type).

You will agree with me: the theory is quite easy, but we initially fail to see the practical aspect. Where should we apply a transient modifier? When it will be useful? Is hard to come up with a factual example unless you have used it before. Like a dog chasing its tail, we fail to find a use case and therefore we cannot apply [practice to the theory](https://medium.com/@enriquelopezmanas/the-theoretical-animal-4f6901aaf571#.w9db0bi8k).

My intention with this article is to help you break this vicious cycle. Let´s check a few practical examples.

Think of an **User** object. This **User** contains among all its properties _login_, _email_ and _password_. When the data is being serialized and transmitted through the network, we can think of a few security reasons why we would not like to send the field _password_ altogether with the entire object. In this case, marking the field as **transient** will solve this security problem. How would this look like in code?
``@Data      
@NoArgsConstructor  
@AllArgsConstructor  
public class User implements Serializable {  

    private static final long serialVersionUID = 123456789L;  

    private String login;  
    private String email;  
    private transient String password;  

    public void printInfo() {  
        System.out.println(&#34;Login is: &#34; + login);  
        System.out.println(&#34;Email is: &#34; + email);  
        System.out.println(&#34;Password is: &#34; + password);  
    }  
}``

Note that this object is implementing the Interface _Serializable_, which is compulsory when you intend to serialize an object. If this interface is not implemented, you will receive a _NotSerializableException_. Note as well the declared field _serialVersionUID_. If you use any of the major Development Environments or Eclipse it will generally be recreated automatically.

If you serialise and then deserialize now an object of type User, the value password will be _null_ afterwards, since it has been marked as **transient**.
> See the annotations @Data, @NoArgsConstructor and @AllArgsConstructor? They are provided by [Lombok](https://projectlombok.org/), a Java library that makes things easier. Although in 2016 Lombok is not as useful as it was before (now languages like Kotlin generate setters and getters automatically, and you can do it with two clicks in any major Development Environment and Eclipse) I still like to use it in certain domains to keep a clean collection of Domain Models.

There is another use case I can think of when using **transient** modifiers: when an object is being derived of another. In that case, we can make our code more efficient by making the derived field **transient**.

Let´s take a look at this piece of code:
``@Data      
@NoArgsConstructor  
@AllArgsConstructor  
public class GalleryImage implements Serializable {````    private static final long serialVersionUID = 123456789L;  

    private Image image;  
    private transient Image thumbnailImage;  

    private void generateThumbnail() {  
        // This method will derive the thumbnail from the main image  
    }  

    private void readObject(ObjectInputStream inputStream)  
            throws IOException, ClassNotFoundException {  
        inputStream.defaultReadObject();  
        generateThumbnail();  
    }      
}``

In this case, the class contains a main _image_ and a _thumbnailImage_ field. The latest field will derive from the former. If we can make the _thumbnailImage_ **transient** our code we will be more efficient: a field that derives from another one will not be conveyed when the object has been serialized.

A minor point at the end of the article: as you can imagine, a **transient** variable cannot be **static** (or it does not make a lot of sense if it is). **static** fields are implicitly **transient** and will not be serialized.
> Summary: use **transient** when an object contains sensitive-data that you do not want to transmit, or when it contains data that you can derive from other elements. **static** fields are implicitly **transient**.

I write my thoughts about Software Engineering and life in general in my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share and/or leave a comment. This is the currency that fuels amateur writers.
