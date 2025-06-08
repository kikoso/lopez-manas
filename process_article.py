import xml.etree.ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
import markdownify as md
import os
import re

# XML content as a string
XML_CONTENT = """
<item>
<title>
<![CDATA[ From Java to Kotlin and back (III): Calling Java from Kotlin ]]>
</title>
<link>https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-iii-calling-java-from-kotlin-f33f5c246d69?source=rss-f08187f6a023------2</link>
<guid isPermaLink="false">https://medium.com/p/f33f5c246d69</guid>
<category>
<![CDATA[ java ]]>
</category>
<category>
<![CDATA[ android ]]>
</category>
<category>
<![CDATA[ kotlin ]]>
</category>
<dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">
<![CDATA[ Enrique López-Mañas ]]>
</dc:creator>
<pubDate>Sun, 14 Mar 2021 07:41:42 GMT</pubDate>
<atom:updated xmlns:atom="http://www.w3.org/2005/Atom">2021-03-15T11:54:17.777Z</atom:updated>
<content:encoded xmlns:content="http://purl.org/rss/1.0/modules/content/">
<![CDATA[ <figure><img alt="" src="https://cdn-images-1.medium.com/max/1024/1*64ZHGwroVJgbBDbC2X_gSQ.jpeg" /></figure><p>This article is part of a series. You can find the remaining article of the series here:</p><p><a href="https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-i-java-calling-kotlin-9abfc6496b04">From Java to Kotlin and back (I) — Calling Kotlin from Java</a></p><p><a href="https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-ii-calling-kotlin-from-java-3bdf72da6e52">From Java to Kotlin and back (II): Calling Kotlin from Java</a></p><p>In this last chapter of the series, we will evaluate consideration when calling Java code from Kotlin.</p><p>One could argue that even in this situation happens often, keeping considerations in mind for some code that might legacy is not that practical. Kotlin has also been designed with interoperability in mind, so Java code from Kotlin is much more “callable” than the other way around, since the design has been in mind since its conception. However, there are a few points that you can keep in mind when working on your Java code, and we would like to explain them in this article.</p><h3>Annotations</h3><p>Since Java lacks a few of the powerful features we already have on Kotlin, we will rely significantly on some annotations that can prepare our Java code to interface with Kotlin.</p><h4>Nullability</h4><p>Whereas nullability is one of the core features in Kotlin, Java does not provide out-of-the-box support for it. Every parameter in Java should always have a nullability annotation. Otherwise, they are understood as “<a href="https://p5v.medium.com/platform-types-in-kotlin-5caceeb556ad">platform types</a>”, which have an ambiguous way to determine nullability and can trigger runtime errors, pretty much what Kotlin nullability aims to avoid. For example, consider the following piece of code:</p><iframe src="" width="0" height="0" frameborder="0" scrolling="no"><a href="https://medium.com/media/70b0e45a013894410e4b694efa9868ea/href">https://medium.com/media/70b0e45a013894410e4b694efa9868ea/href</a></iframe><p>If we try to call the function <em>doNotUseAnnotation </em>with false, the code will trigger an Exception. Because we didn’t add any annotation, Kotlin implies that the function is not nullable. In Java, we would be setting up the nullability as follows:</p><iframe src="" width="0" height="0" frameborder="0" scrolling="no"><a href="https://medium.com/media/ecb0b0afd7cf0c39e2361fa002fef043/href">https://medium.com/media/ecb0b0afd7cf0c39e2361fa002fef043/href</a></iframe><p>The most common ones that we will find are @Nullable and @NotNull, present in the package <em>org.jetbrains.annotation</em> but also in <em>com.android.annotation</em> and others, such as Lombok.</p><p>Generally, Java code that has not been properly annotated can lead to unpredictable behavior. If you have some experience in the Android realm, where the framework is written in Java, you will be constantly relying on annotations that are not all the time where they should be.</p><p>If you are working on Java code that will be potentially exposed to Kotlin, remember to use Nullability annotations to facilitate the lives on the other side of the fence.</p><h4>@UnderMigration annotation</h4><p>The @UnderMigration annotation is pretty useful when we are maintaining some Java code, and we want to inform our potential clients of its current status (please note that the annotation can be found in a separate artifact, <em>kotlin-annotations-jvm</em>)</p><p>@UnderMigration status can have three different values, similar to the <a href="https://blog.jetbrains.com/kotlin/2020/06/kotlin-1-4-m2-released/#explicit-api-mode">explicit API mode</a> introduced in Kotlin 1.4:</p><ul><li>MigrationStatus.STRICT will deliver a compilation error when there is a misusage of an annotation, causing the code to fail.</li><li>MigrationStatus.WARN: similar to the previous one, but just dropping a warning</li><li>MigrationStatus.IGNORE ignores completely the usage of the annotations.</li></ul><h3>Getters and setters in Java</h3><p>Kotlin uses property access instead of getters and setters, like Java. The definition of a getter is a no argument with a name starting with <em>get</em>, and the definition of a setter is a one-argument method with a name starting with <em>set</em>. Boolean getters start with is, so we can use a more natural human language to ask for the value of the property (<em>isClosed</em>, is <em>Finished</em>, etc). Keep this in mind when designing your Java class, although this is pretty much standard. Interestingly, if your attribute provides only a setter it will not be visible as a property, since Kotlin does not support set-only properties (and this is generally an <a href="https://softwareengineering.stackexchange.com/questions/50554/why-it-is-not-recommended-to-have-set-only-property">anti-pattern</a>).</p><p>The following Java class:</p><iframe src="" width="0" height="0" frameborder="0" scrolling="no"><a href="https://medium.com/media/8ace49bae8dc97fd0fb23fe0097ef4a2/href">https://medium.com/media/8ace49bae8dc97fd0fb23fe0097ef4a2/href</a></iframe><p>will be accessed like the following block in Kotlin:</p><iframe src="" width="0" height="0" frameborder="0" scrolling="no"><a href="https://medium.com/media/958d04b23837e86153ae5b618f66bab3/href">https://medium.com/media/958d04b23837e86153ae5b618f66bab3/href</a></iframe><h3>Kotlin keywords</h3><p>Kotlin has a few hard keywords that we should not be using in our Java code, since the Kotlin counterpart will need backticks to call them.</p><iframe src="" width="0" height="0" frameborder="0" scrolling="no"><a href="https://medium.com/media/1c2297e4b429db246f2ccb7b9b802b8a/href">https://medium.com/media/1c2297e4b429db246f2ccb7b9b802b8a/href</a></iframe><p>Protip: these backticks can be used all around when naming methods and variables in Kotlin, not only in the case of hard keywords or tests.</p><iframe src="" width="0" height="0" frameborder="0" scrolling="no"><a href="https://medium.com/media/456d63a09dad282859876119713dd9e0/href">https://medium.com/media/456d63a09dad282859876119713dd9e0/href</a></iframe><h3>Summary</h3><p>This last article presents tips to design and work on our Java code when it will be later on consumed in Kotlin. Java code can expose code to Kotlin with lesser effort than the other way around, but the points explored will be able to help you achieve a more efficient interoperable code.</p><p>I write my thoughts about Software Engineering and life in general on my <a href="https://twitter.com/eenriquelopez">Twitter account</a>. If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.</p><img src="https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=f33f5c246d69" width="1" height="1" alt=""><hr><p><a href="https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-iii-calling-java-from-kotlin-f33f5c246d69">From Java to Kotlin and back (III): Calling Java from Kotlin</a> was originally published in <a href="https://medium.com/google-developer-experts">Google Developer Experts</a> on Medium, where people are continuing the conversation by highlighting and responding to this story.</p> ]]>
</content:encoded>
</item>
"""

