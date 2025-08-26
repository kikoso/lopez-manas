---
title: "A practical implementation of Taleb’s Barbell portfolio"
author: "Enrique López-Mañas"
date: 2025-08-24T20:32:24.225Z
lastmod: 2025-08-26T09:00:03+02:00

description: ""

subtitle: "Where the author teaches himself about the details of an anti-fragile investing strategy"

image: "/articles/2025-08-24_practical-implementation-of-talebs-barbell-portfolio/images/1.jpeg" 
images:
 - "/articles/2025-08-24_practical-implementation-of-talebs-barbell-portfolio/images/1.jpeg"
 - "/articles/2025-08-24_practical-implementation-of-talebs-barbell-portfolio/images/2.png"
 - "/articles/2025-08-24_practical-implementation-of-talebs-barbell-portfolio/images/3.png"


aliases:
    - "/a-practical-implementation-of-talebs-barbell-portfolio-0f50dccb6a6c"

---


> Where the author teaches himself about the details of an anti-fragile investing strategy

Taleb advocates for an anti-fragile approach to investing and life. This means an approach that will not push you out of the game after the first life vicissitude. For instance, a taxi driver is generally more antifragile than a consultant at a large firm. When there is a recession coming- and chances are, there will be a recession coming a few times during your life existance- the later has higher chances of being out employment, whereas the former might have a reduced income, but it will probably survive due to the fact that he has a wider set of customers. This approach advocates for survival to extreme events that can wipe out an entire life of savings and construction.

