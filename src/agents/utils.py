from time import sleep
from langchain_core.messages import AIMessage

_streaming_cache = ""
_ai_messages_ids = []
_cut_message_from = []

def _emulate_streaming(msg):
    global _streaming_cache
    for c in msg:
        print(c, end='', flush=True)
        sleep(0.02)  # simulate streaming delay
        _streaming_cache += c

def stream_agent(chunk: dict) -> str:
    global _ai_messages_ids, _cut_message_from
    if not _ai_messages_ids or chunk.id not in _ai_messages_ids:
        _ai_messages_ids.append(chunk.id)
        _cut_message_from.append(0)
    if chunk.id == _ai_messages_ids[-1]:
        _emulate_streaming(chunk.content[_cut_message_from[-1]:])
        _cut_message_from[-1] += len(chunk.content) - _cut_message_from[-1]

def get_streaming_message():
    global _streaming_cache
    msg = _streaming_cache
    _streaming_cache = "" # Clear cache after retrieving
    return msg

def clears_cache():
    global _streaming_cache, _ai_messages_ids, _cut_message_from
    _streaming_cache = ""
    _ai_messages_ids = []
    _cut_message_from = []

def find_AI_messages(messages, start_index=0):
    ai_messages = []
    ai_messages = [msg for msg in messages if isinstance(msg, (AIMessage))]
    return ai_messages[start_index:]
