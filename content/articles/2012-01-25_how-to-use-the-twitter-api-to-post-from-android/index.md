---
date: '2012-01-25T18:04:27+00:00'
draft: false
slug: how-to-use-the-twitter-api-to-post-from-android
title: How to use the Twitter API to post from Android
---

Posting from Android into Twitter is one of the earliest stages of an Android developer. To keep full control over the posting process, we will use prefer primarily a pure OAuth post instead of dealing with Intents, so we can keep full control. So as a user, we could just think and conclude: the most typical way to authenticate is to pop up a window where we can identify with our user and password to give the application access to our account (not the full account though, just to post from the application!) and forget about the rest of the process. This might be a bit tricky process for newbies in Android. And of course, Twitter will eventually change their API or registration method, so we will found sometimes that our old implementation is not working anymore

We first need to register a Twitter App. For that purpose, we will visit the <a href="https://dev.twitter.com/" target="_blank">developer website</a> of Twitter. After login in, we will add a <a href="https://dev.twitter.com/apps" target="_blank">new application</a>. There are no special settings to be remembered, but the part of the callback URL has changed very oftenly since Twitter released their API. At the moment, if we are developing one application we only need to provide any random URL.

We need three main classes in our application to make it work.

First, TwitterApp. This will be the controller for the API:


<pre lang="java">

import java.net.MalformedURLException;
import java.net.URLDecoder;

import oauth.signpost.OAuth;
import oauth.signpost.OAuthProvider;
import oauth.signpost.basic.DefaultOAuthProvider;
import oauth.signpost.commonshttp.CommonsHttpOAuthConsumer;
import oauth.signpost.commonshttp.CommonsHttpOAuthProvider;

import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.User;

import android.os.Handler;
import android.os.Message;

import android.app.ProgressDialog;
import android.content.Context;
import android.util.Log;
import android.view.Window;

import java.net.URL;

public class TwitterApp {
	private Twitter mTwitter;
	private TwitterSession mSession;
	private twitter4j.auth.AccessToken mAccessToken;
	private CommonsHttpOAuthConsumer mHttpOauthConsumer;
	private OAuthProvider mHttpOauthprovider;
	private String mConsumerKey;
	private String mSecretKey;
	private ProgressDialog mProgressDlg;
	private TwDialogListener mListener;
	private Context context;
	
	public static final String CALLBACK_URL = "twitterapp://connect";
	private static final String TAG = "TwitterApp";
	
	public TwitterApp(Context context, String consumerKey, String secretKey) {
		this.context	= context;
		
		mTwitter 		= new TwitterFactory().getInstance();
		mSession		= new TwitterSession(context);
		mProgressDlg	= new ProgressDialog(context);
		
		mProgressDlg.requestWindowFeature(Window.FEATURE_NO_TITLE);
		
		mConsumerKey 	= consumerKey;
		mSecretKey	 	= secretKey;
	
		mHttpOauthConsumer = new CommonsHttpOAuthConsumer(mConsumerKey, mSecretKey);
		mHttpOauthprovider = new CommonsHttpOAuthProvider("https://api.twitter.com/oauth/request_token",
				 					"https://api.twitter.com/oauth/access_token",
				 					"https://api.twitter.com/oauth/authorize");
		mHttpOauthprovider.setOAuth10a(true);
		mAccessToken	= mSession.getAccessToken();
		
		configureToken();
	}
	
	public void setListener(TwDialogListener listener) {
		mListener = listener;
	}
	
	@SuppressWarnings("deprecation")
	private void configureToken() {
		if (mAccessToken != null) {
			mTwitter.setOAuthConsumer(mConsumerKey, mSecretKey);
			
			mTwitter.setOAuthAccessToken(mAccessToken);
		}
	}
	
	public boolean hasAccessToken() {
		
		return (mAccessToken == null) ? false : true;
	}
	
	public void resetAccessToken() {
		if (mAccessToken != null) {
			mSession.resetAccessToken();
		
			mAccessToken = null;
		}
	}
	
	public String getUsername() {
		return mSession.getUsername();
	}
	
