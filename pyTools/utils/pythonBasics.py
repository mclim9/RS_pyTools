'''Basic Python Functions'''
import os
import logging

logging.basicConfig(level=logging.INFO,
                    filename=__file__.split('.')[0] + '.log', filemode='a',         # noqa:
                    format='%(asctime)s - %(message)s')  # noqa:

logging.debug('hello')

print(f"__file__: {__file__}")
print(f"__name__: {__name__}")
globals()["Test"] = 12345
asdf = globals()
# print(globals())
print("FilePath: " + os.path.dirname(os.path.realpath(__file__)))

asdf = 8
for i in range(2, int(asdf / 2) + 1):
    print(i)