# Define namespaces
NAMESPACES = {
    'dc': 'http://purl.org/dc/elements/1.1/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'atom': 'http://www.w3.org/2005/Atom'
}

def sanitize_filename(title):
    """Sanitizes a title string to be used as a filename."""
    # Remove CDATA and any other unwanted characters
    title = title.strip()
    # Replace spaces and special characters with hyphens
    title = re.sub(r'\s+', '-', title)
    title = re.sub(r'[^\w\s-]', '', title).lower()
    return title

def process_article():
    # Parse the XML
    root = ET.fromstring(XML_CONTENT)

    # Extract fields
    title = root.find('title').text.strip()
    pub_date_str = root.find('pubDate').text.strip()

    # Handle dc:creator with namespace
    creator_element = root.find('dc:creator', NAMESPACES)
    creator = creator_element.text.strip() if creator_element is not None else "Unknown Author"

    categories = [category.text.strip() for category in root.findall('category')]

    # Handle content:encoded with namespace
    content_element = root.find('content:encoded', NAMESPACES)
    html_content = content_element.text.strip() if content_element is not None else ""

    # Format pubDate
    pub_date_obj = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %Z')
    formatted_date = pub_date_obj.strftime('%Y-%m-%d')

    # Create TOML frontmatter
    frontmatter = f"""+++
title = "{title}"
date = "{formatted_date}"
tags = {categories}
authors = ["{creator}"]
images = []
+++
"""

    # Process HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Replace iframes
    for iframe in soup.find_all('iframe'):
        iframe.replace_with("[Embedded content from iframe could not be retrieved]")

    # Remove tracking pixel
    for img in soup.find_all('img', src=re.compile(r"https://medium.com/_/stat")):
        img.decompose()

    # Remove final hr and the "originally published" paragraph
    hr_tag = soup.find('hr')
    if hr_tag:
        next_p = hr_tag.find_next_sibling('p')
        if next_p and "originally published in" in next_p.text:
            next_p.decompose()
        hr_tag.decompose()

    cleaned_html = str(soup)
    markdown_content = md.markdownify(cleaned_html, heading_style='atx')

    # Create output directory if it doesn't exist
    output_dir = 'content/articles'
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    filename = sanitize_filename(title) + '.md'
    filepath = os.path.join(output_dir, filename)

    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(markdown_content)

    print(f"Article processed and saved to {filepath}")

if __name__ == '__main__':
    process_article()