	public void updateStatus(String status) throws Exception {
		try {
			mTwitter.updateStatus(status);
		} catch (TwitterException e) {
			throw e;
		}
	}
	
	public void authorize() {
		mProgressDlg.setMessage("Initializing ...");
		mProgressDlg.show();
		
		new Thread() {
			@Override
			public void run() {
				String authUrl = "";
				int what = 1;
				
				try {
					authUrl = mHttpOauthprovider.retrieveRequestToken(mHttpOauthConsumer, CALLBACK_URL);	
					
					what = 0;
					
					Log.d(TAG, "Request token url " + authUrl);
				} catch (Exception e) {
					Log.d(TAG, "Failed to get request token");
					
					e.printStackTrace();
				}
				
				mHandler.sendMessage(mHandler.obtainMessage(what, 1, 0, authUrl));
			}
		}.start();
	}
	
	public void processToken(String callbackUrl)  {
		mProgressDlg.setMessage("Finalizing ...");
		mProgressDlg.show();
		
		final String verifier = getVerifier(callbackUrl);

		new Thread() {
			@Override
			public void run() {
				int what = 1;
				
				try {
					mHttpOauthprovider.retrieveAccessToken(mHttpOauthConsumer, verifier);
		
					mAccessToken = new twitter4j.auth.AccessToken(mHttpOauthConsumer.getToken(), mHttpOauthConsumer.getTokenSecret());
				
					configureToken();
				
					User user = mTwitter.verifyCredentials();
				
			        mSession.storeAccessToken(mAccessToken, user.getName());
			        
			        what = 0;
				} catch (Exception e){
					Log.d(TAG, "Error getting access token");
					
					e.printStackTrace();
				}
				
				mHandler.sendMessage(mHandler.obtainMessage(what, 2, 0));
			}
		}.start();
	}
	
	private String getVerifier(String callbackUrl) {
		String verifier	 = "";
		
		try {
			callbackUrl = callbackUrl.replace("twitterapp", "http");
			
			URL url 		= new URL(callbackUrl);
			String query 	= url.getQuery();
		
			String array[]	= query.split("&");

			for (String parameter : array) {
	             String v[] = parameter.split("=");
	             
	             if (URLDecoder.decode(v[0]).equals(oauth.signpost.OAuth.OAUTH_VERIFIER)) {
	            	 verifier = URLDecoder.decode(v[1]);
	            	 break;
	             }
	        }
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
		
		return verifier;
	}
	
	private void showLoginDialog(String url) {
		final TwDialogListener listener = new TwDialogListener() {
			@Override
			public void onComplete(String value) {
				processToken(value);
			}
			
			@Override
			public void onError(String value) {
				mListener.onError("Failed opening authorization page");
			}
		};
		
		new TwitterDialog(context, url, listener).show();
	}
	
	private Handler mHandler = new Handler() {
		@Override
		public void handleMessage(Message msg) {
			mProgressDlg.dismiss();
			
			if (msg.what == 1) {
				if (msg.arg1 == 1)
					mListener.onError("Error getting request token");
				else
					mListener.onError("Error getting access token");
			} else {
				if (msg.arg1 == 1)
					showLoginDialog((String) msg.obj);
				else
					mListener.onComplete("");
			}
		}
	};
	
	public interface TwDialogListener {
		public void onComplete(String value);		
		
		public void onError(String value);
	}
}
</pre>

The TwitterDialog class is composed by a basic WebView which loads the URL with the authentication fields:

<pre lang="java">

import android.app.Dialog;
import android.app.ProgressDialog;

import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;

import android.os.Bundle;
import android.util.Log;
import android.content.Context;

import android.view.Display;
import android.view.ViewGroup;
import android.view.Window;

import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;


public class TwitterDialog extends Dialog {

    static final float[] DIMENSIONS_LANDSCAPE = {460, 260};
    static final float[] DIMENSIONS_PORTRAIT = {280, 420};
    static final FrameLayout.LayoutParams FILL = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.FILL_PARENT,
                         						ViewGroup.LayoutParams.FILL_PARENT);
    static final int MARGIN = 4;
    static final int PADDING = 2;

