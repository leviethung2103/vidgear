import vlc 
import pafy 
import time


youtube_url = 'https://www.youtube.com/watch?v=C3Am8d2Fgro'

source_object = pafy.new(youtube_url)
vo_source = source_object.getbest()
playurl = vo_source.url 


instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(playurl)
media.get_mrl()
player.set_media(media)
player.play()
time.sleep(10)


# p = vlc.MediaPlayer('/home/hunglv/Downloads/IMG_8442.MOV')
# p.play()
# time.sleep(10)