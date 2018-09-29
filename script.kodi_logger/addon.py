import xbmcgui
import xbmcplugin
import xbmc
import time
if __name__ == '__main__':
    logfile = '/home/max/test.log'
    monitor = xbmc.Monitor()

    class MyPlayer(xbmc.Player):
        def write_Event_to_file(self, event):
            type = self.getTypePlaying()
            info_tag = self.getInfoTag()
            if type and type != 'other':
                title = info_tag.getTitle()
                filename = self.getPlayingFile()
            else:
                title = ''
                filename = ''
            with open('/home/max/test.log', 'a') as f:
                f.write('%d; ' % int(time.time()) + event + ';' + type + ';' +
                        title + ';' + filename + '\n')

        def getTypePlaying(self):
            if not self.isPlaying():
                return None
            if self.isPlayingVideo():
                return 'video'
            if self.isPlayingAudio():
                return 'audio'
            if self.isPlayingRDS():
                return 'rds'
            return 'other'

        def getInfoTag(self):
            type = self.getTypePlaying()
            if type == 'video':
                return self.getVideoInfoTag()
            elif type == 'audio':
                return self.getMusicInfoTag()
            elif type == 'rds':
                return self.getRDSInfoTag()

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
