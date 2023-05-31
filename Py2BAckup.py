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
        print "Source folder '%s' does not exist." % source_folder
        return

    # Ensure destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get the total number of files for progress calculation
    total_files = 0
    for root, dirs, files in os.walk(source_folder):
        total_files += len(files)

    # Initialize progress variables
    processed_files = 0
    copied_files = 0
    start_time = time.time()

    # List to store the copied files' information
    copied_files_info = []

    # Retrieve the last backup time if available
    last_backup_time = get_last_backup_time(destination_folder)

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

            # Copy the file if it's modified or doesn't exist in the destination or last backup time is earlier
            if not os.path.exists(dest_file) or (
                os.path.getmtime(src_file) > os.path.getmtime(dest_file)
            ) or last_backup_time is None or (
                os.path.getmtime(src_file) > last_backup_time
            ):
                shutil.copy2(src_file, dest_file)
                copied_files += 1

                # Add copied file's information to the list
                copied_files_info.append((src_file, dest_file))

            # Update progress variables
            processed_files += 1

            # Calculate progress percentage
            progress = float(processed_files) / total_files * 100

            # Calculate elapsed time
            elapsed_time = time.time() - start_time

            # Print progress information
            print "Progress: %.2f%% | Processed Files: %d/%d | Copied Files: %d | Elapsed Time: %.2fs" % (
                progress, processed_files, total_files, copied_files, elapsed_time),

    print "\nIncremental copy completed successfully. Total Files Copied: %d." % copied_files

    # Generate log file
    generate_log_file(copied_files_info, destination_folder)

    # Update the last backup time
    update_last_backup_time(destination_folder)


def get_last_backup_time(destination_folder):
    """
    Retrieve the last backup time from the destination folder.

    Args:
        destination_folder (str): The path to the destination folder.

    Returns:
        last_backup_time (float): The last backup time as a floating-point timestamp,
                                  or None if the last backup time file is not found.

    Raises:
        None
    """
    last_backup_file = os.path.join(destination_folder, "last_backup_time.txt")

    if os.path.exists(last_backup_file):
        with open(last_backup_file, "r") as f:
            last_backup_time = float(f.read().strip())
        return last_backup_time

    return None


def update_last_backup_time(destination_folder):
    """
    Update the last backup time in the destination folder.

    Args:
        destination_folder (str): The path to the destination folder.

    Returns:
        None

    Raises:
        None
    """
    last_backup_file = os.path.join(destination_folder, "last_backup_time.txt")
    current_time = time.time()

    with open(last_backup_file, "w") as f:
        f.write(str(current_time))


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
        "incremental_copy_log_%s_%s.txt" % (os.path.basename(destination_folder), time.strftime("%Y%m%d_%H%M%S")),
    )

    with open(log_filename, "w") as log_file:
        log_file.write("Incremental Copy Log\n")
        log_file.write("Date and Time: %s\n\n" % time.strftime("%Y-%m-%d %H:%M:%S"))

        log_file.write("Copied Files:\n")
        for src_file, dest_file in copied_files_info:
            log_file.write("From: %s\n" % src_file)
            log_file.write("To: %s\n" % dest_file)
            log_file.write("\n")

    print "Log file '%s' generated." % log_filename


if __name__ == "__main__":
    source_folder = "/path/to/source/folder"
    destination_folder = "/path/to/destination/folder"

    incremental_copy(source_folder, destination_folder)
