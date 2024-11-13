from langfuse.model import CreateTrace

from app.chat.tracing.langfuse import langfuse


class TraceableChain:

  # intercept every call to the chain automatically
  # in order to inject langfuse trace callback at run time
  def __call__(self, *args, **kwargs):
    # print('>>>> Inside the __call__() method of TraceableChain Mixin')

    # try to access the chain instance's metadata
    # print(f'>>>> Chain metadata:\n{self.metadata}')

    trace = langfuse.trace(
      CreateTrace(
        id=self.metadata['conversation_id'],  # important to be sure subsequent traces added into the same trace on langfuse
        metadata=self.metadata
      )
    )

    # add trace's callback to the existing callback flow
    callbacks = kwargs.get('callbacks', [])
    callbacks.append(trace.getNewHandler())
    kwargs['callbacks'] = callbacks

    return super().__call__(*args, **kwargs)