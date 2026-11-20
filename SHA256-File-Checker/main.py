import hashlib
import shutil
import stat
from pathlib import Path
from tempfile import TemporaryDirectory


TEST_FOLDER = Path(__file__).resolve().parent / "test_folder"


def hash_file(path):
    """Return the SHA-256 digest of a file as 64 hexadecimal characters."""
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        # Feed bytes to the same digest object until we reach the end.
        chunk = file.read(4096)
        while chunk:
            digest.update(chunk)
            chunk = file.read(4096)
    return digest.hexdigest()


def scan_test_folder():
    """Print hashes for regular files directly inside the project's test folder."""
    try:
        if TEST_FOLDER.is_symlink():
            print("Skipping test_folder: symbolic links are not followed.")
            return
        entries = sorted(TEST_FOLDER.iterdir())
    except OSError as error:
        print(f"Could not list test_folder: {error.strerror}")
        return

    for path in entries:
        try:
            if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
                continue
            print(f"{path.name}: {hash_file(path)}")
        except OSError as error:
            print(f"Could not hash {path.name}: {error.strerror}")


def demonstrate_change():
    """Compare a sample's hash before and after editing a temporary copy."""
    source = TEST_FOLDER / "file1.txt"
    try:
        if TEST_FOLDER.is_symlink() or source.is_symlink():
            print("Demo skipped: symbolic links are not followed.")
            return
        if not source.is_file():
            print("Demo skipped: test_folder/file1.txt is missing or not a regular file.")
            return

        with TemporaryDirectory(prefix=".hash-demo-", dir=TEST_FOLDER.parent) as folder:
            copy = Path(folder) / source.name
            shutil.copyfile(source, copy)
            original = hash_file(copy)
            # The sample begins with ASCII H. Change only that byte in the copy.
            with copy.open("r+b") as file:
                if file.read(1) != b"H":
                    print("Demo skipped: file1.txt no longer starts with H.")
                    return
                file.seek(0)
                file.write(b"h")
            modified = hash_file(copy)
            print("\nOne-character demo (temporary copy of file1.txt: H → h)")
            print(f"Original: {original}")
            print(f"Modified: {modified}")
            print(f"File changed: {'yes' if original != modified else 'no'}")
            print("Avalanche effect: a tiny input change produces a very different digest.")
    except OSError as error:
        print(f"Could not run the demo: {error.strerror}")


def main():
    scan_test_folder()
    demonstrate_change()


if __name__ == "__main__":
    main()
