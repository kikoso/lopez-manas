---
date: '2012-01-06T21:46:28+00:00'
draft: false
slug: push-client-android-based-and-server
title: 'Push: Client (Android based) and server'
---

As part of the training and pushing the boundaries in my department, we recently experimented with Push technologies and their application to mobile development. Whereas iPhone seems to support natively push messaging, we soon realize that Android was not perfect in this direction. Surprisingly they haven''t yet considered that a native push support is a technology worth to embedded within their <a href="http://developer.android.com/index.html" target="_blank">official SDK</a>, and this is a completely setback for developers aiming to develop and create their own ideas.

&nbsp;

Let''s explain this is in shortly: push is the name given to the fact that messages can be sent to the receiver, instead of being requested from the client. Although the concept might sounds easy to understand, the explanation on why the implementation is hard is a bit more complex: we can summarize it by saying that the protocol running under the modern Internet communications (TCP/IP) was not designed for Push technologies. For more information on this topic, we recommend to read the <a href="http://www.onsip.com/blog/mike/2010/07/07/the-dangers-of-push-notification-in-mobile-sip-applications" target="_blank">following article</a>.

&nbsp;

So there are three general solutions widely accepted to implement our own Push notifications:
<ul>
	<li><a href="http://code.google.com/intl/de-DE/android/c2dm/" target="_blank">Google C2DM</a>: recently released by Google,</li>
	<li>Poll: although it is not a real push request, the effect looks the same: we periodically poll the server looking for new data. The more often we poll the closer we get to the real-time push. But obviously, it will never be on real-time. Plus the battery will die very quickly</li>
	<li>Persistent TCP/IP connection: the device initiates a long-lived mostly idle TCP/IP connection by playing with the feature of "keep-alive" (sending occasionally messages to the devices). Whenever something new is on the server, the phone initiates a fully TCP connection to acquire the new data. This is the underlying technology for Google C2DM, but you might want to have full control on the entire process until C2DM provides a reliable service.</li>
</ul>
&nbsp;
<div>The Google C2DM API is well described on the official service, but we might need to know a bit more about how to set up the server part. In short, we will need three parts: the C2DM server itself, a client implementation of Push (i.e., in your Android device) and a third party application service. This last component might be a bit tricky to understand, but a short summary of the functionalities performed are:</div>
&nbsp;
<div>
<ul>
	<li>Is able to communicate with the client.</li>
	<li>Will fire HTTP requests to the C2DM server.</li>
	<li>Handle requests algorithm (for instance, we could design it for performing an exponential back off).</li>
	<li>Storages the authentication tokens. They are need to handle applications with a little bit of complexity</li>
</ul>
&nbsp;
<div>As stated before, is easy to set up all the parts, but we might spend more time thinking about the third party server implementation. And that''s the sugar of this article.</div>
&nbsp;
<div>According to the source site of C2DM, the implementation of the Android is quite trivial. We first need to declare in our Manifest the required permissions for the application, which are com.google.android.c2dm.permission.RECEIVE, com.example.myapp.permission.C2D_MESSAGE and of course android.permission.INTERNET.  We also need to declare our receivers. For further information, check out the <a title="Android Manifest for C2DM" href="http://code.google.com/intl/de-DE/android/c2dm/#manifest">official link</a>.</div>
<div>The next step is to register on our application, what can be done with the following code. Typically, we will add it into an onCreate method, or when the application needs to prepare itself for the push.</div>
&nbsp;
<pre lang="java">Intent registrationIntent = new Intent("com.google.android.c2dm.intent.REGISTER");
registrationIntent.putExtra("app", PendingIntent.getBroadcast(this, 0, new Intent(), 0)); // boilerplate
registrationIntent.putExtra("sender", emailOfSender);
startService(registrationIntent);</pre>
&nbsp;
Unregistering is also trivial (again, we might want to add this into the onDestroy event):
&nbsp;
<pre lang="java">
Intent unregIntent = new Intent("com.google.android.c2dm.intent.UNREGISTER");
unregIntent.putExtra("app", PendingIntent.getBroadcast(this, 0, new Intent(), 0));
startService(unregIntent);</pre>
&nbsp;
The basic part for handling the message needs a bit more of explanation. When the method onReceive of our BroadcastReceiver is triggered, we might need to check if we are dealing with the registration or if we are just receiving a push notification. We provide the code for the first case. For the second one, we might need to create our own method based on our design. We will be able to receive a message through the Intent. And that''s the part we need to handle on the server side.
&nbsp;
<pre lang="java">public void onReceive(Context context, Intent intent) {
   if (intent.getAction().equals("com.google.android.c2dm.intent.REGISTRATION")) {
      handleRegistration(context, intent);
   } else if (intent.getAction().equals("com.google.android.c2dm.intent.RECEIVE")) {
      handleMessage(context, intent);
   }
}

