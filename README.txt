NoinoTheGreatOnion
Onion router in python

SETUP:
-Install Python 2.7.9
-Install virtualenvwrapper
-Create a virtualenv and activate it
-Install all packages from requirements.txt

RUNNING:
-Start the server:
    $ python server.py [port]   \# server listens on [port]
    ex. $ python server.py 9099
-Start clients (>3 required for requests to go through):
    $ python client.py [port client will listen on] [port server is listening on] [server IP]
    ex. $ python client.py 6000 9099 123.123.123.123
-Wait for the server to register all the clients (~5 seconds)
-Enter one URL at a time into any client’s stdin, and the response to the GET request on that
 URL will be onion-routed back to that client
    -Timeouts will be indicated by the client. Sending another URL on that client is allowed
     after a timeout.

NOTE:
The current implementation of Noino only supports GET requests that return small responses.
In order to minimize timeouts, try to query for responses smaller than 5KB.

EXAMPLE CLIENT INTERACTION
$ python client.py 6000 9099 123.123.123.123
https://www.eecs.tufts.edu/~jknigh02/
<!DOCTYPE html>

<html>

<head>
<title>My News Feed</title>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script>
    $(document).ready(function() {
//         var init_s = $("#news").html;
    
        if (window.localStorage.length != 0) {
            load_storage();
        }
    
        $("#msg").keypress(function (e) {
            if (e.which == 13) {
                store();
            }
        });

        function store() {
            var curr = Date();
            var news = "<p>" + curr + "&nbsp;-&nbsp" + $("#msg").val() + "</p>";
            $("#msg").val("");
            localStorage.setItem(curr, news);
            load_storage();
        }
        
        //source: http://stackoverflow.com/questions/3138564
        function load_storage() {
            $("#news").html("<p>News...</p>");
            for (var i = localStorage.length - 1; i >=0; i--) {
                $("#news").append(localStorage.getItem(localStorage.key(i)));
            }
        }
    });
    </script>
</head>

<body>
    <h1>My News Feed</h1>
    <h3>My news update: <input type="text" id="msg" name="msg" size="30" /></h3>
    <div id="news">News...</div>
</body>
</html>