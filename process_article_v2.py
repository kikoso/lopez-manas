import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import markdownify as md

# Full HTML content as a string (ensure this is the complete HTML provided by the user)
HTML_CONTENT = """
<header>
<h1 class="p-name">From Java to Kotlin and back (II): Calling Kotlin from Java</h1>
</header>
<section data-field="subtitle" class="p-summary">
In the previous article, we explored how Java and Kotlin can interact with each other, and some considerations in this regard. In this…
</section>
<section data-field="body" class="e-content">
<section name="4726" class="section section--body section--first section--last"><div class="section-divider"><hr class="section-divider"></div><div class="section-content"><div class="section-inner sectionLayout--fullWidth"><figure name="a934" id="a934" class="graf graf--figure graf--layoutFillWidth graf--leading"><img class="graf-image" data-image-id="1*4E0BvbPibFWgKGs1iPi-9w.jpeg" data-width="4928" data-height="3264" data-is-featured="true" src="https://cdn-images-1.medium.com/max/2560/1*4E0BvbPibFWgKGs1iPi-9w.jpeg"></figure></div><div class="section-inner sectionLayout--insetColumn"><h3 name="36b1" id="36b1" class="graf graf--h3 graf-after--figure graf--title">From Java to Kotlin and back (II): Calling Kotlin from Java</h3><p name="4e00" id="4e00" class="graf graf--p graf-after--h3">This article is part of a series. You can find the remaining article of the series here:</p><p name="4438" id="4438" class="graf graf--p graf-after--p"><a href="https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-ii-calling-kotlin-from-java-3bdf72da6e52" data-href="https://medium.com/google-developer-experts/from-java-to-kotlin-and-back-ii-calling-kotlin-from-java-3bdf72da6e52" class="markup--anchor markup--p-anchor" rel="noopener" target="_blank">From Java to Kotlin and back (II): Calling Kotlin from Java</a></p><p name="90bf" id="90bf" class="graf graf--p graf-after--p"><a href="https://enriquelopezmanas.medium.com/from-java-to-kotlin-and-back-iii-calling-java-from-kotlin-f33f5c246d69" data-href="https://enriquelopezmanas.medium.com/from-java-to-kotlin-and-back-iii-calling-java-from-kotlin-f33f5c246d69" class="markup--anchor markup--p-anchor" rel="noopener" target="_blank">From Java to Kotlin and back (III): Calling Java from Kotlin</a></p><p name="eabb" id="eabb" class="graf graf--p graf-after--p">In the previous article, we explored how Java and Kotlin can interact with each other, and some considerations in this regard. In this second edition, we will keep reflecting on some relevant aspects to consider when Java is calling Kotlin.</p><h3 name="616c" id="616c" class="graf graf--h3 graf-after--p">Properties in classes</h3><p name="e306" id="e306" class="graf graf--p graf-after--h3">Likely the first Kotlin feature highlighted when we heard about the language, data classes. Data classes are mainly thought to hold data with some extra functionality allowed, and hence called Data classes. We like them because they automatically generate some functions (getters, setters, <code class="markup--code markup--p-code">toString()</code>, <code class="markup--code markup--p-code">copy()</code>, <code class="markup--code markup--p-code">equals()</code> and <code class="markup--code markup--p-code">hashCode()</code>), which otherwise we need to manually create. For instance, a data class containing just <code class="markup--code markup--p-code">var name : String</code> will compile into the following in Java:</p><figure name="a928" id="a928" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/ab0a9de318cf2f99e022c7ebe4e24cb2.js"></script><figcaption class="imageCaption">Data class compiled in Java</figcaption></figure><p name="4fb6" id="4fb6" class="graf graf--p graf-after--figure">If the name of the var starts with is, then the resulting getter will start with the prefix is. For instance. if we have <code class="markup--code markup--p-code">var isYoung: Boolean</code>, the resulting setter will be:</p><figure name="7987" id="7987" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/fb2abc071a674fc74fd66309b8e49c68.js"></script><figcaption class="imageCaption">Resulting setter of an “is” attribute</figcaption></figure><p name="01b2" id="01b2" class="graf graf--p graf-after--figure">Keep in mind that this does not only work for boolean types, but for any type.</p><h3 name="d452" id="d452" class="graf graf--h3 graf-after--p">Naming with JvmName</h3><p name="d0bb" id="d0bb" class="graf graf--p graf-after--h3">We explored in the previous article some usages for <code class="markup--code markup--p-code">@JvmName</code>, and I would like to provide some more ideas.</p><p name="4910" id="4910" class="graf graf--p graf-after--p">For instance, whereas Kotlin supports Optional values, in Java we do not really name it that way. So if we are designing extension functions that might be called for Java, we might want to provide them a different name so they are idiomatic enough for our Java code. Let’s check the following code:</p><figure name="f1e5" id="f1e5" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/045a8ed69dd44ce924aaddd0f86c9f8e.js"></script><figcaption class="imageCaption">Kotlin class with idiomatic naming</figcaption></figure><p name="4ba2" id="4ba2" class="graf graf--p graf-after--figure"><code class="markup--code markup--p-code">asOptional </code>will likely confuse our Java peers, and what they are looking for underneath is whether a variable is potentially nullable or not. Hence, we specify <code class="markup--code markup--p-code">@JvmName(“ofNullable”)</code>, to change the resulting JVM name. This will be called as follows in Java:</p><figure name="4c03" id="4c03" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/2ba80e8b825c07546064aeb4794a217d.js"></script><figcaption class="imageCaption">Java calling JvmName function</figcaption></figure><p name="bacd" id="bacd" class="graf graf--p graf-after--figure">Note also that Java can access the different types of the sealed class.</p><h3 name="6240" id="6240" class="graf graf--h3 graf-after--p">Default methods in Java interface</h3><p name="c85e" id="c85e" class="graf graf--p graf-after--h3">Since Java 1.8, Java interfaces can contain default methods. Without getting too much into detail, they enable you to add new functionality to an existing interface, ensuring compatibility with code written for older versions of those mentioned interfaces. The <a href="https://docs.oracle.com/javase/tutorial/java/IandI/defaultmethods.html" data-href="https://docs.oracle.com/javase/tutorial/java/IandI/defaultmethods.html" class="markup--anchor markup--p-anchor" rel="noopener" target="_blank">following link</a> explains in detail how they work.</p><p name="5b16" id="5b16" class="graf graf--p graf-after--p">If we want to make all non-abstract members of a Kotlin interface becoming default for any Java class that implements them, we need to compile the code with the following option:</p><p name="8d12" id="8d12" class="graf graf--p graf-after--p"><code class="markup--code markup--p-code">-Xjvm-default=all</code></p><p name="b03c" id="b03c" class="graf graf--p graf-after--p">Let’s see this in practice. Consider the following interface with a default method and that we are compiling with <code class="markup--code markup--p-code">-Xjvm-default=all</code>:</p><figure name="ab8a" id="ab8a" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/2472fe6070723dc3dd5151b16650714a.js"></script><figcaption class="imageCaption">Default interface Kotlin</figcaption></figure><p name="fadf" id="fadf" class="graf graf--p graf-after--figure">This will be implemented in a Java class as follows:</p><figure name="25a7" id="25a7" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/3bb1224943435915ce851066de94cba3.js"></script><figcaption class="imageCaption">Java class implementing default interface</figcaption></figure><p name="f3b3" id="f3b3" class="graf graf--p graf-after--figure">And of course, Java will be able to call all the functions of the interface:</p><figure name="b4f1" id="b4f1" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/890cc08b80abdb03c6a8d5d38ba2d8c9.js"></script><figcaption class="imageCaption">Java class calling default methods</figcaption></figure><p name="bd63" id="bd63" class="graf graf--p graf-after--figure">An interesting tweak is that, of course, Java can also override all the default functions. So if in our example, <code class="markup--code markup--p-code">functionA()</code>needs to have a custom implementation in the class implementing it, we can safely override it.</p><h3 name="e688" id="e688" class="graf graf--h3 graf-after--p">Getter and Setter renaming</h3><p name="9c4d" id="9c4d" class="graf graf--p graf-after--h3">Occasionally we might want to rename our getters and setters. A typical case is when returning an attribute can be composed by operations on some other attributes (for instance, something like returning a name with <code class="markup--code markup--p-code">getName()</code> that adds some sort of prefix or evaluation to determine the complete string being returned). We can easily do it with the annotations <code class="markup--code markup--p-code">@get:JvmName</code> and <code class="markup--code markup--p-code">@set:JvmName</code>as follows:</p><figure name="c736" id="c736" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/041e8a7d6515be05d6dac4af9d118023.js"></script><figcaption class="imageCaption">Changing getters and setters</figcaption></figure><h3 name="375f" id="375f" class="graf graf--h3 graf-after--figure">Null-safety</h3><p name="6d79" id="6d79" class="graf graf--p graf-after--h3">Kotlin is null-safe, Java is not null safe. When we are calling Kotlin functions from Java we can always pass a <code class="markup--code markup--p-code">null</code> as a non-null parameter. Kotlin generates runtime checks for all public functions that expect non-nulls. This provokes a <code class="markup--code markup--p-code">NullPointerException</code> in the Java code immediately. Be mindful when defining nullable and non-nullable parameters in functions, since what in Kotlin is a pleasant experience might become a party of runtime Exceptions in your Java code.</p><h3 name="f72b" id="f72b" class="graf graf--h3 graf-after--p">Using the type Nothing in Java</h3><p name="d743" id="d743" class="graf graf--p graf-after--h3">Or technically, not using it, since there is no natural counterpart in the Java world. In fact, it is interesting because java Void accepts null, but Nothing doesn’t. It is in fact a complex problem in Computer Science that we can philosophically tackle in another tackle, since we are trying to represent nothing with something, and we are biological creatures that deal with physical manifestation of items in our world. Leaving nothingness aside, the Nothing type gets represented with a raw type in Java, so keep this in mind when working with Nothing:</p><figure name="16a6" id="16a6" class="graf graf--figure graf--iframe graf-after--p"><script src="https://gist.github.com/kikoso/2b91bd7b562104061fe1ebf6cf8006a3.js"></script><figcaption class="imageCaption">Nothing in Java</figcaption></figure><h3 name="30d9" id="30d9" class="graf graf--h3 graf-after--figure">Summary</h3><p name="41b8" id="41b8" class="graf graf--p graf-after--h3">This article has explored some more tips on calling Kotlin code from Java. The following article of the series will explore the reverse side of the river, and we will learn how Kotlin can code with legacy Java code, and which considerations we need to keep in mind.</p><p name="860f" id="860f" class="graf graf--p graf-after--p graf--trailing">I write my thoughts about Software Engineering and life in general on my <a href="https://twitter.com/eenriquelopez" data-href="https://twitter.com/eenriquelopez" class="markup--anchor markup--p-anchor" rel="noopener nofollow noopener" target="_blank">Twitter account</a>. If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.</p></div></div></section>
</section>
"""

