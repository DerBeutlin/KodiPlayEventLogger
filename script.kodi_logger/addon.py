import xbmc
import time
import xbmcaddon
import os
if __name__ == '__main__':
    monitor = xbmc.Monitor()
    addon = xbmcaddon.Addon()

    def getLogFilePath(type_playing):
        folder = addon.getSetting('log_folder')
        filename = addon.getSetting('%s_filename' % type_playing)
        if not os.path.isdir(folder):
            return False
        return os.path.join(folder, filename)

    class MyPlayer(xbmc.Player):
        def write_Event_to_file(self, event):
            type_playing = self.getTypePlaying()
            info_tag = self.getInfoTag()
            if not type_playing:
                return None
            info = [
                str(int(time.time())), event,
                str(int(self.getTime())),
                str(int(self.getTotalTime())),
                self.getPlayingFile(),
                info_tag.getTitle()
            ]
            if type_playing == 'audio':
                info.append(info_tag.getArtist())
                info.append(info_tag.getAlbum())
            elif type_playing == 'video':
                info.append(info_tag.getMediaType())
                info.append(info_tag.getTVShowTitle())
                info.append(str(info_tag.getSeason()))
                info.append(str(info_tag.getEpisode()))
            path = getLogFilePath(type_playing)
            if path:
                with open(path, 'a') as f:
                    string = ';'.join(info)
                    string += ';\n'
                    f.write(string)

        def getTypePlaying(self):
            if not self.isPlaying():
                return None
            if self.isPlayingVideo():
                return 'video'
            if self.isPlayingAudio():
                return 'audio'
            return None

        def getInfoTag(self):
            type_playing = self.getTypePlaying()
            if type_playing == 'video':
                return self.getVideoInfoTag()
            elif type_playing == 'audio':
                return self.getMusicInfoTag()

        def onPlayBackStopped(self):
            self.write_Event_to_file('stopped')

        def onPlayBackPaused(self):
            self.write_Event_to_file('paused')

        def onPlayBackResumed(self):
            self.write_Event_to_file('resumed')

        def onPlayBackStarted(self):
            self.write_Event_to_file('started')

    player = MyPlayer()

    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
        time.sleep(1)
