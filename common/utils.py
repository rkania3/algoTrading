import os
import shutil

class Utils(object):
    def archive_charts(self):

        workspace = os.getcwd()

        source = os.path.join(workspace, 'charts')
        dest = os.path.join(workspace, 'archives')

        files = os.listdir(source)

        for f in files:
            shutil.move(os.path.join(source, f), dest)

        return True