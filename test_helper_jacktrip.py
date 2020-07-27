import helper_jacktrip

def test_create_command():
  server1_params = {'hub_mode': True, 'server': False,
                    'ip': '192.168.1.2', 'channels': "1",
                    'queue': "4"}
  mytrip = helper_jacktrip.PyTrip(server1_params)
  assert mytrip.create_command() == "jacktrip -C 192.168.1.2 -n1 -q4 -z"

def test_create_command_default():
  default_peer_params = {'hub_mode': False, 'ip': "",
                        'server': True, 'channels': "1",
                        'queue': "4"}
  mytrip = helper_jacktrip.PyTrip(default_peer_params)
  assert mytrip.create_command() == "jacktrip -s  -n1 -q4 -z"
