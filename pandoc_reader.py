import os
from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open
import pypandoc


class PandocReader(BaseReader):
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
            for name, value in metadata_items:
                name = name.lower()
                value = value.strip()
                metadata[name] = self.process_metadata(name, value)

        os.chdir(self.settings['PATH']) # change the cwd to the content dir
        if not 'PANDOC_ARGS' in self.settings: self.settings['PANDOC_ARGS'] = []
        output = pypandoc.convert(MD, 'html5', format='md', extra_args=self.settings['PANDOC_ARGS'])

        return output, metadata


def add_reader(readers):
    for ext in PandocReader.file_extensions:
        readers.reader_classes[ext] = PandocReader

def register():
    signals.readers_init.connect(add_reader)
