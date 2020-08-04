import jack

client_1_stereo = jack.Client('client_1_stereo')
client_2_stereo = jack.Client('client_2_stereo')
client_3_mono = jack.Client('client_3_mono')
client_4_stereo = jack.Client('client_4_stereo')
client_5_mono = jack.Client('client_5_mono')
client_6_stereo = jack.Client('client_6_stereo')

client_1_stereo.activate()
client_2_stereo.activate()
client_3_mono.activate()
client_4_stereo.activate()
client_5_mono.activate()
client_6_stereo.activate()

client_1_stereo.outports.register("receive_1")
client_1_stereo.outports.register("receive_2")
client_2_stereo.outports.register("receive_1")
client_2_stereo.outports.register("receive_2")
client_3_mono.outports.register("receive_1")
client_4_stereo.outports.register("receive_1")
client_4_stereo.outports.register("receive_2")
client_5_mono.outports.register("receive_1")
client_6_stereo.outports.register("receive_1")
client_6_stereo.outports.register("receive_2")

client_1_stereo.inports.register("send_1")
client_1_stereo.inports.register("send_2")
client_2_stereo.inports.register("send_1")
client_2_stereo.inports.register("send_2")
client_3_mono.inports.register("send_1")
client_4_stereo.inports.register("send_1")
client_4_stereo.inports.register("send_2")
client_5_mono.inports.register("send_1")
client_6_stereo.inports.register("send_1")
client_6_stereo.inports.register("send_2")

all_port_names = ["client_1_stereo:receive_1", "client_1_stereo:receive_2",
                  "client_2_stereo:receive_1", "client_2_stereo:receive_2",
                  "client_3_mono:receive_1", "client_4_stereo:receive_1",
                  "client_4_stereo:receive_2", "client_5_mono:receive_1",
                  "client_6_stereo:receive_1", "client_6_stereo:receive_2",
                  "client_1_stereo:send_1", "client_1_stereo:send_2",
                  "client_2_stereo:send_1", "client_2_stereo:send_2",
                  "client_3_mono:send_1", "client_4_stereo:send_1",
                  "client_4_stereo:send_2", "client_5_mono:send_1",
                  "client_6_stereo:send_1", "client_6_stereo:send_2"]

unique_port_names = ["client_1_stereo",
                     "client_2_stereo",
                     "client_3_mono",
                     "client_4_stereo",
                     "client_5_mono",
                     "client_6_stereo"]

jacktrip_receive_ports = [
    ["client_1_stereo:receive_1", "client_1_stereo:receive_2"],
    ["client_2_stereo:receive_1", "client_2_stereo:receive_2"],
    ["client_3_mono:receive_1"],
    ["client_4_stereo:receive_1", "client_4_stereo:receive_2"],
    ["client_5_mono:receive_1"],
    ["client_6_stereo:receive_1", "client_6_stereo:receive_2"]]

jacktrip_send_ports = [
    ["client_1_stereo:send_1", "client_1_stereo:send_2"],
    ["client_2_stereo:send_1", "client_2_stereo:send_2"],
    ["client_3_mono:send_1"],
    ["client_4_stereo:send_1", "client_4_stereo:send_2"],
    ["client_5_mono:send_1"],
    ["client_6_stereo:send_1", "client_6_stereo:send_2"]]

all_connections = [
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_3_mono:send_1']),
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_5_mono:send_1']),
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_3_mono:send_1']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_5_mono:send_1']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_3_mono:receive_1'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_3_mono:receive_1'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_3_mono:receive_1'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_3_mono:receive_1'],
        ['client_5_mono:send_1']),
    (['client_3_mono:receive_1'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_3_mono:send_1']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_5_mono:send_1']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_5_mono:receive_1'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_5_mono:receive_1'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_5_mono:receive_1'],
        ['client_3_mono:send_1']),
    (['client_5_mono:receive_1'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_5_mono:receive_1'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_3_mono:send_1']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_5_mono:send_1'])]
