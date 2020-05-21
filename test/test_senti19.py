# import senti19 as s19
from unittest.mock import Mock
# from .context import senti19
import senti19.senti19


def test_print_name():
    """
    test http_call
    """
    name = 'test'
    data = {'name': name}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    assert s19.http_call(req) == 'Hello {}!'.format(name)
    print("test_print_name works")


def test_print_hello_world():
    data = {}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    assert s19.http_call(req) == 'Hello World!'
    print("test_print_hello_world works")


def test_stream_listner():
    """Test stream listener """
    pass


def test_tweet_analyzer():
    """Test Tweet analyzer """
    pass


def test_tweet_processor():
    """Test Tweet processor """
    pass    



if __name__ == '__main__':
    test_print_name()
    test_print_hello_world()