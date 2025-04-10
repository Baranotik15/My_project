from pathlib import PurePath, PurePosixPath

from storages.backends.dropbox import DropboxStorage

class PatchedDropboxStorage(DropboxStorage):
    def _full_path(self, name):
        fixed_name = PurePath(name).as_posix()
        full_path = (PurePosixPath(self.root_path) / fixed_name).as_posix()
        return full_path
