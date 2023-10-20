from flask import Flask, request, send_from_directory, jsonify, render_template
import os
from stats import *

# Change files directory according to your files folder
FILES_DIR = "./files"

# Load Flask app
app = Flask(__name__)


# Default landing page. Used for file upload only.
@app.route('/')
def main():
    return render_template("index.html")


# Upload function
@app.route("/upload", methods=["POST"])
def upload_files():

    # Get the list of files from webpage
    files = request.files.getlist("file")

    try:
        # Iterate for each file in the files List, and Save them
        for file in files:
            file.save(os.path.join(FILES_DIR, file.filename))
        return "<h1>Files Uploaded Successfully.!</h1>"
    except Exception as e:
        print(e)
        return "<h1>Files Upload Failed!</h1>"


# File download function
@app.route("/download/<string:file_name>", methods=["GET"])
def download_file(file_name):
    try:
        return send_from_directory(FILES_DIR, file_name)
    except Exception as e:
        print(e)
        return "The file you wanted to download does not exist."


# File delete function
@app.route("/delete/<string:file_name>", methods=["GET"])
def delete_files(file_name):

    print(file_name)

    try:
        path = os.path.join(FILES_DIR, file_name)
        os.remove(path)
        return "Deleted successfully."
    except Exception as e:
        print(e)
        return "The file you wanted to delete does not exist."


# ------------ Listing and sorting function ---------------
# The following sort selectors are implemented
#   - file name (default)
#   - file type
#   - file size
#   - file upload time
#   - file modification time
# Ascending and Descending ordering is also implemented
# ---------------------------------------------------------
@app.route("/list", methods=["GET"])
def list_files():

    # get query strings
    sort_type = request.args.get('sort')
    order = request.args.get('order')

    # Establish order (either ascending by default or descending by query string choice)
    reverse = True if order == "desc" else False

    # Sort all files in the folder
    file_list = sorted(os.listdir(FILES_DIR), key=lambda v: v.lower(), reverse=reverse)

    # If "type" file sort is requested in the query string return files sorted by type as a json object
    if sort_type == 'type':

        file_dict = {}

        for file in file_list:
            name, extension = os.path.splitext(file)
            if extension not in file_dict.keys():
                file_dict[extension] = []
            file_dict[extension].append(name)

        return jsonify(file_dict)

    # If "size" file sort is requested in the query string return file list sorted by size
    elif sort_type == 'size':
        size_sorted_files = sorted(file_list, key=lambda x: os.stat(os.path.join(FILES_DIR, x)).st_size,
                                   reverse=reverse)
        return size_sorted_files

    # If "upload_time" is requested in the query string return file list sorted by time it was uploaded
    elif sort_type == 'upload_time':
        # This is where my assumptions about creation time and upload time were mistaken
        # A better approach would have been to use a database and store the upload time there.
        # That is because once the file is saved to hard drive it overrides the original uploaded files metadata and
        # creation time changes to the time it was saved.
        # Therefore: ---->
        # Upload time can also be considered creation time
        upload_sorted_files = sorted(file_list, key=lambda x: os.path.getctime(os.path.join(FILES_DIR, x)),
                                     reverse=reverse)
        return upload_sorted_files

    # The original instructions were to apply a sort by creation time as distinct from upload time. Unfortunately,
    # due to the reasons stated above, my approach destroyed that information at the time of upload (as I do not use
    # a database in my solution.
    # Therefore: ---->
    # I decided to use time of file modification as a sorting option instead.
    elif sort_type == 'modification_time':
        modification_sorted_files = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(FILES_DIR, x)),
                                           reverse=reverse)
        return modification_sorted_files

    # Default output is a list of file names
    return file_list


# Return file statistics (total size, average size, median size, file count
@app.route("/stats", methods=["GET"])
def get_stats():

    total_file_size = 0  # Measured in bytes (sum of all output from os.path.getsize())
    total_num_files = 0
    file_sizes = []

    # go through each file only once
    for filename in os.listdir(FILES_DIR):
        f = os.path.join(FILES_DIR, filename)

        # checking if it is a file
        if os.path.isfile(f):
            total_file_size += os.path.getsize(f)
            total_num_files += 1
            file_sizes.append(os.path.getsize(f))

    output = [
        f"Total size of files stored: {convert_size(total_file_size)}",
        f"Average file size is: {convert_size(total_file_size / total_num_files)}",
        f"Median file size is: {convert_size(get_median(file_sizes))}",
        f"Total number of files is: {total_num_files}",
    ]

    return output


# Return a list of all file extensions that are present in the file folder
@app.route("/extensions", methods=["GET"])
def get_extensions():

    all_extensions = []

    for filename in os.listdir(FILES_DIR):
        f = os.path.join(FILES_DIR, filename)

        # checking if it is a file
        if os.path.isfile(f):
            split_name = os.path.splitext(f)
            if split_name[1] not in all_extensions:
                all_extensions.append(split_name[1])

    return all_extensions


if __name__ == "__main__":
    app.run(debug=True)
