import re
from bs4 import BeautifulSoup
from markdownify import markdownify as md

html_content = """
<figure><img alt="" src="https://cdn-images-1.medium.com/max/768/1*xeAPuWFdYuep6JvFUdvvDw.jpeg" /></figure><p>I have always been fascinated by the above comic strip. A discussion on randomness and determinism becomes as much a philosophical issue as it is a practical one. They are used in a variety of applications: from the obvious cryptography, gaming or gambling to the less evident politics or arts.</p><p>How can we be sure that a number is random? Will observing the process mine our efforts on generating the random number, similar to the observation of a cat inside a box with a decaying radioactive atom? Despite the potential complexity of generating random numbers, we can provide an initially simple method to generate them.</p><p>When I participate in meetups or conferences as an organizer, there is one simple game I like to practice at the end of the session, and it is developing a script together with the audience that selects a random participant eligible for a gift (a cup, a t-shirt, etc… any swag generally provided by the hosting organization). The list of participants usually comes in a .CSV file, and coming from the Java world live-coding this can be a daunting task: opening streams, closing them… Damn, I am myself scared of even trying this on stage. However, in Kotlin the solution is rather simple:</p><SCRIPT SRC="https://medium.com/media/ba79231fd46bbaa59e43db42f9a18b43/href"></SCRIPT><p>(except the part of guessing how to specify the path, which is impossible to get right at the first try).</p><p>While playing this little game, very often the name of a participant comes up twice, so we jokingly express our doubts on whether the process is being truly random, or the randomness algorithm has been tweaked to favor one individual and let him/her go back home with all the swag. Developing on stage an algorithm that is able to provide a random number might require more time than using <em>java.util.Random</em>. However, we can dive into it before the stage event, and understand how randomness is implemented in Java.</p><p><a href="https://hg.openjdk.java.net/jdk8/jdk8/jdk/file/tip/src/share/classes/java/util/Random.java">OpenJDK</a> provides the open-source code of <em>java.util.Random</em>, and it is quite interesting to see how it works. It uses a <a href="https://en.wikipedia.org/wiki/Linear_congruential_generator">48-bit LCG generator</a>, based on the chapter of <a href="https://www.informit.com/articles/article.aspx?p=2221790">The Art of Computer Programming</a> by Donald Knuth. An LCG generator uses a formula similar to the following one:</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/406/1*pMUnXy3V6rB4_M0dHaAV4A.png" /><figcaption>LCG generation formula</figcaption></figure><p>Let’s take a look at each component in this formula:</p><ul><li><em>Xn </em>is our starting seed, which should be unpredictable enough. For instance, it could be the amount of time that has passed since our system started, or the amount of RAM currently being used, or a XOR of the current Date.</li><li><em>a</em> is a multiplier — randomly selected</li><li><em>c</em> is an increment- randomly selected</li><li>m is the number we use to execute the modulo operation- fixed and randomly selected</li></ul><p>The selection of the previous values may affect the quality or randomness of the output, so we can go down the rabbit hole and increase the entropy for those selected values (by either making them random as well or using a more convoluted process to generate them). In fact, Java generates the above parameters from rand48, so they get as random as it is acceptable for most usages.</p><p>The following code excerpt is an implementation in Kotlin of a linear congruential generator:</p><SCRIPT SRC="https://medium.com/media/044396dae74d67626a79cd5f3d1b33bf/href"></SCRIPT><p>LCG is fast and apt for most computers to be used. Require minimal memory, and it can execute fast. However, its usage is not intended in every field (for instance, cryptographic applications should use secure pseudorandom number generators for salt and key generation).</p><h3>Summary</h3><p>Most of the randomness generators created since the early computing days use some sort of variation of the abovementioned mechanism. However, its usage is not apt for all systems. In the upcoming article, we will see which systems should use a different random numbers generator, and which algorithms are currently available for that.</p><p>I write my thoughts about Software Engineering and life in general on my <a href="https://twitter.com/eenriquelopez">Twitter account</a>. If you have liked this article or it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.</p><img src="https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=17ca0718ae52" width="1" height="1" alt=""><hr><p><a href="https://medium.com/google-developer-experts/a-short-story-of-randomness-i-17ca0718ae52">A short story of randomness (I)</a> was originally published in <a href="https://medium.com/google-developer-experts">Google Developer Experts</a> on Medium, where people are continuing the conversation by highlighting and responding to this story.</p>
"""

# Use BeautifulSoup to parse and manipulate HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 1. Replace SCRIPT tags
for script_tag in soup.find_all('script'): # BeautifulSoup find_all is case-insensitive for tags
    script_tag.replace_with('[Embedded content from iframe could not be retrieved]')

# 2. Remove the specific img tracking pixel
img_to_remove = soup.find('img', src="https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=17ca0718ae52")
if img_to_remove:
    img_to_remove.decompose()

# 3. Remove the final <hr> and the <p> tag following it
hr_tags = soup.find_all('hr')
if hr_tags:
    last_hr = hr_tags[-1]
    next_sibling = last_hr.find_next_sibling()
    if next_sibling and next_sibling.name == 'p':
        next_sibling.decompose()
    last_hr.decompose()

# Convert the modified soup to HTML string
modified_html = str(soup)

# Convert HTML to Markdown
# Options for markdownify can be added here if needed, e.g., strip=['a'] to remove links etc.
# Default options should handle img, figure, figcaption, p, a, ul, li, h3 correctly.
markdown_output = md(modified_html, heading_style='atx')

print(markdown_output)
