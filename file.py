import os

def check_file(input_dir, output_dir, release_version = True):
    file_list = []
    output_file_list = []
    files_removed = []
    input_dir = os.listdir(input_dir)
    output_dir = os.listdir(output_dir)

    for file_in in input_dir:
        if not file_in.startswith('.'):
            file_list.append(file_in)

    if release_version is True:
        print("\nChecking valid files...")
        for file_out in output_dir:
            if file_out.lower().endswith('.png'):
                output_file_list.append(file_out)

        # solving https://github.com/deeppomf/DeepCreamPy/issues/25
        # appending in list with reason as tuple (file name, reason)
        for lhs in file_list:
            lhs.lower()
            if not lhs.lower().endswith('.png') :
                files_removed.append((lhs, 0))
            for rhs in output_file_list:
                if(lhs == rhs):
                    files_removed.append((lhs, 1))

        # seperated detecting same file names and deleting file name list
        # just in case of index_error and show list of files which will not go though
        # decensor process
        print("\n＃＃＃ These files will not be decensored for following reason  ＃＃＃\n")

        error_messages(file_list, files_removed)
        input("\nPress anything to continue...")

        print("\n＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃\n")

    return file_list, files_removed

def error_messages(file_list, files_removed):
    if files_removed is None:
        return

    for remove_this, reason in files_removed:
        if file_list is not None:
            file_list.remove(remove_this)
        if reason == 0:
            print(" REMOVED : (" + str(remove_this) +")   is not PNG file format")
        elif reason == 1:
            print(" REMOVED : (" + str(remove_this) +")   already exists")
        elif reason == 2:
            print(" REMOVED : (" + str(remove_this) +")   file unreadable")
