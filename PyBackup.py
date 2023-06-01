import os
import shutil
import time


def incremental_copy(source_folder, destination_folder):
    """
    Perform an incremental copy of a folder and its contents to a specified location.

    Args:
        source_folder (str): The path to the source folder.
        destination_folder (str): The path to the destination folder.

    Returns:
        None

    Raises:
        None
    """
    # Ensure source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    # Ensure destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get the total number of files for progress calculation
    total_files = sum(len(files) for _, _, files in os.walk(source_folder))

    # Initialize progress variables
    processed_files = 0
    copied_files = 0
    start_time = time.time()

    # List to store the copied files' information
    copied_files_info = []

    # Iterate over the source folder recursively
    for root, dirs, files in os.walk(source_folder):
        # Calculate the corresponding destination folder
        dest_root = root.replace(source_folder, destination_folder, 1)

        # Ensure the corresponding destination folder exists
        if not os.path.exists(dest_root):
            os.makedirs(dest_root)

        # Copy modified or new files to the destination
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)

            # Copy the file if it's modified or doesn't exist in the destination
            if not os.path.exists(dest_file) or (
                os.path.getmtime(src_file) > os.path.getmtime(dest_file)
            ):
                shutil.copy2(src_file, dest_file)
                copied_files += 1

                # Add copied file's information to the list
                copied_files_info.append((src_file, dest_file))

            # Update progress variables
            processed_files += 1

            # Calculate progress percentage
            progress = processed_files / total_files * 100

            # Calculate elapsed time
            elapsed_time = time.time() - start_time

            # Print progress information
            print(
                f"Progress: {progress:.2f}% | "
                f"Processed Files: {processed_files}/{total_files} | "
                f"Copied Files: {copied_files} | "
                f"Elapsed Time: {elapsed_time:.2f}s",
                end="\r",
            )

    print(
        f"\nIncremental copy completed successfully. Total Files Copied: {copied_files}."
    )

    # Generate log file
    generate_log_file(copied_files_info, destination_folder)


def generate_log_file(copied_files_info, destination_folder):
    """
    Generate a log file with the date and time of the incremental copy, containing
    a summary of the copied files and their source-destination directories.

    Args:
        copied_files_info (list): List of tuples containing the copied files' source
                                  and destination information.
        destination_folder (str): The path to the destination folder.

    Returns:
        None

    Raises:
        None
    """
    log_filename = os.path.join(
        os.path.dirname(destination_folder),
        f"incremental_copy_log_{os.path.basename(destination_folder)}_{time.strftime('%Y%m%d_%H%M%S')}.txt",
    )

    with open(log_filename, "w") as log_file:
        log_file.write("Incremental Copy Log\n")
        log_file.write(f"Date and Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        log_file.write("Copied Files:\n")
        for src_file, dest_file in copied_files_info:
            log_file.write(f"From: {src_file}\n")
            log_file.write(f"To: {dest_file}\n")
            log_file.write("\n")

    print(f"Log file '{log_filename}' generated.")


if __name__ == "__main__":
    source_folder = "/home/zaesh/Documents/temp"
    destination_folder = "/home/zaesh/Documents/temp2"

    incremental_copy(source_folder, destination_folder)