private void handleRegistration(Context context, Intent intent) {
   String registration = intent.getStringExtra("registration_id");
   if (intent.getStringExtra("error") != null) {
      // Registration failed, should try again later.
   } else if (intent.getStringExtra("unregistered") != null) {
      // unregistration done, new messages from the authorized sender will be rejected
   } else if (registration != null) {
      // Send the registration ID to the 3rd party site that is sending the messages.
      // This should be done in a separate thread.
      // When done, remember that all registration is done.
   }
}
</pre>
&nbsp;

So this is the core of the server application. This method needs to receive an auth code, and the device registration ID. The device registration ID will be provided when our phone is registered in the previous step. The authcode is the authentication through a Google account. For instance, we could create a dummy account, and send it along with the push notification:

&nbsp;
<pre lang="php">googleAuthenticate("mydummyaccount@gmail.com","mydummypassword")</pre>
&nbsp;

Afterwards, we can send a message type and the content itself. This allows us to have more flexibility in our notifications. For instance, we might provide a message type which corresponds with an error, and on the content we can send the complete error text.
&nbsp;
<pre lang="php">function sendMessageToPhone($authCode, $deviceRegistrationId, $msgType, $messageText) {
    $headers = array(''Authorization: GoogleLogin auth='' . $authCode);
    $data = array(
      ''registration_id'' =&gt; $deviceRegistrationId,
      ''collapse_key'' =&gt; $msgType,
      ''data.message'' =&gt; $messageText //TODO Add more params with just simple data instead
   );

   $ch = curl_init();

   curl_setopt($ch, CURLOPT_URL, "https://android.apis.google.com/c2dm/send");
   if ($headers)
      curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
      curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
      curl_setopt($ch, CURLOPT_POST, true);
      curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

      $response = curl_exec($ch);

      curl_close($ch);

      return $response;
   }

function googleAuthenticate($username, $password, $source="Company-AppName-Version", $service="ac2dm") {

   if( isset($_SESSION[''google_auth_id'']) &amp;&amp; $_SESSION[''google_auth_id''] != null) {
   return $_SESSION[''google_auth_id''];
}

// get an authorization token
$ch = curl_init();
if(!ch){
   return false;
}

curl_setopt($ch, CURLOPT_URL, "https://www.google.com/accounts/ClientLogin");
$post_fields = "accountType=" . urlencode(''HOSTED_OR_GOOGLE'')

. "&amp;Email=" . urlencode($username)
. "&amp;Passwd=" . urlencode($password)
. "&amp;source=" . urlencode($source)
. "&amp;service=" . urlencode($service);
curl_setopt($ch, CURLOPT_HEADER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post_fields);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

// for debugging the request
//curl_setopt($ch, CURLINFO_HEADER_OUT, true); // for debugging the request

$response = curl_exec($ch);

//var_dump(curl_getinfo($ch)); //for debugging the request
//var_dump($response);

//var_dump(curl_getinfo($ch)); //for debugging the request
//var_dump($response);

curl_close($ch);
if (strpos($response, ''200 OK'') === false) {
   return false;
}

// find the auth code
preg_match("/(Auth=)([\\w|-]+)/", $response, $matches);

if (!$matches[2]) {
   return false;
}
$_SESSION[''google_auth_id''] = $matches[2];

return $matches[2];
}</pre>
&nbsp;

I hope you enjoyed the tutorial. For any further questions or inquiries, you can drop me a line into my personal <a href="mailto:eenriquelopez@gmail.com" target="_blank">email</a>.

&nbsp;

Enrique López-Mañas