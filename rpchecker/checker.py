from http.client import HTTPConnection
from urllib.parse import urlparse

## Create method which takes a url and timeout arguement. 
def site_is_online(url, timeout=2):
    """Return True if the target URL is online.

    Raise an exception otherwise.
    """
    error = Exception("unknown error")
    parser = urlparse(url)

    # Extract hostname from target URL
    host = parser.netloc or parser.path.split("/")[0]

    # Check if website available over HTTP and HTTPS port
    for port in (80, 443):
        connection = HTTPConnection(host=host, port=port, timeout=timeout)

        # Attempt to make head request, throwing exception if unable to do so
        try:
            connection.request("HEAD", "/")
            return True
        except Exception as e:
            error = e
        finally:
            connection.close()
    raise error