    private String mUrl;
    private TwDialogListener mListener;
    private ProgressDialog mSpinner;
    private WebView mWebView;
    private LinearLayout mContent;
    private TextView mTitle;

    private static final String TAG = "Twitter-WebView";
    
    public TwitterDialog(Context context, String url, TwDialogListener listener) {
        super(context);
        
        mUrl 		= url;
        mListener 	= listener;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mSpinner = new ProgressDialog(getContext());
        
        mSpinner.requestWindowFeature(Window.FEATURE_NO_TITLE);
        mSpinner.setMessage("Loading...");

        mContent = new LinearLayout(getContext());
        
        mContent.setOrientation(LinearLayout.VERTICAL);
        
        setUpTitle();
        setUpWebView();
        
        Display display 	= getWindow().getWindowManager().getDefaultDisplay();
        final float scale 	= getContext().getResources().getDisplayMetrics().density;
        float[] dimensions 	= (display.getWidth() < display.getHeight()) ? DIMENSIONS_PORTRAIT : DIMENSIONS_LANDSCAPE;
        
        addContentView(mContent, new FrameLayout.LayoutParams((int) (dimensions[0] * scale + 0.5f),
        							(int) (dimensions[1] * scale + 0.5f)));
    }

    private void setUpTitle() {
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        
        Drawable icon = getContext().getResources().getDrawable(R.drawable.twitter_icon);
        
        mTitle = new TextView(getContext());
        
        mTitle.setText("Twitter");
        mTitle.setTextColor(Color.WHITE);
        mTitle.setTypeface(Typeface.DEFAULT_BOLD);
        mTitle.setBackgroundColor(0xFFbbd7e9);
        mTitle.setPadding(MARGIN + PADDING, MARGIN, MARGIN, MARGIN);
        mTitle.setCompoundDrawablePadding(MARGIN + PADDING);
        mTitle.setCompoundDrawablesWithIntrinsicBounds(icon, null, null, null);
        
        mContent.addView(mTitle);
    }

    private void setUpWebView() {
        mWebView = new WebView(getContext());
        
        mWebView.setVerticalScrollBarEnabled(false);
        mWebView.setHorizontalScrollBarEnabled(false);
        mWebView.setWebViewClient(new TwitterWebViewClient());
        mWebView.getSettings().setJavaScriptEnabled(true);
        mWebView.loadUrl(mUrl);
        mWebView.setLayoutParams(FILL);
        
        mContent.addView(mWebView);
    }

    private class TwitterWebViewClient extends WebViewClient {

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
        	Log.d(TAG, "Redirecting URL " + url);
        	
        	if (url.startsWith(TwitterApp.CALLBACK_URL)) {
        		mListener.onComplete(url);
        		
        		TwitterDialog.this.dismiss();
        		
        		return true;
        	}  else if (url.startsWith("authorize")) {
        		return false;
        	}
        	
            return true;
        }

        @Override
        public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
        	Log.d(TAG, "Page error: " + description);
        	
            super.onReceivedError(view, errorCode, description, failingUrl);
      
            mListener.onError(description);
            
            TwitterDialog.this.dismiss();
        }

        @Override
        public void onPageStarted(WebView view, String url, Bitmap favicon) {
            Log.d(TAG, "Loading URL: " + url);
            super.onPageStarted(view, url, favicon);
            mSpinner.show();
        }

        @Override
        public void onPageFinished(WebView view, String url) {
            super.onPageFinished(view, url);
            String title = mWebView.getTitle();
            if (title != null && title.length() > 0) {
                mTitle.setText(title);
            }
            mSpinner.dismiss();
        }

    }
}

</pre>

And as we can expect, TwitterSession manages the twitter session:

<pre lang="java">
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.content.Context;

public class TwitterSession {
	private SharedPreferences sharedPref;
	private Editor editor;
	
	private static final String TWEET_AUTH_KEY = "auth_key";
	private static final String TWEET_AUTH_SECRET_KEY = "auth_secret_key";
	private static final String TWEET_USER_NAME = "user_name";
	private static final String SHARED = "Twitter_Preferences";
	
