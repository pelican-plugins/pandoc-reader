from datetime import datetime
from pelican import signals
from pelican.readers import BaseReader
import pypandoc

class NewReader(BaseReader):
    enabled = True
    file_extensions = ['md', 'markdown', 'mkd', 'mdown']

    def read(self, filename):
        with open(filename) as file:
            metadata_items = []
            in_content = False
            MD = ''
            for line in file.readlines():
                splitted = line.split(':', 1)
                if len(splitted) == 2 and not in_content:
                    metadata_items.append(splitted)
                else:
                    in_content = True
                    MD += line

            metadata = {}
            for item in metadata_items:
                name, value = item
                name = name.lower()
                value = value.strip()
                meta = self.process_metadata(name, value)
                metadata[name] = meta

        if 'PANDOC_ARGS' in self.settings:
            output = pypandoc.convert(MD, 'html5', format='md', extra_args=self.settings['PANDOC_ARGS'])
        else:
            output = pypandoc.convert(MD, 'html5', format='md')

        return output, metadata

def add_reader(readers):
    readers.reader_classes['md'] = NewReader

def register():
    signals.readers_init.connect(add_reader)
