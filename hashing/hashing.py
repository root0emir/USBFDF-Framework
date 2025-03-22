import hashlib
import os
import argparse
import time

def get_supported_algorithms():
    return ["md5", "sha1", "sha256", "sha512", "sha384", "sha3_256", "sha3_512"]

def calculate_hash(file_path, hash_algorithm):
    hash_func = hashlib.new(hash_algorithm)
    file_size = 0
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
                file_size += len(chunk)
        return hash_func.hexdigest(), file_size
    except FileNotFoundError:
        return f"Error: {file_path} not found.", 0
    except PermissionError:
        return f"Error: Permission denied for {file_path}.", 0
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}", 0

def main():
    parser = argparse.ArgumentParser(description="Calculate the hash of one or more files using various algorithms.")
    parser.add_argument("files", nargs='+', help="The path to the file(s).")
    parser.add_argument("algorithm", choices=get_supported_algorithms(), help="The hash algorithm to use.")
    args = parser.parse_args()

    for file_path in args.files:
        start_time = time.time()
        hash_value, file_size = calculate_hash(file_path, args.algorithm)
        end_time = time.time()

        print(f"File: {file_path}")
        print(f"Algorithm: {args.algorithm.upper()}")
        print(f"Hash: {hash_value}")
        print(f"File Size: {file_size} bytes")
        print(f"Time Taken: {end_time - start_time:.2f} seconds")
        print("=" * 40)

if __name__ == "__main__":
    main()