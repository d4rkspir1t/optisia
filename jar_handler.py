import subprocess
import numpy
import logging


class JarCall:
    def __init__(self, path):
        self.base_call = ['java', '-jar']
        self.jar_path = path

    def make_call(self, params=[]):
        call = self.base_call
        call.append(self.jar_path)
        call.extend(params)
        print('LEN CALL: %d' % len(call))
        print('CALL:\t', call)
        print('-'*50, '\n')

        subprocess.call(call, stdout=None, stderr=None)
        # output = subprocess.call(call, stdout=None, stderr=None)
        # if output > 0:
        #     print('Warning, result was %s ' % output)


# caller = JarCall(path='omnisia.jar')
# caller.make_call(['--help'])
