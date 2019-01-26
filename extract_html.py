


def simple_get(url_to_compute):
    """
      Attempts to get the content at `url` by making an HTTP GET request.
      If the content-type of response is some kind of HTML/XML, return the
      text content, otherwise return None.
      """
    try:

        resp = get(url_to_compute, headers=_headers, stream=True, verify=False)
        if is_good_response(resp):
            return resp.content
        else:
            return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url_to_compute, str(e)))
        return None
    except ConnectionError:
        print('Web site does not exist')
        return None




def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    try:

        content_type = resp.headers['Content-Type'].lower()
        print(resp.status_code)
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)
    except:
        return None


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
