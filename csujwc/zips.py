import tarfile
import bz2

from contants import ZIP
# unzip factory
class UnzipFactory(object):

    @staticmethod
    def create_unzip(fname):
        if fname.endswith('bz2'):
            return Uzbz2(fname)

# unzip abstract class
class Unzip(object):
    
    def __init__(self, fname):
        self.fname = fname

    def unzip(self):
        pass

class Uzbz2(Unzip):

    def unzip(self):
        fname = self.fname
        try:
            archive = tarfile.open(fname, 'r:bz2')
            archive.debug = 0
            for tarinfo in archive:
                archive.extract(tarinfo, r'.')
            archive.close()
            return ZIP.SUCCESS
        except Exception as e:
            return ZIP.FAILED
