---
date: '2011-10-09T21:04:36+00:00'
draft: false
slug: cvblob-library-for-android
title: cvBlob library for Android
---

I recently moved to Barcelona to start working in here. Although I''m not working in any computer-vision based project, I still keep a high interest in this field, trying to conduct as many personal projects as possible. My work team is highly motivated and full of professionals, and we all keep our personal projects besides our work.

Recently I met <a title="Fegabe" href="https://plus.google.com/115987041616851932912/posts" target="_blank">Fegabe</a> in Barcelona, who''s a member of the <a title="Barcelona gtug" href="http://barcelona.gtugs.org/" target="_blank">GTUG Barcelona</a> core team and an Android Developer. We decided to start together a Sudoku Solver for Android. Although there are already many of them published in the Market, we just wanted to do it for fun and to get a bit deeper into computer vision and pattern recognition. There is an <a title="OpenCV for Android" href="http://opencv.willowgarage.com/wiki/Android" target="_blank">OpenCV port</a> for Android, but we decided to keep our implementation pure Java.

The following steps are applied in order to capture, detect and solve the Sudoku:

-The user must take a picture of the Sudoku using the camera of the device.

-After the picture is taken, a <a title="Thresholding" href="http://en.wikipedia.org/wiki/Thresholding_(image_processing)" target="_blank">Threshold</a> is applied to the image, so we can get a black and white version. Of course, there is some preprocessing involved. Things like smoothing out noise, some morphological operations, etc.

-When the picture has been taken, we apply a <a title="Blob detection" href="http://en.wikipedia.org/wiki/Blob_detection" target="_blank">blob detection</a> in order to detect the biggest segment of the image. We work under the assumption that this segment will be the outer line of the Sudoku table.

-Afterwards, we can use the <a href="http://www.aishack.in/2010/03/the-hough-transform/">Hough transform</a> to get lines in the image. It returns lines in mathematical terms. So after this step, we’ll know exactly where a lines lies… and not just the pixels where it lies.

-When the lines has been detected, it will be easier to locate each individual cell. The number inside will be recognized using a <a title="Neural Network" href="http://en.wikipedia.org/wiki/Neural_network" target="_blank">neural network</a>.

-The last step is the easiest: we just solve the sudoku by using any of all the <a title="Sudoku algorithms" href="http://en.wikipedia.org/wiki/Sudoku_algorithms" target="_blank">known algorithms</a>
<div>The Sudoku Solver is still to be finished, but the cvBlob library is working fine, so I decided to publish it. The implementation is based on Dr. <a title="Andrew Greensted" href="http://www.elec.york.ac.uk/staff/ajg112.html" target="_blank">Andrew Greensted</a> suggestion for <a title="Blob Detection" href="http://www.labbookpages.co.uk/software/imgProc/blobDetection.html" target="_blank">Blob Detection</a>.</div>
I shared the project with a GPL license in <a href="http://code.google.com/p/cvblob-for-android/" target="_blank">Google Code</a>. All the technical information can be found there, besides the source code and a binary file for Android. If you wanna try out, I would highly appreciate any feedback

&nbsp;

<img src="/images/cvBlobDetection.png" alt="blob detection" width="255" />

&nbsp;