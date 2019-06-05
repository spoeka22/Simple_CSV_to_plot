import os
from collections import OrderedDict
import shutil


folders = []
filenames = OrderedDict()

folder_path = r'C:\Users\annawi\Desktop\Projects\Propene oxidation\Experiments\201905_PdAufoams\XPS + ISS\ISS - before_after echem\ISS_as_prep'

filename_add = "_5sArsputter"

for root, subfolders, files in os.walk(folder_path):
# for root, subfolders, files in os.walk(r'C:\Users\annawi\Desktop\Projects\Propene oxidation\Experiments\201807_AuPd'):
# for root, subfolders, files in os.walk(r'C:\Users\annawi\Desktop\Projects\Propene oxidation\Thin films for EC-CP-MS'):

    if len(files)==0: continue
    foldername = root[root.rfind('\\')+1:]
    print(foldername)
    folders.append(foldername)
    files_this_folder = []
    # print(root)
    for filename in files:
        if False: #set false to only search for files in folder and no moving/renaming required
            if filename.endswith(".avg"):  #usually ".mpt"
                old_path = folder_path + '\\' + foldername + '\\' + filename
                new_path = folder_path + '\\' + foldername + '\\' + foldername+ filename_add + ".avg"
                os.rename(old_path, new_path)
                print("File renamed: " + new_path)
                copy_destination = folder_path[:folder_path.rfind('\\')]
                print(copy_destination)
                shutil.copy2(new_path, copy_destination)
                # print(root)
        if filename.endswith(".avg"):  #usually ".mpt"
            files_this_folder.append(filename)
            # print(root)
    filenames[foldername] = files_this_folder
    # filenames[root[-15:]] = files_this_folder


print(folders)

print(filenames)
