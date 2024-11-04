#
#
## Second day of Election Month 2024
## TODO
# 
* add a menu item that adds a task to the todo list
* add a menu item that adds a subtask to the todo list

Looks like test_ah_assistant is the latest.  The plan is to add a todo to the todo list using the smart menu system.

After that, we will add a subtask.
Let's add a todo and then show the todo list.

show the id's in the todo list so that we can use it to remove a task.  or maybe assing it to the "done_list".  this would be valuble for tracking time for invoices.

When this is working, we can start asking the assistant to crud the todo and done list.


#
#
## First day of Novemer 2024
#
### The Airplane Gauge
* get the subscription working on the awm side.
    - create a StoreKit configuration file.
    - set up a StoreKit configuration.
    - enable StoreKit testing in Xcode.
    - prepare to validate receipts in the test ennvironment.

#
### Agent Builder Project
* Add a Todo to a todo list.  make sure the the part that writes to the file is completely decoupled from the other parts of the todo system.
    - add the todo in the smart menu
    - in the smart menu selection, fire up the system that adds the todo to the todo list.
* Start the Agent Builder project


#
### Firebase issues to bed
- debug PHP script from the command line.
part that writes to the file is completely decoupled from the other parts of the todo system.

##
## Done
### Largo Matrix
* 1:19pm moved TB up 6 rows.  checked TB flashing is ok.  moved TP 9 one row to the right.
* 1:31pm checked TB and Set score blinking ok and wrote the end note.

#
#
## Halloween 2024
* remember the agents below.  expand on them.  make one.  make more. start communication busses.
* create a todo list.  start here.

## TODO
### Largo Matrix
* 12:20pm - move TB up 6 rows
* 12:22pm - Tweak #22, as the TB is not flashing when the Set score flashes.
* 12:32pm - In  the two TBs "9" need to move one column to the right.
# 
#
### Agent Builder Project
* Start the Agent Builder project
* Add a Todo to a todo list.  make sure the the part that writes to the file is completely decoupled from the other parts of the todo system.
#
### The Airplane Gauge
* get the subscription working on the awm side.
    - open the Xcode project
    - find out where the subscription is supposed to connect. - 2:12pm
    - finished fixing the double printing of messages.  the app delegate was initiating the root window.  only to this in the scene delegate. - 2:51pm
    - find out if this thing is working or not.



#
### Firebase issues to bed
- rewrite PHP curl part to use jwt when getting the fresh token for sending a message. - 4:51pm
- still looking for logs!  - 6:13pm
- wire in and test the now working message sending system.

##
## Done
### Largo Matrix
* 1:19pm moved TB up 6 rows.  checked TB flashing is ok.  moved TP 9 one row to the right.
* 1:31pm checked TB and Set score blinking ok and wrote the end note.

#### end note
I have move the TB up 6 rows.  The TB "9" has been moved one column to the right.
The TB blinking looks OK to me for both Match and Set scenarios.  If you still see a problem, please put the machine in the state where you think that there is a problem and I will take a break from what I am doing and look at it.

Also, I have seen the broken Undo scenario a few times already during testing.  I can not pinpoint how to reproduce the problem.  I think it has something to do with the timeout.  I am mentioning this now so that when we approach the end of wrapping this part up, we should probably spend some more time on getting this bug reproduced and fixed.

I am going to sign off now, but if you need me to take a look at something later on today, I will be available for that.
#### note end  1:30pm

### The Airplane Gauge
* Added subscription and subscription localization.  4:36pm  waiting for review... 4:40pm

#
### Firebase issues to bed


##
##
## Wednesday October 30, 2024

I was able to get the Vision Team iOS app to receive a Firebase message.  I will finish cleaning all of the code up and testing the chat system tomorrow.  We will put this Firebase communication issue to bed for good.  I should have the iOS chat system working tomorrow at some point.

## Remaining steps to get Firebase working:
- Follow instructions in the link below to get PHP to generate tokens on the fly for each message to send.

### link to 4o chat about connecting to a google service account:
https://chatgpt.com/share/6722e639-b610-8006-88fb-4b8f9c4053dd

