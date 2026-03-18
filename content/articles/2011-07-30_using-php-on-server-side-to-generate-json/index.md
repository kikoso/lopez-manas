---
date: '2011-07-30T11:54:15+00:00'
draft: false
slug: using-php-on-server-side-to-generate-json
title: Using PHP on server side to generate JSON
---

Recently, I publish one <a href="goo.gl/DPsAL" title="DefCon - Android Market" target="_blank">application</a> into the Android Market that tries to predict when Spain will default. The application uses the data provided by my colleague Juan Carlos Barba from his <a href="jcbcarc.dyndns.org/Defcon.php" target="_blank">server</a>. There are basically a set of levels pointing out the seriousness of the Spanish level of <a href="http://en.wikipedia.org/wiki/Credit_default_swap" title="CDS" target="_blank">CDS</a> and <a href="http://en.wikipedia.org/wiki/Credit_default_swap" title="spread" target="_blank">Spread </a>of the debt. The model establishes 5 different levels of alert (or how he called them, DefCon). My implementation customized the data to visualize into the Android Platform.

Firstly, I needed to access his database into the server, which was a slow task due to the nature of the server (a personal computer with a normal DSL connection). My idea was to rely this task into something that could avoid overloading the server, and then I thought about everything that happens now with all the client / server application. Why not using a PHP file to generate JSON with the information I needed?

Since I do not have access to Juan Carlos'' server, I decided to do it on my own server. I created some PHP files that query the server, and give me the information in JSON format

<pre lang="php"> 
<?php
mysql_connect("jcbcarc.dyndns.org","user","password");
mysql_select_db("economia");
 
$q=mysql_query("SELECT * , DATE(FechayHora) AS fecha FROM economia.spreads GROUP BY fecha ORDER BY fecha;");
while($e=mysql_fetch_assoc($q))
        $output[]=$e;
 
print(json_encode($output));
 
mysql_close();
?>
</pre>

Now the data has to be requested and handled from the Android side:
<pre lang="java"> 
private void initPHP() {
		//http post
		 String result = "";
		  InputStream is = null ;
		 try{
			 DefaultHttpClient httpclient = new DefaultHttpClient();
		         HttpPost httppost = new HttpPost("/defcon/cds.php5");
		         HttpResponse response = httpclient.execute(httppost);
		         HttpEntity entity = response.getEntity();
		         is = entity.getContent();
		 } catch(Exception e) {
		         Log.e("log_tag", "Error in http connection "+e.toString());
		 }
		 //convert response to string
		 try{
		         BufferedReader reader = new BufferedReader(new InputStreamReader(is,"iso-8859-1"),8);
		         StringBuilder sb = new StringBuilder();
		         String line = null;
		         while ((line = reader.readLine()) != null) {
		                 sb.append(line + "\
");
		         }
		         is.close();
		  
		         result=sb.toString();
		 }catch(Exception e){
		         Log.e("log_tag", "Error converting result "+e.toString());
		 }
		  
		 //parse json data
		 try{
		         JSONArray jArray = new JSONArray(result);
		         int lastDay = 0;
		         for(int i=0;i<jArray.length();i++){
		        	 JSONObject json_data = jArray.getJSONObject(i);
		        	 DateFormat df = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
		        	 Date day = null;
		        	 try {
		        		 day = df.parse(json_data.getString("FechayHora"));
		        	 } catch (ParseException e) {
		        		 e.printStackTrace();
		        	 }
		            if (i == 0) 
		            	lastDay = day.getDay();
		            if (day.getDay() != lastDay) {
		            	mEntity.getCdsData().add(new CDS(json_data.getInt("Secuencial"),day,json_data.getString("Pais"),json_data.getDouble("CDS")));
		            	lastDay = day.getDay();
		            }
		         }
		 } catch(JSONException e){
		         Log.e("log_tag", "Error parsing data "+e.toString());
		 }
	 }
</pre>

The code can be improved to handle authentication, HTTPS, or do more complex work in general. In a project at work we used authentication based on a pair of generated keys, but a simple method based on a known keyword is enough.