var RequestFactories = [
	function () { return new XMLHttpRequest(); },
	function () { return new ActiveXObject("Msxml2.XMLHTTP"); },
	function () { return new ActiveXObject("Msxml3.XMLHTTP"); },
	function () { return new ActiveXObject("Microsoft.XMLHTTP"); }
];

function createRequest() {
	for (var i = 0; i < RequestFactories.length; i++)
    {
		try
        {
			return RequestFactories[i]();
		}
		catch (e)
        {
			return null;
		}
	}
}

function sendRequest(url, callback, postData) {
	var request = createRequest();
	if (!request)
    {
        return;
    }
	var method = postData ? "POST" : "GET";
	request.open(method, url, true);
	request.setRequestHeader('User-Agent', 'XMLHTTP/1.0');
	if (postData)
    {
		request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    }
	request.onreadystatechange = function () {
		if (request.readyState != 4)
        {
            return;
        }
		if (request.status != 200 && request.status != 304)
        {
			return;
		}
		callback(request);
	};
	if (request.readyState == 4)
    {
        return;
    }

	request.send(postData);
}

function toggleProperties(photo_id)
{
    var e = document.getElementById('properties');
    if (e.innerHTML == "")
    {
        sendRequest("/photo/" + photo_id + "/properties/",
                    function(request) {
                        e.innerHTML = request.responseText;
                    });
    }
    else
    {
        e.innerHTML = "";
    }
}

function toggleComments(photo_id)
{
    var e = document.getElementById('comments');
    if (e.innerHTML == "")
    {
        sendRequest("/photo/" + photo_id + "/comments/",
                    function(request) {
                        e.innerHTML = request.responseText;
                        setTimeout("window.scrollTo(0, document.body.scrollHeight)", 0);
                    });
    }
    else
    {
        e.innerHTML = "";
        window.scrollTo(0, 0);
    }
}

function submitComment(photo_id)
{
    var data =
        "human=" + encodeURIComponent(document.getElementById('human').value) + "&" +
        "name=" + encodeURIComponent(document.getElementById('name').value) + "&" +
        "email=" + encodeURIComponent(document.getElementById('email').value) + "&" +
        "url=" + encodeURIComponent(document.getElementById('url').value) + "&" +
        "text=" + encodeURIComponent(document.getElementById('text').value);

    sendRequest("/photo/" + photo_id + "/comments/",
        function(request) {
            document.getElementById('comments').innerHTML = "";
            window.scrollTo(0, 0);
        }, data);
}
