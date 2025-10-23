# Blutooth's Simple Python Web Server
A simple base to build off of for any web related shenanigans you could think of!

## How to use:
Simply clone the repository and open 'Main.py' to set the name of the port used and the name of the logger, then you can open 'HTTPHandler.py' to find two methods, 'handle_GET_request' and 'handle_POST_request', which you can change to your heart's desire.<br>

### Handling return data:
Both methods require you to return the Status Code (i.e 404 or 200), the Headers, and the Data being served to the user; The return is formated as a list:<br>
```
int: status,
list: headers,
bytes/bytes-like: data
```
<br>
Here's an example:

`return 200, [("Content-Type", "text/html")], "<html></html>"`<br>

You can also return using the built in 'error' function, which you can use by calling it during the return:<br>`return error(200, "Attached message")`
<br>
The error method will force the headers to return as Content-Type: application/json, but it makes error handling much more streamlined. Especially if you have to implement 1000 ways to handle user error.

### Handling GET requests:
Under the handle_GET_request function you'll see two variables for the incoming URL, and attached parameters formated in a dictionary.<br>
The URL part is a list of all the keywords the user sends that appear after the domain name.<br>

<sub>Example: `https://thatgalblu.com/code/brainf_ck` will result in `url = ["code", "brainf_ck"]` & `paramters = {}`<br>
Example 2: `https://thatgalblu.com/images/camera?latest=true` will result in `url = ["images", "camera"]` & `paramters = {"latest": "true"}`<br>
Note: The paramters are separated by commas and do not require the format of key=value. If no value is provided, it will default to boolean true</sub><br>

The method also detects if you are requesting a file instead of an index, and the function is split in two parts for returning bare files and for handling/returning `index.html`'s.<br>
Both halves will handle missing/unfindable files with the `Server.fourohfour` variable, which you can use to send the 404 page found in the "http/404" folder back to the user.<br><br>

You can use the index handler as an example on how to send html files, or really any file, after some processing has happened.

### Handling POST requests:
By default, all POST requests must be formated as application/json with this structure:<br>
```
{
  "method": string
}
```
After that, you can add anything else you want to the JSON and handle it within the method itself<br><br>

I personally like to format the method as
```
...
match method:
  case "foo":
    try: bar = data['bar']
    except: return error(400, "No bar in the data.")
    ...
  case _: return error(400, "Unknown method")
```

## Caveats:
Currently, the code is not able to properly parse non-trailing-slash links.<br>
<sub>https://thatgalblu.com vs. https://thatgalblu.com/</sub><br>
Using a non-trailing-slash link will cause relative file paths to break and think that they are one folder above where they actually are.<br>
You can add a line in the 'Main.py' file to automatically redirect those links to add a slash to the end, or just not use relative file paths, but neither of those options are fun.<br>
I'll be working on fixing this in the mean time, hopefully it won't take too long to implement!