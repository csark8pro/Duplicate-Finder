import hashlib
import os
import tkinter as tk
import pdb

from tkinter import filedialog

class duplicate_checker(tk.Frame):
    """duplicate """
    # global variables here
    folder = ''
    duplicates = 0

    def __init__(self):
        tk.Frame.__init__(self, master=None, height=600, width=800,)
        self.grid_propagate(0)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """create widgets"""
        # label pic
        # self.brand_label = tk.Label(self, image=ImageTk.PhotoImage(Image.open('brand.jpg')))
        # self.brand_label.grid()

        # select folder button
        self.folderButton = tk.Button(self, text="Select Directory", command=self.selectFolder)
        self.folderButton.grid(row=0, column=0)

        # remove duplicates button
        self.removeDuplicates = tk.Button(self, text="Remove Duplicates", command=lambda:self.detect_duplicates(self.folder))
        self.removeDuplicates.grid(row=1, column=0)

        # quit button
        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(row=3, column=0)

    def selectFolder(self):
        """Ask for a Directory"""
        self.folder = filedialog.askdirectory()
        self.setFolderPath(self.folder)

    def setFolderPath(self,folderpath):
        """Show selected folder as a string """
        self.selectedfolder = tk.Label(self, text=folderpath)
        self.selectedfolder.grid(row=0, column=1)

    def setDuplicatesFound(self,duplicatesfound):
        """Show how many duplicates are found"""
        self.selectedfolder = tk.Label(self, text=str(duplicatesfound))
        self.selectedfolder.grid(row=1, column=1)

    def file_listing(self, path):
        """create a listing of all files in the given path"""
        # file listing
        file_list = []

        # walk through all folders and add files to the list
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_list.append(os.path.join(root, name))

        return file_list

    def md5_for_file(self, f, block_size=2 ** 20):
        """create md5 checksum for a file"""
        md5 = hashlib.md5()

        while True:
            data = f.read(block_size)
            if not data:
                break

            md5.update(data)
        return md5.digest()

    def file_and_chksum(self, file_list):
        """create a dictionary with filename:checksum of the files in (1folder)"""
        # create empty dict
        file_chksum_dict = {}

        for file in file_list:
            # open file in binary mode
            open_file = open(file, "br")
            # add filepath + md5checksum to dictionary
            file_chksum_dict[file] = self.md5_for_file(open_file)
            # close file
            open_file.close()

        return file_chksum_dict

    def detect_duplicates(self, path_to_check):
        """compare file checksums in 1 folder"""
        # 1. create file_listing
        print("1. create file_listing")
        file_list = self.file_listing(path_to_check)
        # 2. create dict with md5 chksum
        print("2. create dict with md5 chksum")
        file_md5_dict = self.file_and_chksum(file_list)
        # 3. check 4 duplicates
        print("3. check 4 duplicates")
        for x in file_md5_dict:
            for i in file_md5_dict:
                if file_md5_dict[x] == file_md5_dict[i] and i != x:
                    # set a empty tag to remove the file
                    file_md5_dict[i] = ''

        for file in file_md5_dict:
            if file_md5_dict[file]:
                pass
            else:
                os.remove(file)

main = duplicate_checker()
main.master.title("Duplicate Checker by Raphael Aigner")
main.mainloop()