import sys; sys.path.insert(0, '.')
from omnitype.storage.config import AppConfig
from omnitype.core.trigger_parser import TriggerParser

cfg = AppConfig()
parser = TriggerParser(cfg)

print("Testing all triggers with space:")
tests = [
    ('Hello world .g', 'grammar'),
    ('Please reply .polite', 'tone'),
    ('Bonjour .tr', 'translate'),
    ('What is AI .ta', 'ask_ai'),
    ('Fix this ...make formal...', 'custom_rewrite'),
    ('hello.g', None),  # no space — should NOT match
    ('hello  .g', 'grammar'),  # double space — should match
]
for text, expected in tests:
    m = parser.parse(text)
    got = m.trigger_type if m else None
    status = 'PASS' if got == expected else 'FAIL'
    print(f'  [{status}] "{text}" -> {got}  (expected {expected})')

# Simulate what happens when keyboard lib sends 'space' as event.name
print("\nSimulating keyboard buffer with 'space' key name fix:")
chars = ['h','e','l','l','o',' ','.','g']  # after fix: space = ' '
buf = ''.join(chars)
m = parser.parse(buf)
print(f'  Buffer: {repr(buf)} -> {m.trigger_type if m else None}')