	public TwitterSession(Context context) {
		sharedPref 	  = context.getSharedPreferences(SHARED, Context.MODE_PRIVATE);
		
		editor 		  = sharedPref.edit();
	}
	
	public void storeAccessToken(twitter4j.auth.AccessToken accessToken, String username) {
		editor.putString(TWEET_AUTH_KEY, accessToken.getToken());
		editor.putString(TWEET_AUTH_SECRET_KEY, accessToken.getTokenSecret());
		editor.putString(TWEET_USER_NAME, username);
		
		editor.commit();
	}
	
	public void resetAccessToken() {
		editor.putString(TWEET_AUTH_KEY, null);
		editor.putString(TWEET_AUTH_SECRET_KEY, null);
		editor.putString(TWEET_USER_NAME, null);
		
		editor.commit();
	}
	
	public String getUsername() {
		return sharedPref.getString(TWEET_USER_NAME, "");
	}
	
	public twitter4j.auth.AccessToken getAccessToken() {
		String token 		= sharedPref.getString(TWEET_AUTH_KEY, null);
		String tokenSecret 	= sharedPref.getString(TWEET_AUTH_SECRET_KEY, null);
		
		if (token != null && tokenSecret != null) 
			return new twitter4j.auth.AccessToken(token, tokenSecret);
		else
			return null;
	}
}
</pre>

Now let''s see how this works. In this application we will need to insert our consumer and private keys in the upper variables. The rest of the code is easy to understand: we will initialize the Twitter object, and we will post!

<pre lang="java">

public class ProceedActivity extends Activity {
	
	private TwitterApp mTwitter;

	private static final String twitter_consumer_key = "key";
	private static final String twitter_secret_key = "key";
	private String username = "";
	Dialog dialog ;
	
	 private final TwDialogListener mTwLoginDialogListener = new TwDialogListener() {
	        @Override
	        public void onComplete(String value) {
	            username    = mTwitter.getUsername();
	            username    = (username.equals("")) ? "No Name" : username;
	            Toast.makeText(getActivity(), "Connected to Twitter as " + username, Toast.LENGTH_LONG).show();
	            postToTwitter(String.valueOf("texto"));
	        }
	 
	        @Override
	        public void onError(String value) {
	        	Toast.makeText(getBaseContext(), "Twitter connection failed", Toast.LENGTH_LONG).show();
	        }
	    };
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.proceed);
		
		mTwitter = new TwitterApp(this, twitter_consumer_key,twitter_secret_key);
		   
		mTwitter.setListener(mTwLoginDialogListener);
	 
		dialog = new Dialog(this);
		dialog.setContentView(R.layout.custom_dialog);
		
	      
					ImageView imageTwitter = (ImageView) dialog.findViewById(R.id.imageTwitter);
					
					 imageTwitter.setOnClickListener(new OnClickListener() {

						@Override
						public void onClick(View v) {
							ProgressDialog dialog = ProgressDialog.show(getBaseContext(), "", 
			                        "Loading. Please wait...", true);
							if (mTwitter.hasAccessToken()) {
								postToTwitter(String.valueOf("texto"));
							} else {
								mTwitter.authorize();
							}
							dialog.dismiss();
						}
						 
					 });
					
					
			
	}

	
	
	private void postToTwitter(final String review) {
    	
        new Thread() {
            @Override
            public void run() {
                int what = 0;
 
                try {
                    mTwitter.updateStatus(getResources().getString(R.string.finalTextShare)+" "+review);
                } catch (Exception e) {
                    what = 1;
                }
 
                mHandler.sendMessage(mHandler.obtainMessage(what));
            }
        }.start();
    }
 
    private Handler mHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            String text = (msg.what == 0) ? "Posted to Twitter" : "Post to Twitter failed";
            dialog.dismiss();
            Toast.makeText(getBaseContext(), text, Toast.LENGTH_SHORT).show();
        }
    };
    
    
    public Activity getActivity () {
    	return this;
    }
	
	
}
</pre>

Enrique López-Mañas