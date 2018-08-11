import hashlib
import os
import tkinter as tk

from tkinter import filedialog, StringVar

class duplicate_checker(tk.Frame):
    """duplicate """
    # global variables here
    folder = ''
    filestoremove = []
    defaultprefix = 'select prefix'
    prefixes = ['select prefix', '.jpg', '.png', '.mp4', '.mp3', '.pdf']

    def __init__(self):
        tk.Frame.__init__(self, master=None, height=200, width=400)
        self.grid_propagate(0)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """create widgets"""

        # select folder button
        self.folderButton = tk.Button(self, text='Select Directory', command=self.selectFolder)
        self.folderButton.grid(row=0, column=0)

        # remove duplicates button
        self.removeDuplicates = tk.Button(self, text='Remove Duplicates', command=lambda:self.detect_duplicates(self.folder))
        self.removeDuplicates.grid(row=2, column=0)

        # file prefix filter
        self.options = StringVar(master=self, value=self.prefixes)
        self.options.set(self.defaultprefix)
        self.prefixselection = tk.OptionMenu(self, self.options, *self.prefixes)
        self.prefixselection.grid(row=1, column=0)

        # quit button
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=3, column=0)

    def selectFolder(self):
        """Ask for a Directory"""
        self.folder = filedialog.askdirectory()
        self.showSelectedPath()

    def showSelectedPath(self):
        """Show selected folder as a string """
        self.selectedfolder = tk.Label(self, text=self.folder)
        self.selectedfolder.grid(row=0, column=1)

    def showAmountDelFiles(self):
        # show amount of duplicates are found
        self.showamount = tk.Label(self, text=str(len(self.filestoremove)) + ' Files removed.')
        self.showamount.grid(row=2, column=1)

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
                # file prefix filter default
                if self.options.get() == self.defaultprefix:
                    file_list.append(os.path.join(root, name))
                else:
                    if self.options.get() in os.path.join(root, name):
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
            open_file = open(file, 'br')
            # add filepath + md5checksum to dictionary
            file_chksum_dict[file] = self.md5_for_file(open_file)
            # close file
            open_file.close()

        return file_chksum_dict

    def detect_duplicates(self, path_to_check):
        """compare file checksums in 1 folder"""
        # 1. create file_listing
        print('1. create file_listing')
        file_list = self.file_listing(path_to_check)
        # 2. create dict with md5 chksum
        print('2. create dict with md5 chksum')
        file_md5_dict = self.file_and_chksum(file_list)
        # 3. check 4 duplicates
        print('3. check 4 duplicates')
        for x in file_md5_dict:
            for i in file_md5_dict:
                if file_md5_dict[x] == file_md5_dict[i] and i != x:
                    file_md5_dict[x] = ''
                    self.filestoremove.append(x)
        for file in self.filestoremove:
            os.remove(file)
        self.showAmountDelFiles()
        self.filestoremove = []

main = duplicate_checker()
main.master.title('Duplicate Checker by Raphael Aigner')
main.mainloop()