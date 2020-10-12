import noisebox_helpers as nh

level_meter = nh.level_meter.LevelMeter(port=None, name="Mock", mock=True)

def test_process_meter_value():
    assert level_meter.process_meter_value(-12) == -12
    assert level_meter.process_meter_value(-60) == -52
    assert level_meter.process_meter_value(0) == 0
    assert level_meter.process_meter_value(float('Inf')) == -52
