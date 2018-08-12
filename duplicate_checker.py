import hashlib
import os
import tkinter as tk
import threading

from tkinter import filedialog, StringVar, END


class duplicate_checker(tk.Frame):
    """duplicate """
    # global variables here
    folder = ''
    filestoremove = []
    defaultprefix = 'select prefix'
    prefixes = ['select prefix', '.jpg', '.png', '.mp4', '.mp3', '.pdf']

    def __init__(self):
        tk.Frame.__init__(self, master=None, height=400, width=400)
        self.grid_propagate(0)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """create widgets for the ui """
        # select folder button
        self.folderButton = tk.Button(
            self, text='Select Directory', command=self.selectFolder
        )
        self.folderButton.grid()

        # file prefix filter
        self.options = StringVar(master=self, value=self.prefixes)
        self.options.set(self.defaultprefix)
        self.prefixselection = tk.OptionMenu(
            self, self.options, *self.prefixes
        )
        self.prefixselection.grid()

        # find duplicates button
        self.findDuplicates = tk.Button(
            self, text='Find Duplicates',
            command=lambda: self.detect_duplicates(self.folder)
        )
        self.findDuplicates.grid()

        # Listing of duplicates
        self.listbox = tk.Listbox(self)
        self.listbox.grid()

        # remove duplicates button
        self.removeDuplicates = tk.Button(
            self, text='Remove Duplicates',
            command=lambda: self.remove_duplicates()
        )
        self.removeDuplicates.grid()

        # quit button
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

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
        self.showamount = tk.Label(
            self, text=str(len(self.filestoremove)) + ' Files removed.'
        )
        self.showamount.grid(row=4, column=1)

    def setDuplicatesFound(self, duplicatesfound):
        """Show how many duplicates are found"""
        self.selectedfolder = tk.Label(self, text=str(duplicatesfound))
        self.selectedfolder.grid()

    def setprogress(self, message):
        try:
            self.progress.destroy()
        except AttributeError:
            pass
        self.progress = tk.Label(self, text=message)
        self.progress.grid(row=2, column=1)

    def fill_listing(self):
        """fill the list with duplicates"""
        self.listbox.delete(0, END)
        for path in self.filestoremove:
            self.listbox.insert(END, path)

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
        """create a dict with filename:checksum of the files in (1folder)"""

        file_chksum_dict = dict()
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
        # show progress
        print('1. create file_listing')
        file_list = self.file_listing(path_to_check)
        # 2. create dict with md5 chksum
        pause.seconds(10)
        print('2. create dict with md5 chksum')
        file_md5_dict = self.file_and_chksum(file_list)
        # 3. check 4 duplicates
        print('3. check 4 duplicates')
        for x in file_md5_dict:
            for i in file_md5_dict:
                if file_md5_dict[x] == file_md5_dict[i] and i != x:
                    file_md5_dict[x] = ''
                    self.filestoremove.append(x)
        self.fill_listing()

    def remove_duplicates(self):
        """remove all files in the list"""
        self.setprogress('Removing Duplicates')
        for file in self.filestoremove:
            os.remove(file)
        self.showAmountDelFiles()
        self.filestoremove = []


main = duplicate_checker()
main.master.title('Duplicate Checker by Raphael Aigner')
main.mainloop()
