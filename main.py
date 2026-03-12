import tkinter as tk
from iiif_downloader.ui import IIIFDownloaderUI

if __name__ == "__main__":
    root = tk.Tk()
    app = IIIFDownloaderUI(root)
    app.run()