import os
from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open
import pypandoc

class NewReader(BaseReader):
    enabled = True
    file_extensions = ['md', 'markdown', 'mkd', 'mdown']


    def read(self, filename):
        with pelican_open(filename) as text:
            metadata_items = []
            in_content = False
            MD = ''
            for line in text.splitlines():
                splitted = line.split(':', 1)
                if len(splitted) == 2 and not in_content:
                    metadata_items.append(splitted)
                else:
                    in_content = True
                    MD += line + '\n'

            metadata = {}
            for item in metadata_items:
                name, value = item
                name = name.lower()
                value = value.strip()
                meta = self.process_metadata(name, value)
                metadata[name] = meta

        os.chdir(self.settings['PATH']) # change the cwd to the content dir
        if 'PANDOC_ARGS' in self.settings:
            output = pypandoc.convert(MD, 'html5', format='md', extra_args=self.settings['PANDOC_ARGS'])
        else:
            output = pypandoc.convert(MD, 'html5', format='md')

        return output, metadata

def add_reader(readers):
    readers.reader_classes['md'] = NewReader

def register():
    signals.readers_init.connect(add_reader)
