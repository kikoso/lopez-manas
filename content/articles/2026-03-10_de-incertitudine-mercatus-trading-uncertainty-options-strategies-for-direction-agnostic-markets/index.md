---
title: "De Incertitudine Mercatus"
author: "Enrique López-Mañas"
date: 2026-03-10T12:00:00.000Z

description: "Trading Uncertainty: Options Strategies for Direction-Agnostic Markets"

subtitle: "Where the author embraces pure volatility."

image: "/articles/2026-03-10_de-incertitudine-mercatus-trading-uncertainty-options-strategies-for-direction-agnostic-markets/images/1.jpg" 
images:
 - "/articles/2026-03-10_de-incertitudine-mercatus-trading-uncertainty-options-strategies-for-direction-agnostic-markets/images/1.jpg"

---

> Where the author embraces pure volatility.

Trading Uncertainty: Options Strategies for Direction-Agnostic Markets

I wrote somewhere else a short excerpt with my opinion of the current state of the world in AI, financial bubbles, and company valuations that I will reproduce here:

There are growing discussions about a possible bubble in the AI world. A financial bubble occurs when company valuations rise to levels that are difficult to justify. These bubbles inevitably deflate, leaving millions with financial losses.

In technology, we have the example of the dot-com bubble of 2000. A prominent case was pets.com: once the darling of the boom, it eventually collapsed. Today, we see names like Nvidia, OpenAI, and others raising similar concerns about whether we are on a comparable trajectory. History does not repeat itself, but it often rhymes.

It is important to distinguish between two ideas: the existence of a bubble in a sector, and whether investors can still make money by participating in it.

The dot-com bubble burst, but the internet remained. The collapse affected valuations, not the underlying technology. Many companies that were part of that era, like Microsoft and Cisco, survived and thrived afterward.

The AI sector could face a similar adjustment, but my view is that AI is here to stay. Valuations might correct for some companies, and priorities may shift toward energy consumption, real-world utility, and perhaps a reassessment of whether we truly need AI in every chatbot or workflow.

Whether there is a bubble or not is hard to say. No one really knows, despite all the opinionated articles that appear daily. My view is that AI will remain, but many companies will eventually leave the field, and usage will normalize as we recognize its limitations. It may happen sooner or later, but the future we end up with will likely look very different from what we see today.

The financial world keeps behaving irrationally. 

#### Embracing the unknown

So, we find ourselves in a peculiar situation. We are looking at a market, specifically the tech sector heavily influenced by AI, and we know that a significant event is likely. We just don't know which event. The bubble might burst, sending valuations crashing down to earth. Or, alternatively, the massive capital expenditure might suddenly pay off in an unforeseen breakthrough, sending valuations skyrocketing even further. 

If you are following a traditional investing approach, this is a nightmare. If you buy a stock, you need it to go up. If you short a stock, you need it to go down. You are forced to predict the future direction of an irrational system. 

But what if you didn't have to? What if you could say, "I have no idea if this company will be worth double or half its current value in six months, but I am absolutely certain it won't stay exactly where it is today."

This is where options strategies, specifically the Long Straddle, come into play. It is a tool for the direction-agnostic investor. It perfectly aligns with an anti-fragile mindset: you are positioning yourself to benefit from extreme volatility, regardless of the direction the wind blows.

### The Long Straddle

To implement a long straddle, you simultaneously buy a Call option (betting the price goes up) and a Put option (betting the price goes down) on the same underlying asset, with the same strike price, and the same expiration date.

Let's use a hypothetical example. Suppose there is a widely discussed AI company, let's call it DontBeEvil, currently trading at $200 per share. You believe that their upcoming earnings report will either be a massive disappointment leading to a sell-off, or it will announce a revolutionary new model causing the stock to soar. You don't know which.

You execute a long straddle:
1. You buy a Call option with a strike price of $200, expiring in 3 months. Let's say the premium is $15 ($1,500 total).
2. You buy a Put option with a strike price of $200, expiring in 3 months. Let's say the premium is also $15 ($1,500 total).

Your total cost (and maximum possible loss) is $30 per share, or $3,000 total. 

Because you paid a combined premium of $30, you need the stock to move more than $30 in either direction just to break even at expiration. This means you only start making a profit if DontBeEvil rises above $230 (the upper breakeven point) or falls below $170 (the lower breakeven point).

#### The Secret of Early Exits

You might be thinking: *expecting a 15% growth or drop in 3 months is a lot just to break even. Isn't this too much to bet $3,000?*

Here is the secret of trading options: you almost never hold them until expiration. The $3,000 is your maximum possible loss if you hold until the very last day and the stock stays exactly flat. However, if DontBeEvil jumps 8% in the first two weeks due to a leaked memo, the value of your Call option will spike significantly due to the sudden price movement and increased implied volatility. 

You can sell the straddle early, closing both the Call and the Put positions, for a profit long before hitting that mathematical "breakeven at expiration" mark. You are trading the momentum, not just the final destination.

#### The Outcomes

Here is what happens in the different scenarios:

**Scenario A: The market does nothing.** DontBeEvil stays exactly at $200, or anywhere between $170 and $230. Both your Call and Put will expire either worthless or without enough intrinsic value to cover your initial cost. In the worst-case scenario (it stays exactly at $200 until expiration), you lose your entire $3,000 premium. This is the danger of the straddle. Time decay (theta) is your enemy. You need significant movement, and you need it before expiration.

**Scenario B: The bubble bursts.** The company announces they are pivoting back to selling physical servers. The stock crashes to $140. 
- Your Call option is worthless.
- Your Put option is now deep in the money. You have the right to sell at $200 something currently worth $140. The intrinsic value is $60 per share ($6,000 total). 
- Subtracting your initial $3,000 investment, your net profit is $3,000.

**Scenario C: The rocket takes off.** They announce a model that writes flawless code. The stock jumps to $260.
- Your Put option is worthless.
- Your Call option is deep in the money. You have the right to buy at $200 something currently worth $260. The intrinsic value is $60 per share ($6,000 total).
- Subtracting your initial $3,000 investment, your net profit is $3,000.

### A philosophy of volatility

Notice the beauty here. In both extreme scenarios, you won. The only scenario where you lose is the one where the world remains boring and predictable. 

As I mentioned in my article about the Barbell portfolio, this strategy requires a specific mindset. It is not for your entire nest egg. It belongs in the "risky" 10% of your barbell. It requires patience and the psychological fortitude to watch your options slowly bleed value (due to time decay) while waiting for the volatility event to occur. 

You are essentially buying insurance against stability. When the market is calm, you pay your premiums. When the market panics or euphoriates, you collect the payout. In an era where technological paradigms shift overnight and financial markets behave irrationally, embracing uncertainty might just be the most rational choice you can make. 

I write my thoughts about Software Engineering and life in general on my [Mastodon account](https://kotlin.social/@eenriquelopez). If you have liked this article or if it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.