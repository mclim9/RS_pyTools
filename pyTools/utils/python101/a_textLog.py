import logging

class testLog():
    """ instrument socket class """
    def __init__(self):
        self.filename = __file__.split('.')[0] + '.log'
        logging.basicConfig(level=logging.INFO,
                    filename=self.filename, filemode='a',         # noqa:
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa:

    def write(self, outText):
        logging.info(f'{outText}')

# #########################################################
# ## Main Code
# #########################################################
if __name__ == "__main__":
    testr = testLog()
    testr.write('hello')
    testr.write('hello')
    testr.write('hello')
