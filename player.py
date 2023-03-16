import os
import vlc
import tkinter as tk
from tkinter import filedialog

class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Reproductor de videos en cadena")
        self.player = None
        self.list_player = None
        self.videos = []
        
        # Configurar la interfaz de usuario
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.select_button = tk.Button(self.frame, text="Seleccionar carpeta", command=self.select_folder)
        self.select_button.pack(side=tk.LEFT)
        
        self.play_button = tk.Button(self.frame, text="Reproducir", command=self.play_videos)
        self.play_button.pack(side=tk.LEFT)
        
        self.pause_button = tk.Button(self.frame, text="Pausar", command=self.pause_videos, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT)
        
        self.exit_button = tk.Button(self.frame, text="Salir de pantalla completa", command=self.exit_fullscreen, state=tk.DISABLED)
        self.exit_button.pack(side=tk.LEFT)
        
    def select_folder(self):
        folder = filedialog.askdirectory()
        self.videos = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp4")]
        
    def play_videos(self):
        if len(self.videos) == 0:
            return
        
        # Crear una instancia del reproductor de VLC
        self.player = vlc.Instance("--no-xlib")
        media_list = self.player.media_list_new()
        
        # Agregar los videos a la lista de reproducción
        for video in self.videos:
            media = self.player.media_new(video)
            media_list.add_media(media)
        
        # Reproducir los videos en cadena
        player = self.player.media_player_new()
        player.set_fullscreen(True)
        
        self.list_player = self.player.media_list_player_new()
        self.list_player.set_media_list(media_list)
        self.list_player.set_media_player(player)



        self.list_player.play()
        
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)
        
    def pause_videos(self):
        if self.list_player.is_playing():
            self.list_player.pause()
            self.pause_button.config(text="Reanudar")
        else:
            self.list_player.play()
            self.pause_button.config(text="Pausar")
        
    def exit_fullscreen(self):
        if self.list_player.get_media_player().get_fullscreen():
            self.list_player.get_media_player().set_fullscreen(False)
            self.exit_button.config(text="Ir a pantalla completa")
        else:
            self.list_player.get_media_player().set_fullscreen(True)
            self.exit_button.config(text="Salir de pantalla completa")
        
root = tk.Tk()
app = VideoPlayer(root)
root.mainloop()
