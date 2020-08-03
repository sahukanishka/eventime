# eventime
<h3>Team project  </h3>
<p>kanishka sahu 
Vivek sharma 
Simarpreet singh </p>

<h3> About </h3>

<p>Events are the most recurring and crucial part of our studies as we learn a
lot from them. But sometimes managing it becomes a cumbersome
process and sometimes leads to wrong info spreading and sometimes
students don&#39;t get updates of new events happening around them. This
website is meant to make the event management a bit easier. As
everything related to events is collected at a single source therefore
everybody has ease to find any event and any info about it without any
hassle.
In this platform teachers and students can see updates of new events and
also show interest in an event by participating in it which also makes the
teacher to know the audience engagement. A single platform also makes it
easier to manage the events flawlessly.</p>


 <img alt="Qries" src="https://gm1.ggpht.com/puYfg_SFfpP0W7q0y_mJo4erP-DMBijF5G6sMMfieiuo2o20HJ0-p3FlW6POW8sL-Fo94vINve9VTcXt_KUEmP-0DH5FeFoMgeFtDn74VOAiFN42lZayuS5weTza-epIqdIM1ze2nSvqHH8Kcl2za3fcJoJysNuUUtv2wRpVOcybb1C4Tpu0V2RrcykVU1ZlXrJtFCdg4VNMqOm0vkWyzuryroIy0MJUyl2sTYk3np-drzVmNmxVDLeXQKPTazBa4sIWu_sd2kf4JnYNYbfFduoMKAKjxveX21HSrPD9NglvLAhMZlHnnmoYf4pUCcoSPEY7ibRpjCO5MNHMg92efcL1iDZnXHSrWbHzkOyIB2k7irRggXGQ1ww5TqWA0WgjT2uC3x3wKb89-mr_XELG4NrgpNYkEyrN-fFY_MTO1n70NLtXie_KsqV0kEdF9DKlFEdtbj9xHouaI8G6R7Qjw1jwZBzLMFGOgJPvuRxrpLJxCNudVJBAlz4aByQRtZciOQlrPYQ37iK_oQzUqqrmyZuWO6YqIGiJm-7zxYrSSXqwaRO0QaPNkHJUNNLN0iDOi4X_qkIDsCHg_7dOldLp4PZhI6rYHUqjHy-5t--zcuJ9UH_lEfvK0D1F4btI8ZLtHRewItpRrei84Olcnm9fwL1TGgtbIvMd4cbNjHAMjmV6P0W6Kms5yyxTV18cP3MLXBL12Wxr8zSQ9xqvDTqMAF5TnxtzjkdCc8JVjPKBfuFL8FQ3kAX6XiBM6x2fQXwnDXfXJg=s0-l75-ft-l75-ft"

<h2>End points of Website </h2>


1. ‘/’ :
I. GET method:
This route serves the purpose of checking previous login with
the use of cookies.
It can cause 2 states:
a. If user was not logged in then it will redirect to the login
page
b. If a user already was logged in previously then it will
redirect to the homepage endpoint.

2. ‘/login’ :
I. GET method:
This method is used to send the login html page to the user.
II. POST method:
● This method is used when the user has submitted the
login form.
● It also checks that the data user entered exist or is it valid.
● After successful submission of data session is
manipulated so that there is no need to login next time.
● In this method we have user id, password as values and
we make sure that the hashed password is matched with
the user input password’s hash.

3. ‘/register’ :
I. GET method:
This method sends the register html page to the user.

30

II. POST method:
● This method is called when the user submits the
registration data.
● Data include user id, password, access type, department
name.
● The input password is firstly converted to its hash and
then it is stored in database

4. ‘/home’ :
I. GET method:
● This method handles display of homepage by sending
home html to user.
● It also takes events data from our mongodb database.
● We have used jinja templating to manipulate the events
over the html page.

5. ‘/account’ :
I. GET method:
● In this method the account html page is sent to the user.
● Prior to that the account detail is fetched from the
backend.
● There is signout option and the participated events list
which is useful to look the overview of user’s activity

6. ‘/event’ :
6.1 ‘/event/new’ :
I. GET method:
This method sends the new event form page to the user.


II. POST method:
● This is called when form is submitted by the user
● It has various data like name, description, timings,
department name, venue.
● After submission the data is pushed to the event
collection.

6.2 ‘/event/&lt;event id&gt;’:
I. GET method:
● The html page of the event is loaded.
● Firstly the event document is collected from the backend
which is passed as a dynamic route.
● Then Participants are collected from that document along
with the updates of the event.

II. POST method:
For admin:
● It is used when the admin needs to edit the data such as
removing participants.
● It also handles addition of new updates.
For student:
● It is used to participate in the event
● If already participated in the rolling out from that event.

6.3 ’/event/&lt;event id&gt;/&lt;response type&gt;’:
I. POST method:
a) Response type = ‘push’:
Adds participants to the event.


b) Response type = ‘pull’:
Removes/Rollout participant from event.
c) Response type = ‘update’:
Add a new update to the event.
d) Response type = ‘delupd’:
Delete an update of an event.

6.4 &#39;/event/&lt;event id&gt;/&lt;partid&gt;/remove&#39; :

I. POST method:
This route is only used by admin and teachers to remove
a student from participants ist of an event.

7. ‘/logout’ :
I. GET method:
Logs the user out of the website.