def sanitize_filename(title):
    """Sanitizes a title string to be used as a filename."""
    title = title.strip()
    title = re.sub(r'\s+', '-', title)
    title = re.sub(r'[^\w\s-]', '', title).lower()
    return title

def process_article_v2():
    # Parse the HTML
    soup = BeautifulSoup(HTML_CONTENT, 'html.parser')

    # Extract title
    title_element = soup.find('h1', class_='p-name')
    title = title_element.text.strip() if title_element else "Untitled Article"

    # Extract main article body
    body_section = soup.find('section', attrs={'data-field': 'body', 'class': 'e-content'})

    if not body_section:
        print("Error: Could not find the main body section of the article.")
        return

    # --- Frontmatter ---
    author = "Enrique López-Mañas"
    date_str = "2021-03-07"
    tags = ["java", "kotlin", "interoperability"]

    frontmatter = f"""+++
title = "{title}"
date = "{date_str}"
tags = {tags}
authors = ["{author}"]
images = []
+++
"""

    # --- HTML to Markdown Conversion for the body ---
    body_soup = BeautifulSoup(str(body_section), 'html.parser') # Re-parse to isolate changes

    # Replace Gist scripts
    for script in body_soup.find_all('script', src=re.compile(r"https://gist.github.com/.*/(.*?).js")):
        gist_id = script['src'].split('/')[-1].replace('.js', '')
        script.replace_with(f"[Gist {gist_id}]")

    # Remove section-divider divs
    for div in body_soup.find_all('div', class_='section-divider'):
        div.decompose()

    # Remove empty figcaption elements
    for figcaption in body_soup.find_all('figcaption'):
        if not figcaption.text.strip():
            figcaption.decompose()

    cleaned_html_body = str(body_soup)
    markdown_content = md.markdownify(cleaned_html_body, heading_style='atx')

    # --- File Output ---
    output_dir = 'content/articles'
    os.makedirs(output_dir, exist_ok=True)

    filename_base = sanitize_filename(title)
    filepath = os.path.join(output_dir, filename_base + '.md')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(markdown_content)

    print(f"Article processed and saved to {filepath}")

if __name__ == '__main__':
    process_article_v2()
