---
title: "Teaching My Mac mini to Call the Plumber"
author: "Enrique López-Mañas"
date: 2026-11-06T12:00:00.000Z

description: "How Pipecat, MLX Whisper, a local Gemma model in LM Studio and Piper turned into a voice agent that can hold a phone conversation, running entirely on a Mac mini."

subtitle: "Some companies in Germany still only talk to you over the phone. So I asked my Mac mini to do the talking."

image: "/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/2.png"
images:
 - "/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/2.png"
 - "/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/0.png"
 - "/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/1.png"
 - "/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/3.png"

---

A few weeks ago, on a Friday morning, I was looking for someone who could install a Japanese toilet in our flat in Munich. In Germany they are called Dusch-WC, and fitting one in a rented flat is not trivial: the cistern is hidden in the wall, and mine has no water connection prepared for it. I was working with Claude, so I asked it to find plumbers in the city and email them asking whether they do this kind of installation.

It found a good list and wrote to all of them. But five of the companies only had a phone number on their website. No email, no contact form, nothing. This is still very common in Germany, specially among small Handwerker businesses, and it is exactly the kind of task I tend to postpone for weeks.

#### A phone call I could not make

So I asked the obvious question: could you call them? The answer was no. Claude can not place phone calls, but it offered to build a service that could. I told it to build it locally, with a Gemma model running in LM Studio on the Mac mini at home, the same machine that already runs my [Local AI Bridge](/articles/2026-04-09_bridging-the-gap-local-ai-meets-telegram-cli/) and my [food log](/articles/2026-10-24_logging-what-i-eat-with-immich-a-local-vision-model-and-a-telegram-bot/).

The same morning I had a prototype: an application that listens through the microphone, converts the voice to text, passes the text to the local model and synthesises the answer back as speech. A voice agent that can hold a conversation, without any cloud service involved. Is not connected to a phone line yet, but it already behaves like a caller, and that is what this article is about.

#### The pipeline