### Successful Firebase communication:
```bash
curl -X POST -H "Authorization: key=AAAAw8pNIFs:APA91bGvEcd3eK94Sxd-NlFPckxwmD8GMX616A-yccmcKZdIWJHZYYlgR4ga0zcfRCVRXONBO3YGLUuEml7yuqtGuU4UxZ0MzfodcvCIdI6snTWaJDVlxvd3gbc3qWczX_H4lpgvpcAx" \
   -H "Content-Type: application/json" \
   -d '{
         "to": "eoQkLf4l0UUUrurCYYI0AU:APA91bHcIydEC-dghyqe7gdZYP6rK4_TXqQ_5cIbaZFiECA69szKHKIn6paqjV7WE61Sr8NGLDbK2m7n83i54lk1jMY0GD0bHAw4MomvjMsJOZGU_79xj5Q",
         "notification": {
           "title": "Test Notification",
           "body": "This is a test message from Firebase"
         },
         "data": {
           "customKey": "customValue"
         }
       }' \
   https://fcm.googleapis.com/fcm/send
```

# FCMClient class
```php
<?php

class FCMClient {
    private $serviceAccountPath;
    private $projectId;

    public function __construct($serviceAccountPath, $projectId) {
        $this->serviceAccountPath = $serviceAccountPath;
        $this->projectId = $projectId;
    }

    public function getAccessToken() {
        $tokenUrl = 'https://oauth2.googleapis.com/token';
        $jwt = $this->createJwt();

        $postData = http_build_query([
            'grant_type' => 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion' => $jwt,
        ]);

        $opts = ['http' => [
            'method' => 'POST',
            'header' => "Content-Type: application/x-www-form-urlencoded\r\n",
            'content' => $postData,
        ]];

        $context = stream_context_create($opts);
        $response = file_get_contents($tokenUrl, false, $context);
        $response = json_decode($response, true);

        return $response['access_token'] ?? null;
    }

    private function createJwt() {
        $serviceAccount = json_decode(file_get_contents($this->serviceAccountPath), true);
        $header = base64_encode(json_encode(['alg' => 'RS256', 'typ' => 'JWT']));
        $now = time();
        $claimSet = [
            'iss' => $serviceAccount['client_email'],
            'scope' => 'https://www.googleapis.com/auth/firebase.messaging',
            'aud' => 'https://oauth2.googleapis.com/token',
            'exp' => $now + 3600,
            'iat' => $now,
        ];

        $payload = base64_encode(json_encode($claimSet));
        $data = $header . '.' . $payload;
        $signature = '';
        openssl_sign($data, $signature, $serviceAccount['private_key'], 'sha256');
        $jwt = $data . '.' . base64_encode($signature);

        return $jwt;
    }

    public function sendPushNotification($fields) {
        $url = 'https://fcm.googleapis.com/v1/projects/' . $this->projectId . '/messages:send';
        $accessToken = $this->getAccessToken();

        if (!$accessToken) {
            die("Error: Unable to obtain access token.");
        }

        $headers = [
            'Authorization: Bearer ' . $accessToken,
            'Content-Type: application/json',
        ];

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($fields));

        $result = curl_exec($ch);

        if ($result === false) {
            die('Curl failed: ' . curl_error($ch));
        }

        curl_close($ch);
        return $result;
    }
}

// Usage example:
$serviceAccountPath = '/path/to/service-account.json';
$projectId = 'visionteam-78cf8';

$fcmClient = new FCMClient($serviceAccountPath, $projectId);

// Define the notification payload
$fields = [
    "message" => [
        "token" => "eoQkLf4l0UUUrurCYYI0AU:APA91bHWqC5ImwBdylRtCs_dXVy4nJl2Qu74hBR746rFg12sbQXLJPWslRd2vPVrYrwLig2xIzBss20KUUCz0kX1qzbD-0eY7HK_prgxwRPDIUc90fo4D-Yarko8pyKrZibngiTUqahP",
        "notification" => [
            "title" => "Test Message",
            "body" => "This is a test notification sent via PHP",
        ],
        "data" => [
            "customDataKey" => "customDataValue",
        ],
    ],
];

$result = $fcmClient->sendPushNotification($fields);
echo "FCM Response: " . $result;
```

