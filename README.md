# Blutooth's Simple Python Web Server
A simple base to build off of for any web related shenanigans you could think of!

## How to use:
Simply clone the repository and open 'Main.py' to set the name of the port used and the name of the logger, then you can open 'HTTPHandler.py' to find two methods, 'handle_GET_request' and 'handle_POST_request', which you can change to your heart's desire.<br><br>

By default, the code will automatically redirect non-trailing-slash URLs. This is to prevent issues with relative pathed imports/files inside any .html and .css files you have.<br>
It also prevents any URLs from trying to back-track up your file system using "../../"

### Handling return data:
Both methods require you to return the Status Code (i.e 404 or 200), the Headers, and the Data being served to the user; The return is formated as a list:<br>
```
int: status,
list: headers,
bytes/bytes-like: data
```
<sub>Example: `return 200, [("Content-Type", "text/html")], "<html></html>"`</sub><br><br>

You can also return using the built in 'error' function, which you can use by calling it during the return:<br>
`return error(200, "Attached message")`<br>
The error method will force the headers to return as Content-Type: application/json, but it makes error handling much more streamlined. Especially if you have to implement 1000 ways to handle user error.

### Handling GET requests:
Under the handle_GET_request function you'll see two variables for the incoming URL, and attached parameters formated in a dictionary.<br>
The URL part is a list of all the keywords the user sends that appear after the domain name.<br>

<sub>Example: `https://thatgalblu.com/code/brainf_ck` will result in `url = ["code", "brainf_ck"]` & `paramters = {}`<br>
Example 2: `https://thatgalblu.com/images/camera?latest=true` will result in `url = ["images", "camera"]` & `paramters = {"latest": "true"}`<br>
Note: The paramters are separated by commas and do not require the format of key=value. If no value is provided, it will default to boolean true.</sub><br>

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
After that, you can add anything else you want to the JSON and handle it within the method itself.<br><br>

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