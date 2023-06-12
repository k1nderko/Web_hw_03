import argparse
import logging
from shutil import copyfile
from pathlib import Path
from threading import Thread, Condition


parser = argparse.ArgumentParser(description='Sorting folders')

parser.add_argument('-s', '--source', help='Source folder', required=True)
parser.add_argument('-o', '--output', help='Output folder', default='dist')

args = vars(parser.parse_args())

source = Path(args.get('source'))
output = Path(args.get('output'))

folders = [source]

def grabs_folders(path, condition: Condition):
    logging.info('getting folders...')

    def inner(path: Path):
        for f in path.iterdir():
            if f.is_dir():
                folders.append(f)
                inner(f)

    with condition:
        inner(path)
        logging.info(folders)
        condition.notify_all()


def copy_files(folder: Path):

    for f in folder.iterdir():
        if f.is_file():
            ext = f.suffix[1:]
            new_folder = output / ext
            try:
                new_folder.mkdir(parents=True, exist_ok=True)
                copyfile(f, new_folder / f.name)
            except EOFError as error:
                logging.debug(error)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    condition = Condition()

    work_with_folders = Thread(target=grabs_folders, args=(source, condition,))
    work_with_folders.start()

    with condition:
        condition.wait()

        for f in folders:

            work_with_files = Thread(target=copy_files, args=(f, ))
            work_with_files.start()

    logging.debug('Finished')