The agent is built on [Pipecat](https://github.com/pipecat-ai/pipecat), an open source Python framework for voice agents. Pipecat thinks in pipelines: frames of audio and text flow from one service to the next, and every piece can be replaced by another one. Mine looks like this:

1. **Silero VAD** detects when the other person has stopped talking, so the agent knows when it is its turn.
2. **MLX Whisper** (large-v3-turbo) transcribes the audio. MLX is Apple's machine learning framework, so the transcription runs natively on Apple Silicon.
3. **LM Studio** serves the language model through its OpenAI-compatible API. I used Gemma 4 26B-A4B, a mixture of experts model that only activates around 4 billion parameters per token: fast enough to answer, and with a decent German.
4. **Piper** converts the answer back to speech, with the German voice `thorsten-high`.

![image](/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/0.png#layoutTextWidth)

_The whole pipeline. Only the prompt and the voice change between languages, and only the transport will change for real calls._

For this first phase there is no phone line at all. Pipecat comes with a small web client that connects over WebRTC, so I open a page, click Connect and talk to the agent from the browser. To try it from another computer or from a phone I added a Cloudflare tunnel, since browsers only give access to the microphone on localhost or over HTTPS.

The nice part of this design is that the second phase only changes the transport. The same pipeline can receive the audio from a telephony provider instead of a browser.

#### Teaching it how to behave on the phone

The most interesting file in the repository is not the code, but the prompt. It is written in German, and it describes the call as if I was briefing an assistant: Herr López Mañas rents a flat in Munich, he wants to retrofit a Dusch-WC, his concealed cistern is a Geberit with a specific article number, and he would like to avoid replacing it. The agent has to find out four things: whether the company does this kind of installation, whether it works without changing the cistern, what is needed for the power supply, and roughly how much it costs and when there could be an appointment.

A few rules turned out to be important:

- **Wait for the other side.** On a real call the company picks up and says its name first, so the agent stays silent until somebody speaks.
- **Say that it is an AI.** The first sentence makes clear that it is an AI assistant calling on my behalf. Apart from being honest, the EU AI Act asks for this kind of transparency when a person talks to a machine.
- **One question at a time, one or two sentences per answer.** Long answers are painful when they are read aloud.
- **No lists, no symbols, no emojis.** Everything the model writes ends up in the speaker.
- **Never invent, never commit.** If it does not know something, it says that I will get back to them. It takes note of proposed appointments, but it never confirms one.

The audio is not recorded. When the call ends, only the text transcript is saved locally, which is enough for what I need.

#### Making it talk

The first version did not say a single word. The logs showed that Whisper understood me perfectly ("Hallo, grüß Gott"), but the replies of the model were empty. The reason was hidden in the token counts: Gemma 4 can reason before answering, and it spent 197 of the 200 tokens I allowed on thinking. There was nothing left to speak.

![image](/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/1.png#layoutTextWidth)

_197 tokens of thinking, 3 tokens left for the answer. A reasoning model with a small limit is a very quiet caller._

The fix was to disable thinking through the chat template (`enable_thinking: false`, which LM Studio passes to the model) and to raise the limit to 1024 tokens. In a phone call this matters twice, because a model that thinks for a few seconds means a few seconds of silence on the line.

Two more problems appeared during the morning, both of them small and annoying:

- **IPv6.** The Cloudflare tunnel was pointing at `localhost`, which `cloudflared` resolved to the IPv6 address `[::1]`, while the bot was only listening on IPv4. Changing it to `127.0.0.1` solved it.
- **Configuration overwritten.** I added language profiles, so `PROFILE=vi ./run.sh` switches the Whisper language, the voice and the prompt together. The agent kept answering in German anyway, because the Pipecat runner reloads the `.env` file with override enabled after the bot module is imported. Applying the profile when each session starts, once the runner is done, fixed it.

None of these problems were related with voice or language models. As usual, most of the time went into the plumbing, which is quite fitting for a project about plumbers.

#### Testing it in Vietnamese

Once it worked in German, I asked for a Vietnamese version, so my wife could test it in her own language. The prompt was translated, Whisper switched to Vietnamese and Piper got the voice `vi_VN-vais1000-medium`, which sounds noticeably more robotic than the German one.

My wife played the plumber. She answered the "phone", and the agent introduced itself: an AI calling on behalf of Enrique López-Mañas, who would like to ask about prices for an installation. She kept answering, it kept asking one question at a time, and the conversation went on as if she was talking to a polite and slightly slow assistant. In the end she played a tough plumber: they can only give a price after checking on site and asking their technical department. The agent took note, said that I would get back to them, thanked her and said goodbye, exactly as the prompt asks.

![image](/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/2.png#layoutTextWidth)

_The end of the Vietnamese test in the Pipecat Playground. The agent called her "anh", the form for a man, during the whole conversation, and her last line (which Whisper transcribed a little bit garbled) ends with "không phải anh": not "anh"._

Slightly slow is the honest description. On the local model there were around 15 seconds between sentences, and according to the timestamps of the playground a complete reply took between 30 and 35 seconds. That is fine for a demo, but no plumber will wait half a minute on the line.

![image](/articles/2026-11-06_teaching-my-mac-mini-to-call-the-plumber/images/3.png#layoutTextWidth)

_Time between her message and the complete reply of the agent, from the timestamps of the transcript above._

 It reminded me of the Duplex demo that Google showed in 2018, where an assistant booked an appointment at a hair salon over the phone. The difference is that this one runs on a Mac mini at home and took a morning to put together.

#### A few lessons

- **Thinking models and voice do not mix well.** Every token of reasoning is silence on the line. For a voice agent I would rather choose a smaller and faster model without reasoning than a bigger and smarter one.
- **Latency is the real product.** Under a second and a half a conversation feels natural, at fifteen seconds it is a curiosity. Smaller models (7B to 14B, 4 bit) and the quantised Whisper turbo are the obvious next steps.
- **Write the prompt for the ear.** It is worth to treat the prompt like a script that will be read aloud: short sentences, no formatting, one question at a time.
- **Prototyping became cheap.** The idea and the first working conversation happened on the same morning, and most of that time went into the three bugs above.

The roadmap has two more phases. The second one is connecting a real phone line, through a provider like Twilio or Telnyx over websockets or a SIP account with sipgate, so the agent can place outbound calls. The third one is summarising each transcript and emailing me the result: which companies do the installation, how much it would cost and when they could come. For now, the agent lives in a private repository and only talks to my family.

If you have liked this article or if it did help you, feel free to share, 👏 it and/or leave a comment. This is the currency that fuels amateur writers.
