from transitions import Machine


class ChatBot():
    states = [
        'asleep',
        'get pizza size',
        'get payment method',
        'make an order',
    ]

    transitions = [
        {
            'trigger': 'start',
            'source': 'asleep',
            'dest': 'get pizza size'
        },
        {
            'trigger': 'get_payment_method',
            'source': 'get pizza size',
            'dest': 'get payment method'
        },
        {
            'trigger': 'make_order',
            'source': 'get payment method',
            'dest': 'make an order'
        },
        {
            'trigger': 'end_order',
            'source': 'make an order',
            'dest': 'asleep'
        },
        {
            'trigger': 'stop',
            'source': '*',
            'dest': 'asleep'
        },
    ]

    def __init__(self):
        self.size = None
        self.payment = None

        self.machine = Machine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial='asleep'
        )
