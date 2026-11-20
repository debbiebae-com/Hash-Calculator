# SHA-256 File Integrity Checker

A beginner Python project that prints SHA-256 hashes for five sample files and shows how changing one character changes a file's hash. It includes a repeatable demo that leaves the original files untouched.

## Objectives

- Compute SHA-256 hashes without loading entire files into memory.
- Verify that unchanged files produce identical hashes across runs.
- Observe how a one-character edit affects a digest.
- Report file access errors without stopping the rest of the scan.

## How SHA-256 works

SHA-256 deterministically turns any sequence of bytes into a 256-bit digest, displayed here as 64 hexadecimal characters. Think of the digest as a digital fingerprint: matching a trusted earlier digest gives strong evidence that the bytes have not changed. Hashes do not encrypt files or prove who changed them.

The **avalanche effect** means that a small input change typically changes about half the output bits. SHA-256 is preferred over SHA-1 because practical collision attacks can produce two different inputs with the same SHA-1 digest; no practical collision attack is known for full SHA-256. Keep reference hashes somewhere trusted: if someone can replace both the file and its reference hash, a plain hash check cannot reveal the substitution.

## Project layout

```text
SHA256-File-Checker/
├── .gitignore
├── README.md
├── main.py
└── test_folder/
    ├── file1.txt
    ├── file2.txt
    ├── file3.txt
    ├── file4.txt
    └── file5.txt
```

## Linux setup and usage

Use Python 3.8 or later. No packages or virtual environment are needed. From the repository root:

```bash
cd SHA256-File-Checker
python3 --version
python3 main.py
```

The script checks regular files directly inside the project's `test_folder`. It skips subdirectories and symbolic links. It runs once rather than monitoring continuously.

### Example output (excerpt)

```text
file1.txt: d9014c4624844aa5bac314773d6b689ad467fa4e1d1a50a1b8a99d5a95f72ff5

One-character demo (temporary copy of file1.txt: H → h)
Original: d9014c4624844aa5bac314773d6b689ad467fa4e1d1a50a1b8a99d5a95f72ff5
Modified: 4dca0fd5f424a31b03ab807cbae77eb32bf2d089eed1cee154b3afed458de0dc
File changed: yes
```

### Repeat the experiment

In Bash, compare two runs without changing any files:

```bash
diff -u <(python3 main.py) <(python3 main.py)
```

No output from `diff` means the runs match. To test a change yourself, make a separate copy of a sample and edit only that copy:

```bash
cp --no-clobber test_folder/file1.txt review-copy.txt
sha256sum review-copy.txt
nano review-copy.txt
sha256sum review-copy.txt
```

Use a different scratch filename if `review-copy.txt` already exists. In Nano, change `H` in `Hello` to `h`, save, and compare the two hashes. Remove your scratch copy before staging files. The built-in demo makes and removes its own temporary copy automatically.

## What I learned

- `hash_file()` opens a file in binary mode (`rb`) so Python reads the exact bytes. The `with` block closes the file, and the loop feeds 4096-byte chunks to one hash object until it reaches the end. An empty file still has a valid digest.
- `scan_test_folder()` uses `Path` to locate the folder beside the script, and `try`/`except` to report expected filesystem errors and continue past an unreadable file.
- `demonstrate_change()` uses a temporary copy, edits one byte, and compares the two digests. The `if __name__ == "__main__"` check lets me import the functions without starting the scan.

## Ethical and legal notice

This tool is intended only for monitoring files and folders you own or have explicit permission to monitor. Unauthorized monitoring or accessing systems without permission may violate laws.
