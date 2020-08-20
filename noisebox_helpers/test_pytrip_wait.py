from pytrip_wait import PyTripWait


def test_check_stdout_success():
    pytrip_wait = PyTripWait()
    errors = []
    stdout = 'Received Connection from Peer!'

    pytrip_wait.check_stdout(stdout, '123.123.123.123')
    if pytrip_wait.message != ['==SUCCESS==', 'jacktrip connected!']:
        errors.append("Message does not match", stdout)
    if not pytrip_wait.connected:
        errors.append("Error: Should be connected")
    if pytrip_wait.waiting:
        errors.append("Error: Should not be waiting")

    assert not errors


def test_check_stdout_stopped():
    pytrip_wait = PyTripWait()
    errors = []
    stdout = 'JackTrip Processes STOPPED!'
    message = ['==ERROR==',
               'Could not connect to: 123.123.123.123',
               'JackTrip Processes STOPPED!']

    pytrip_wait.check_stdout(stdout, '123.123.123.123')
    if pytrip_wait.message != message:
        errors.append("Message does not match", stdout)
    if pytrip_wait.connected:
        errors.append("Error: Should not be connected")
    if pytrip_wait.waiting:
        errors.append("Error: Should not be waiting")

    assert not errors


def test_check_stdout_error():
    pytrip_wait = PyTripWait()
    errors = []
    stdout_list = ['Maybe the JACK server is not running',
                   'Unable to connect to JACK server',
                   'JACK server not running',
                   'Peer Buffer Size',
                   'Wrong bit resolution',
                   'Exiting JackTrip']

    for stdout in stdout_list:
        pytrip_wait.check_stdout(stdout, '123.123.123.123')
        if pytrip_wait.message != ['==ERROR==', stdout, 'JackTrip stopped']:
            errors.append("Message does not match", stdout)
        if pytrip_wait.connected:
            errors.append("Error: Should not be connected")
        if pytrip_wait.waiting:
            errors.append("Error: Should not be waiting")

    assert not errors
