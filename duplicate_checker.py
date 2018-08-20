import hashlib
import os
import tkinter as tk
from tkinter import END, Checkbutton, IntVar, Scrollbar, StringVar, filedialog

import send2trash


class duplicate_checker(tk.Frame):
    """duplicate """
    # global variables here
    folder = ''
    filestoremove = []
    defaultprefix = 'select prefix'
    prefixes = ['select prefix', '.jpg', '.png', '.mp4', '.mp3', '.pdf']

    def __init__(self):
        tk.Frame.__init__(self, master=None, height=320, width=800)
        self.grid_propagate(0)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """create widgets for the ui """
        # select folder button
        self.folderButton = tk.Button(
            self, text='Select Directory', command=self.selectFolder
        ).grid()

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
        self.findDuplicates.grid(row=3, column=0)

        # Listing of duplicates
        self.listbox = tk.Listbox(self)
        self.listbox.config(width=50)
        self.listbox.grid(row=3, column=1)

        # remove duplicates button
        self.removeDuplicates = tk.Button(
            self, text='Remove Duplicates',
            command=lambda: self.remove_duplicates()
        )
        self.removeDuplicates.grid(row=4, column=0)

        # move files to trash checkbox
        self.var = IntVar()
        self.filestotrash = Checkbutton(
            self, text='Move to Trash',
            variable=self.var, onvalue=1,
            offvalue=0,
        )
        self.filestotrash.grid(row=4, column=1)

        # remove empty dirs button
        self.delemptyfolders = tk.Button(
            self,
            text='Remove empty directories',
            command=lambda: self.rem_empty_dirs(self.folder),
        )
        self.delemptyfolders.grid(row=5, column=0)

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

    def showamountduplicates(self, bytes=0, filesfound=0):
        """show amount and size of duplicates are found"""
        if bytes:
            if bytes > 1024 * 1024 * 1024:
                savedsize = str(round(bytes / 1024 / 1024 / 1024, 2)) + ' GB'
            else:
                savedsize = str(round(bytes / 1024 / 1024, 2)) + ' MB'
        else:
            savedsize = '0 MB'
        self.amountduplicates = tk.Label(
            self,
            text=str(filesfound) + ' Duplicates Found. ' + savedsize,
        )
        self.amountduplicates.grid(row=2, column=1)

    def showAmountDelFiles(self):
        """show how many files are removed"""
        self.showamount = tk.Label(
            self, text=str(len(self.filestoremove)) + ' Files removed.'
        )
        self.showamount.grid(row=4, column=2)

    def showAmountDelDirs(self, deldir=0):
        """show how many directories are removed"""
        self.showamount = tk.Label(
            self, text=str(deldir) + ' Directories removed.'
        )
        self.showamount.grid(row=4, column=2)

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

    def rem_empty_dirs(self, path):
        """remove empty dirs """
        dirsremoved = 0
        for dirpath, dirnames, filenames in os.walk(path, topdown=False):
            if not dirnames and not filenames:
                os.rmdir(dirpath)
                dirsremoved += 1
        self.showAmountDelDirs(dirsremoved)

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
        self.filestoremove = []
        duplicate_byte_size = 0
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
                    duplicate_byte_size += os.stat(x).st_size
                    self.filestoremove.append(x)
        self.showamountduplicates(duplicate_byte_size, len(self.filestoremove))
        self.fill_listing()

    def remove_duplicates(self):
        """remove all files in the list"""
        self.setprogress('Removing Duplicates')
        if self.var.get():
            for file in self.filestoremove:
                send2trash.send2trash(file)
        else:
            for file in self.filestoremove:
                os.remove(file)

        self.showAmountDelFiles()
        self.filestoremove = []


main = duplicate_checker()
main.master.title('Duplicate Checker by Raphael Aigner')
main.mainloop()
