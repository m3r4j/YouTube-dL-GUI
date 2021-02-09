import pytube
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pyperclip
import threading
import re
import os
from pathlib import Path

# A boolean to tell the program that something is already in progress
downloading = False

# Regular expressions for the youtube link
linkRe = link_re = re.compile(r'(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?')


# Extra features #############################
def checkBut(opNum, form=False, amount=False):
    if amount:
        if opNum == 1:
            playlist.deselect()

        elif opNum == 2:
            singleVid.deselect()

    if form:
        if opNum == 1:
            mp4.deselect()

        elif opNum == 2:
            mp3.deselect()



def detectClipboard():
    while True:
        if linkRe.search(pyperclip.paste()):
            linkEntry.delete(0, END)
            linkEntry.insert(0, pyperclip.paste())
            pyperclip.copy('')



def detectClipboardThread():
    thread = threading.Thread(target=detectClipboard)
    thread.setDaemon(True)
    thread.start()


# Extra features #############################

# Download button which downloads the link with given options by the user
def download():
    global downloading
    
    if not linkRe.search(linkEntry.get()):
        messagebox.showerror('Error', 'Please input a valid youtube link to download')
        return
    
    elif option_single.get() == False and option_playlist.get() == False:
        messagebox.showerror('Error', 'Please select a single video or whole playlist')
        return

    elif option_mp3.get() == False and option_mp4.get() ==  False:
        messagebox.showerror('Error', 'Please select the file format (mp3 or mp4)')
        return


    # Ask the user where to save the file when pressing download
    curr_directory = os.getcwd()
    path = filedialog.askdirectory(initialdir = curr_directory)
    
    if os.path.exists(path):    
        os.chdir(path)

    else:
        return

    # Set downloading to true since everything has been checked
    downloading = True

    # Download the video in the given format by the user
    # MP4
    if option_mp4.get() == True:
        # Single video
        if option_single.get() == True:
            pytube.YouTube(linkEntry.get()).streams.get_highest_resolution().download()


        # Whole playlist
        else:
            playlistVids = pytube.Playlist(linkEntry.get())
            for videos in playlistVids.video_urls:
                pytube.YouTube(videos).streams.get_highest_resolution().download()

        
    # MP3
    else:
        # Single video
        if option_single.get() == True:
                video = pytube.YouTube(linkEntry.get())
                video = video.streams.filter(only_audio=True)
                video[0].download()
                paths = sorted(Path('.').iterdir(), key=lambda f: f.stat().st_mtime)
                origFile = str(paths[-1])
                newFile = str(paths[-1])
                index=(newFile.find('.mp4'))
                newFile = list(newFile)
                newFile[index + 3] = '3'
                newFile = ''.join(newFile)
                os.rename(origFile, newFile)

            

        # Whole playlist
        else:
            playlistVids = pytube.Playlist(linkEntry.get())
            for videos in playlistVids.video_urls:
                video = pytube.YouTube(videos)
                video = video.streams.filter(only_audio=True)
                video[0].download()
                paths = sorted(Path('.').iterdir(), key=lambda f: f.stat().st_mtime)
                origFile = str(paths[-1])
                newFile = str(paths[-1])
                index=(newFile.find('.mp4'))
                newFile = list(newFile)
                newFile[index + 3] = '3'
                newFile = ''.join(newFile)
                os.rename(origFile, newFile)


    
    # Show the message when finished
    messagebox.showinfo('Finished', 'The file has finished downloading')
    
    # Clear everything after finished downloading
    linkEntry.delete(0, END)

    if option_single.get() == True:
        singleVid.deselect()

    else:
        playlist.deselect()

    if option_mp3.get() == True:
        mp3.deselect()

    else:
        mp4.deselect()
        
    downloading = False
    return


# Start the download thread
def downloadThread():
    if downloading:
        messagebox.showinfo('Waiting', 'A download is already in progress')
        return
    
    thread = threading.Thread(target=download)
    thread.setDaemon(True)
    thread.start()

            
# Screen
root = Tk()

# Title
root.title('YouTube-dL')

# Screen Size
root.geometry('450x300')

# Unresizable
root.resizable(0,0)

# Background color
default_bg = '#%02x%02x%02x' % (240, 240, 237) # This is the default tkinter color in windows
root.configure(bg=default_bg)

# Link Label
linkLabel = Label(root, text='Link:', fg='blue', font=('bold', 15))
linkLabel.place(x=10, y=50)

# Link Entry
linkEntry = Entry(root, width=40, fg='purple', font=(None, 11))
linkEntry.place(x=70, y=56)


# CheckBox for one vid or more
option_single = BooleanVar()
option_playlist = BooleanVar()

singleVid = Checkbutton(root, text='Single Video', variable=option_single, command=lambda: checkBut(1, amount=True))
singleVid.place(x=70, y=100)

playlist = Checkbutton(root, text='Whole Playlist', variable=option_playlist, command=lambda: checkBut(2, amount=True))
playlist.place(x=70, y=120)

# Checkbox for formats
option_mp3 = BooleanVar()
option_mp4 = BooleanVar()

mp3 = Checkbutton(root, text='.mp3', variable=option_mp3, command=lambda: checkBut(1, form=True))
mp3.place(x=70, y=160)

mp4 = Checkbutton(root, text='.mp4', variable=option_mp4, command=lambda: checkBut(2, form=True))
mp4.place(x=70, y=180)

# Download button
downloadButton = Button(root, text='Download', fg='blue', command=downloadThread)
downloadButton.place(x=70, y=215)

# Threads
detectClipboardThread()

# Mainloop
root.mainloop()
