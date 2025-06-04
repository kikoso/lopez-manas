+++
title = "Vibe Coding, Kotlin, Finance, and Data Visualization"
date = "2025-04-12"
tags = ["finance", "kotlin", "programming", "investing"]
images = []
+++

![](https://cdn-images-1.medium.com/max/1024/1*ZwgQvwiwhHiEZc2j7905DQ.jpeg)

Recently, I came across a paper discussing an experiment and tried to reproduce it. Here’s a brief summary:

**- Portfolio A**: In a bull market, grows by 20%; in a bear market, drops by 20%.
**- Portfolio B**: In a bull market, grows by 25%; in a bear market, drops by 35%.
**- Bull market probability:** 75%.

![](https://cdn-images-1.medium.com/max/1024/1*qJ4nV9eXJYn_FQM_ypUxlw.png)

According to the paper, both portfolios should have a one-year expected return of 10%. However, the paper claims that Portfolio A wins over Portfolio B around 90% of the time at the end of a 30-year simulation. This sounds a bit too excessive to me (it means that, at the end of the entire simulation, 9 times out of 10 portfolio A wins). I was expecting this number to be lower. The author also mentioned that he was using GenAI to generate the code, and he even mentions “this process seems like magic”. Strong indications that the code is likely not correct.

So I decided, also in preparation for my [KotlinConf session](https://kotlinconf.com/speakers/2f606e32-997a-4b74-8420-76a47e7d66a3), to run a Monte Carlo simulation. I found that Portfolio A outperforms Portfolio B around 66% of the time. So either my calculation was wrong, or the calculation on the paper wasn’t accurate.

After a valuable exchange with one of my Data Science reference experts, [Alexander Nozik](https://medium.com/u/1d85b0f0c1a7), it seems that the paper was making an, allegedly, wrong assumption: by using two independent samples to generate the sample, so the variance is larger. By using the same generator for both, which is what happens in a real-life scenario, this makes more sense.

The following sample uses two separate random generators, both seeded with the same fixed value (123) This ensures reproducibility: every time you run the simulation, the results are the same.

Because the seeds are the same, both random number generators will generate the same sequence of random numbers (at least initially). But since they’re passed independently to different portfolio simulations, they stay in sync but separate. Good for a fair comparison.

[Medium Media](https://medium.com/media/65bd2f6d3f1ead49ff54501bea002907/href)

The following snippet uses asingle Random instance, seeded with the current time. So: no reproducibility . Results change on every run.

The same random sequence is shared between portfolioA and portfolioB during each iteration. This might lead to coupled randomness (i.e., the same stream drives both portfolios). This is undesirable if you want the portfolios to evolve independently.

[Medium Media](https://medium.com/media/bb92f2535a2c5e2a3b3c3a163788c23b/href)

The result? Using the first code snippet (arguably the correct approach for this simulation) makes portfolio A the winner 65% of the time, with portfolio B defeating A 35% of the time. The second code snippet reverses the results, giving portfolio A the best performance 90% of the time, compared to 10% for portfolio B. The difference, in the end, is significant.

Datalore file with the sources can be found here:

[https://datalore.jetbrains.com/notebook/juj4AIqkd2CE3c9AVDs48P/CIokUJ6mIk9yOxGhD3qYd2/](https://datalore.jetbrains.com/notebook/juj4AIqkd2CE3c9AVDs48P/CIokUJ6mIk9yOxGhD3qYd2/)

Here you can find one image of one run of the Montecarlo simulation using the portfolio using the random generator with a Time-Based seed (using, by the way, [Plotly.kt](https://github.com/SciProgCentre/plotly.kt): a fantastic tool for Data Visualization).

![](https://cdn-images-1.medium.com/max/1024/1*-kYTFtQPHfn6qtpTnm7igQ.jpeg)

Here there is another one with the overall distribution of the final portfolio values after 1000 runs of 30 years (this time using a [Histogram Plot from Kandy](https://kotlin.github.io/kandy/histogram-bar-plot.html))

![](https://cdn-images-1.medium.com/max/1024/1*5hqObBXwpaJq5AiNDyylbw.png)

### Conclusion

For me, the key takeaway from this experiment is the importance of using consistent randomization methods when simulating financial models. Small differences in how randomness is generated can significantly affect the results, as demonstrated in the comparison of Portfolio A and Portfolio B. Using separate random generators for each portfolio leads to exaggerated differences, whereas using a single, shared generator yields a more realistic, balanced outcome.

This serves as a cautionary reminder for anyone involved in financial simulations or decision-making: even a seemingly minor coding mistake or incorrect assumption can lead to vastly different conclusions. In the case of large-scale financial modeling, such errors could result in multi-million-dollar discrepancies. Always be diligent and cautious when working with randomization in simulations — especially when relying on auto-generated code (GenAI should be called *complex auto-completion* more often, to raise awareness of what we are really dealing with here).

I share my thoughts about Software Engineering and life in general on my [Mastodon account](https://kotlin.social/@eenriquelopez). If you have liked this article or if it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.

Disclaimer: This article didn’t use Generative AI in its elaboration.
