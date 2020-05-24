##How to Set Up a Cloud Function Triggered by a Cloud Storage Pub/Sub Topic

Useful GCP documentation links:  
* [PubSub Tutorial](https://cloud.google.com/scheduler/docs/tut-pub-sub)  
* [PubSub Notifications for Cloud Storage Documentation](https://cloud.google.com/storage/docs/pubsub-notifications)  
* [PubSub Notifications for Cloud Storage Tutorial](https://cloud.google.com/storage/docs/reporting-changes)

### 1. Set up a Cloud Function 
Open the GCP console and go to the "Cloud Functions" page.  
Click "Create Function".  
Choose a descriptive name for your function. Leave the memory allocation at its default value.  
Change the Trigger to "Cloud Pub/Sub". You will be required to selection a Cloud Pub/Sub topic from a drop-down menu.  
If you haven't made a Pub/Sub topic yet, you will be prompted to create a topic. Make sure you choose a descriptive name and remember it for later.    
For now, we'll just leave the defaul "hello_pubsub" functions in place, and change them later once we're certain the function is being trigger correctly.  

### 2. Set up Pub/Sub for Storage Buck "Notification Configuration"
We want our cloud function to trigger whenever a file in our storage is added or changed.  
To do so, we'll set up a "Notification Configuration" for our bucket, which specifies the Pub/Sub topic to receive notification, the events to trigger notifications, and the information contained within notifications.  

First, make sure you have the necessary permissions [documented here](https://cloud.google.com/storage/docs/reporting-changes).  
You will need to add the "Storage Object Admin" role for your bucket/username.  
Now go to "IAM & Admin", and add the "Pub/Sub Admin" role for your username.  
Next, open the GCP cloud shell by clicking the ">_" icon in the upper right corner of the console. It may take a few minutes to set up the shell machine.  
Now create the notification in the shell like so:  
```
gsutil notification create -f json -t pubsub-topic-name -e OBJECT_FINALIZE gs://bucket-name
```
Make sure to replace `pubsub-topic-name` and `bucket-name` with your values.
The `OBJECT_FINALIZE` flag means that notifications will only be sent when a new object is finished being added to the bucket.  

### 3. Test Your Pub/Sub Topic
To test your pub/sub topic, we'll want to add a "Pull" subscriber so that we can easily view our activity log.  
To do this, go to "Pub/Sub", click your topic, click the "Create Subscription" drop-down menu at the bottom, and choose "Create subscription".  
Give your topic a well-named ID, choose "Pull" delivery type, keep the other default settings and click "Create".  
Now it's time to test it out!  
Navigate to your bucket in the console and add a test file to the bucket.  
Wait a few minutes, then navigate to your Pub/Sub topic and click "View Messages" at the top.  
Select the testing subscription you just made, then click "Pull". A message should appear in the table below.  
Next, navigate to your cloud function and click "View Logs" at the top. 
You should see multiple lines beginning with `Function execution started`, followed by several JSON lines describing the triggering event.
