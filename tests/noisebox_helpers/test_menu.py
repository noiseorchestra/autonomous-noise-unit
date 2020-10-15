from noisebox_helpers import menu

main_menu_items = ['CONNECT TO SERVER',
                   'LEVEL METER',
                   'P2P SESSION',
                   'SETTINGS -->']

settings_items = [{"name": "INPUT", "value": "mono"},
                  "IP ADDRESS",
                  "JACKTRIP",
                  "UPDATE",
                  "<-- BACK"]

advanced_settings_items = [{"name": "INPUT", "value": "1"}, {"name": "BUFFER", "value": "6"}, "<-- BACK"]

input_values = ["1", "2"]
buffer_values = ["2", "4", "6", "8"]

def test_next_input_value():
    assert menu.next_value(input_values, "1") == "2"
    assert menu.next_value(input_values, "2") == "1"

def test_next_buffer_value():
    assert menu.next_value(buffer_values, "2") == "4"
    assert menu.next_value(buffer_values, "6") == "8"
    assert menu.next_value(buffer_values, "8") == "2"
