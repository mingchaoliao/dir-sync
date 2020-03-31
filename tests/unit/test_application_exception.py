from sync.application_exception import ApplicationException


class TestApplicationException():
    def test_get_message_from_the_exception(self):
        message = 'this is a error message'
        try:
            raise ApplicationException(message)
        except ApplicationException as e:
            assert e.get_message() == message
