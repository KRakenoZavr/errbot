from errbot import botflow, FlowRoot, BotFlow


class MyFlows(BotFlow):
    """ Conversation flows for Errbot"""

    @botflow()
    def example(self, flow: FlowRoot):
        first_step = flow.connect('first', auto_trigger=True)
        second_step = first_step.connect('second')
        third_step = second_step.connect('third')
