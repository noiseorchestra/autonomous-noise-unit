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

ladspa_client_1 = jack.Client('left-65')
ladspa_client_2 = jack.Client('left-30')
ladspa_client_3 = jack.Client('right-30')
ladspa_client_4 = jack.Client('right-65')

ladspa_client_1.activate()
ladspa_client_2.activate()
ladspa_client_3.activate()
ladspa_client_4.activate()

ladspa_client_1.outports.register('Output (Left)')
ladspa_client_1.outports.register('Output (Right)')
ladspa_client_2.outports.register('Output (Left)')
ladspa_client_2.outports.register('Output (Right)')
ladspa_client_3.outports.register('Output (Left)')
ladspa_client_3.outports.register('Output (Right)')
ladspa_client_4.outports.register('Output (Left)')
ladspa_client_4.outports.register('Output (Right)')

ladspa_client_1.inports.register('Input (Left)')
ladspa_client_1.inports.register('Input (Right)')
ladspa_client_2.inports.register('Input (Left)')
ladspa_client_2.inports.register('Input (Right)')
ladspa_client_3.inports.register('Input (Left)')
ladspa_client_3.inports.register('Input (Right)')
ladspa_client_4.inports.register('Input (Left)')
ladspa_client_4.inports.register('Input (Right)')

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

ladspa_sends = [['left-65:Input (Left)', 'left-65:Input (Right)'],
                ['left-30:Input (Left)', 'left-30:Input (Right)'],
                ['right-30:Input (Left)', 'right-30:Input (Right)'],
                ['right-65:Input (Left)', 'right-65:Input (Right)']]

ladspa_receives = [['left-65:Output (Left)', 'left-65:Output (Right)'],
                   ['left-30:Output (Left)', 'left-30:Output (Right)'],
                   ['right-30:Output (Left)', 'right-30:Output (Right)'],
                   ['right-65:Output (Left)', 'right-65:Output (Right)']]

ladspa_receive_connections = [
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['left-65:Input (Left)', 'left-65:Input (Right)']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['left-30:Input (Left)', 'left-30:Input (Right)']),
    (['client_3_mono:receive_1'],
        ['right-30:Input (Left)', 'right-30:Input (Right)']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['right-65:Input (Left)', 'right-65:Input (Right)']),
    (['client_5_mono:receive_1'],
        ['left-65:Input (Left)', 'left-65:Input (Right)']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['left-30:Input (Left)', 'left-30:Input (Right)'])]

ladspa_send_connections = [
    (['left-65:Output (Left)', 'left-65:Output (Right)'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['left-65:Output (Left)', 'left-65:Output (Right)'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['left-65:Output (Left)', 'left-65:Output (Right)'],
        ['client_3_mono:send_1']),
    (['left-65:Output (Left)', 'left-65:Output (Right)'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['left-65:Output (Left)', 'left-65:Output (Right)'],
        ['client_5_mono:send_1']),
    (['left-65:Output (Left)', 'left-65:Output (Right)'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['left-30:Output (Left)', 'left-30:Output (Right)'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['left-30:Output (Left)', 'left-30:Output (Right)'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['left-30:Output (Left)', 'left-30:Output (Right)'],
        ['client_3_mono:send_1']),
    (['left-30:Output (Left)', 'left-30:Output (Right)'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['left-30:Output (Left)', 'left-30:Output (Right)'],
        ['client_5_mono:send_1']),
    (['left-30:Output (Left)', 'left-30:Output (Right)'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['right-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['right-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['right-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_3_mono:send_1']),
    (['right-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['right-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_5_mono:send_1']),
    (['right-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['right-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['right-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['right-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_3_mono:send_1']),
    (['right-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['right-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_5_mono:send_1']),
    (['right-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2'])]