## Tuesday October 28, 2024
In Build Settings.  Take out Main from UIKit Main Storyboard File Base Name


# For Apple account in account.apple.com
- Enter first, last name and birthdate
- Enter email address and phone number
- Verify email address and phone number with codes.



## Sunday October 26, 2024
start with this todo list
make automatic time logger
11:53 am - this list is born again.

* start making a list of commands to quickly start projects.
	right now.  it is sunday.  I need to change the Android system in the same
	way that I changed the iOS system

* find the places in code where you changed the iOS system.
	- which classes where changed from the original to what it is now with the three axes.
	- Speed Calculator
	- Acceleration Controller
* get these classes into a temp folder for comparison.

* instead of  just assigning acceleration value * 9.81, we do this 1st:
```swift
class AccelerationController {
	// instead of the z-axis, input all three axes to the speed calculation.
	let calculatedSpeed = speedCalculator!.getCurrentSpeed( three_axes_acceleration: currentValues, this_time: timestamp, last_time: self.timestamp )
	//
	// remember this for the other speed calculation types.  Sometimes the current speed is held
	// in the speed calculator object.  In the case of the original nac app, the current speed
	// is held in one of the accelerometer object variables.  In this case, the current speed.
	currentSpeed += Float( calculatedSpeed )
	// ...
}

class SpeedCalculator {
	// ...
	// three_axes_acceleration_arg passed in from the iOS system instead of just the z-axis	
	let acceleration_vector_sum = sqrt(
		pow( three_axes_acceleration_arg[ 0 ], 2 ) +
		pow( three_axes_acceleration_arg[ 1 ], 2 ) +
		pow( three_axes_acceleration_arg[ 2 ], 2 )
	)

	// Determine direction based on the z-axis acceleration
	let direction: Double = three_axes_acceleration_arg[ 2 ] < 0 ? -1.0 : 1.0

	// Calculate acceleration with direction and the vector sum of the three axes
	let acceleration = acceleration_vector_sum * direction * 9.81  // convert g-units to m/s²

	// resume original acceleration calculations with this acceleration variable which represents
	// the acceleration calculated using all 3 axes...
}
```
finished on 2:22pm

* this is the place in the Java code that correspond to the places in code where the iOS system was changed.
```java
private float getCurrentSpeed(float value, long newTimestamp) {
	float dT = (newTimestamp - this.timestamp) * NS2S;
	float result = value * dT;
	if (config.getMeasurementUnits() == MeasureConfig.MeasurementUnits.METRICS) {
		// Convert to kph
		return result * 3.6f;
	} else {
		// Convert to mph
		return result * 2.2369f;
	}
}
```

mixed weak and strong like before gym.  is that bad?
we will see...

## agent 1:
- wake up. 
- read the notes.
- If there are new notes, timestamp them.

## agent 2:
- find the project that I am looking for.
- open vscode for that project.

## agent 3:
- keep track of the amount of time that you are working on whatever project you are working on.
- find a way to detect coffee breaks.

##
##

## Friday October 25, 2024
For MCBA, The message view controller seems to be working fine except for the Firebase messaging not comming through.  I will continue to debug this communication issue next time.

I wired in and tested the Email button from the report page of the NAC app.  I have updated the minimac to the latest iOS (Sequoia 15.0.1) and updated to the latest Xcode to get iPhone 16 Pro simulator for screenshots.  I uploaded the Binary with the new 3-axes calculator.  All of the screenshots, compliances and descriptions have been filed out.  The app is ready for review and has been submitted to the app store.  After the app is accepted, we can transfer the ownership to Tim and add the subscription and pricing.

I will add the 3-axes calculator part to Android over the weekend an keep an eye on the Apple submission.  Hopefully it will be done in a few days.



## Thursday October 24, 2024
### Thursday night after starting tuesday with speedometer wrap up.
When the administrator shows up in the "li" of the chat screen, it means that the conversation in the database is ordered in such a way that makes this happen.  I fixed this today by deleting the first two top messages in the database from steve.  The way to prevent this would be todo: don't create an "li" for a conversation until we get the user in scope and not just the admin.
