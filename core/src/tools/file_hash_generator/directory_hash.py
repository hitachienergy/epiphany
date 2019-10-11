import os
import hashlib
import logging
import argparse
import time

BLOCK_SIZE = 65536


def hash_factory(hash_algorithm):
    if hash_algorithm == "sha256":
        return hashlib.sha256()

    if hash_algorithm == "sha512":
        return hashlib.sha512()

    raise NotImplementedError


def file_hash(file_path, hash_algorithm):

    hash_engine = hash_factory(hash_algorithm)

    with open(file_path, 'rb') as file:
        buf = file.read(BLOCK_SIZE)
        while len(buf) > 0:
            hash_engine.update(buf)
            buf = file.read(BLOCK_SIZE)

    return hash_engine.hexdigest()


def create_files_to_hash_list(packages_path):
    files_to_hash = []

    logging.info("Starting creating list of files to hash")

    for root, directory, files in os.walk(packages_path):
        for file in files:
            file_full_path = os.path.join(root, file)
            if os.path.isfile(file_full_path):
                files_to_hash.append(file_full_path)

    return files_to_hash


def write_files_with_hash_to_file(files_to_hash, output_file, hash_algorithm):

    logging.info(f"Writing hash ({hash_algorithm}) list to output file")
    with open(output_file, "w") as dest_file:

        for file in files_to_hash:
            hashed_value = file_hash(file, hash_algorithm)
            logging.info(f"Filename: {file} - {hash_algorithm}: {hashed_value}")
            dest_file.write(f"{hashed_value}  {file}\n")


def parse_arguments():
    parser = argparse.ArgumentParser('Run hash function over directory.')

    parser.add_argument('-p', '--packages-directory', type=str,
                        help='path where packages to hash are stored')
    parser.add_argument('-o', '--output', type=str,
                        help='file to which packages with hash will be written')
    parser.add_argument('-a', '--algorithm', type=str,
                        help='hashing algorithm available: [ sha256, sha512]')
    parser.add_argument('--debug', action='store_true',
                        help='debugging option')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    arguments = parse_arguments()

    log_level = logging.DEBUG if arguments.debug else logging.INFO

    logging.basicConfig(level=log_level)

    logging.debug(arguments)

    logging.info("Starting hash program.")

    packages_path = arguments.packages_directory
    output_file = arguments.output
    hashing_algorithm = arguments.algorithm

    start_time = time.time()

    files_to_sha = create_files_to_hash_list(packages_path)
    write_files_with_hash_to_file(files_to_sha, output_file, hashing_algorithm)

    logging.debug(f"Time of execution: {time.time() - start_time}")