![image](/articles/2025-08-24_practical-implementation-of-talebs-barbell-portfolio/images/2.png#layoutTextWidth)
Chart with the recessions during the last century. If you, like me, belong to the Millenial Generation, this is the third or forth recession that happens during your professional life.



As I want to understand also anti-fragility, it means to embrace volatility, instead of fearing it. And this does not apply only to the realm of investing. For instance, walking and sprinting could be preferable, in terms of health, to jogging. Jogging is a moderate chronic stressor, whereas sprinting is intense but short, followed by some rest (walking). This advocates also for intermittent fasting: long breaks between meals stress the body beneficially vs. constant eating (one of the rare areas that enjoys near-universal consensus is the benefit of fasting).

In investing terms, this translates into (among others) a strategy called Barbell. The Barbell strategy has, on one side, extreme conservatism, and on the other side, extreme risk-taking. Nothing in the middle. There are two core consequences of this:

*   Very limited risk: the safe part caps all the downside of the risky one.
*   The risky part has an unlimited upside.

Now, there is a lot of pontification about anti-fragile portfolios and less realization. With the present article, the author clarifies his own ideas and comes up with a practical implementation of an anti-fragile approach to investing.

As a reminder, this is what works for me and my life circumstances. You need to see what suits you, your lifestyle and circumstances. The beauty of investing is that it is partly technical, partly data-driven, partly based on your interpretation of that data, and partly gut feeling. Different people will choose different methods, they will reach different outputs and they both might be happy with the process that leads them there. Even benchmarks might not always be relevant for everybody. If you are mostly using the dividends of your portfolio, you might not care if the portfolio is not growing that much.

On a related note, comparison is the thief of joy. Do not compare yourself with others when it comes to investing or to anything else in that regard. See if the situation is acceptable for you, see if you can do it better and take decisions to move in one direction or another.

A Barbell portfolio could have 90% of its allocation to a very conservative part, and another 10% to a high-risk/high-reward part. Let’s check them in detail.

### The conservative part

Generally, as a very conservative part, the instruments that are generally proposed are short-term Treasuries, bonds, maybe physical cash, and gold if you’re paranoid. The advantage of those instruments is (generally) a predictive evolution, low risk, and low volatility. There are some disadvantages that can be talked about, like the risk of inflation eating up any profit from those instruments, the lack of liquidity for some bonds, etc. But generally, it is correct to assume that they will be safer than other alternatives in the market.

I have written a few articles [with my views](https://enriquelopezmanas.medium.com/a-gentle-introduction-to-investing-for-software-engineers-i-motivation-4cb968a8e634) [on investing](https://enriquelopezmanas.medium.com/a-recapitulation-of-investing-in-pandemic-times-976566b0b6cc). I hold most of my eggs in a basket that includes mostly companies that have been paying an increasing dividend for a number of years. According to a canonical view of risk management, this is not safe. Companies can cut the dividend anytime, and maintaining or increasing it during a period of economic downturn, regardless of how the company is performing, can be a recipe for a financial tragedy. Exxon was notably an exception during the COVID pandemic: despite the dividend not being sustainable under any metric, they increased it and they made it out well of that scenario. It could also have failed.

For me, the risk/award trade-off from investing in this companies is acceptable for my life circumstances. I am not going to say it is optimal, since the definition of optimal slides constantly, but it keeps me satisfied. This is my current portfolio distribution:
![image](/articles/2025-08-24_practical-implementation-of-talebs-barbell-portfolio/images/3.png#layoutTextWidth)
Enrique’s Fund, June 2025

Not every company is a dividend king or aristocrat; about 73% of them. I have been overtime incorporating other instruments, like CEFs, which focus on income without a constant appreciation of the principal (namely, DNP Select Income Fund, Blackrock Science &amp; Technology or Reaves Utility Income Fund). Overall, this is a portfolio that, for me has been stable over the years. Price fluctuates similarly to the S&amp;P500, income grows steadily, and the risk is acceptable for me.

### The risky part

The risk part is that one that has a large risk, and a large potential upside. For me, one of the interpretations of the anti-fragility is that I can’t be using leverage, or any instrument that will kick me out of the game when an extreme situation happens. I am assuming there will be a few Black Swans from today until the day I die, and my resistance to them must be 100%, not 99%. In the same way, I would not enter on a plane where I hear that the probability of dying with the incumbent pilot is 1%. Life is too precious to risk it, and so are my investments.

So, to implement this strategy, we discard everything that involves leverage (i.e., using money you don’t own). These are instruments like CFDs, leveraged ETFs, etc. The maximum loss must be limited to money on the risky budget, not somewhere else. So, how can we implement a high-risk/high-reward approach?

By trading CALL options on SPY, the ETF that tracks the S&amp;P 500. SPY is liquid, widely traded, and closely tied to overall market behavior. It is simpler and more accessible than something like the VIX, which is more abstract and harder to time effectively.

Here is an example. Suppose SPY is trading at $420. You buy a CALL option with 3 to 6 months until expiration, with a strike price of $460. Let us assume the premium for that option is $1.50 per share, or $150 for a standard contract of 100 shares. That is your maximum loss.

Now imagine a market rally triggered by unexpected monetary easing or strong tech performance. If SPY jumps to 500 before the option expires, your CALL becomes deep in the money. The intrinsic value is $4,000 ($500 minus $460, multiplied by 100 shares). Subtracting the $150 premium, your net gain is $3,850.

The key point is that you do not even need to exercise the option. In periods of rapid upward movement, the premium of the CALL option itself rises dramatically. You can sell the option at a much higher price than you paid. Historically, in similar market moves, SPY CALL options have returned a high multiple of the costs. I was not able to find specific closing values for options, but some literature points to a 50x or a 100x. In my very personal experience during 2025, it was possible to get a 10x or even a 20x.

This strategy offers limited downside, capped at the premium paid, and potentially large upside in times of market surges. It fits well with an antifragile mindset. You are not using borrowed money, you are not exposed to liquidation, and you cannot be forced out of the market.

The problem here, and I think this is the general problem with this strategy, it is a constant money drain until the volatility hits and you can profit from it. Investors are impatient, and money changes hands when people are impatient. It is hard to sit with a bunch of open CALLs when everybody else is getting larger returns by buying any other companies.

### How this can evolve?

It will again, depend, on your life circumstances. You can use the dividends and distributions from the Core portfolio to fund your life expenses. You can allocate a percentage of those distributions to the Risky portfolio.

I have been personally allocating a part of my investments to follow this approach for about a year now. With Trump in power it would not be unsurprising to see more volability in the markets, and 2025 is a good example: the badly called Liberation Day, the attack on Iran, the generally erratic policy…

Volatility is not instrinsically bad if you know how to benefit from it. Taleb has a decent amount of literature on this topic, and if you haven’t read them, you can start reading the Incerto series.
