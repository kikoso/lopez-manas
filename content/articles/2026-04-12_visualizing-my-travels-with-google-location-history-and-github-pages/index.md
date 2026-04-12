---
title: "Visualizing My Travels: A Small App for Google Location History"
author: "Enrique López-Mañas"
date: 2026-04-12T15:00:00.000Z

description: "Building a local-first, privacy-conscious visualizer for Google Timeline data using GitHub Pages."

image: "/articles/2026-04-12_visualizing-my-travels-with-google-location-history-and-github-pages/image1.jpeg"
images:
  - "/articles/2026-04-12_visualizing-my-travels-with-google-location-history-and-github-pages/image1.jpeg"

---

For many of us, our digital footprint is scattered across various services, but perhaps none is more personal than our location history. Google Maps has been tracking our every move for years, and while the "Timeline" feature in the app is useful, it often feels like a walled garden. I recently wanted to see a more high-level summary of my travels, specifically how many days I have spent in different countries over the last decade.

Instead of looking for a third-party service that would require me to upload my sensitive data to their servers, I decided to build a small local-first application. The goal was simple: a website where I can drag and drop my location-history.json file and get an immediate visualization without any data leaving my browser. This is what I call a "privacy-first" approach to personal data analysis.

The architecture of the app is intentionally minimal. It is a single-page application hosted on GitHub Pages, utilizing Leaflet.js for mapping and Tailwind CSS for a modern interface. The heavy lifting happens in the browser using the File API to read the JSON export from Google Takeout. I implemented a point-in-polygon algorithm to match coordinates to country boundaries, allowing the app to generate a choropleth map where countries are color-coded based on the duration of my stay.

One of the most interesting parts of this project was dealing with the raw data format. Google provides a massive JSON file containing every "visit" and "timeline path" recorded by your phone. Parsing this efficiently in JavaScript without freezing the UI required some careful handling of the data loop. The result is a dashboard that provides a ranked table of countries, total days spent, and even a breakdown by years.

I found out, for instance, that I have spent over six years in Germany and nearly two years in Vietnam. Seeing these numbers visualized on a world map provides a different perspective on my own life trajectory. It is a reminder that as developers, we have the power to build tools that help us understand ourselves better without compromising our privacy.

The application is now live on GitHub and I have made the source code public. It serves as a template for how we can build useful utilities that respect user data by keeping all processing on the client side. If you have your location history ready, you can simply drop it in and see your own world map bloom into view.

I wrote this small tool in a few hours, but the insights it provides are lasting. It is a small reminder that sometimes the most useful software is the one that solves a personal curiosity in the simplest way possible. You can find the repository on my GitHub profile if you want to experiment with it.

I write my thoughts about Software Engineering and life in general on my Mastodon account. If you have liked this article or if it did help you, feel free to share it and leave a comment. This is the currency that fuels amateur writers.
