#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
import logging.config
import subprocess
import threading

UnLinkCrash = False

class GatherLog(threading.Thread):

    def __init__(self):
        super(GatherLog, self).__init__()

    def run(self):#定义每个线程要运行的函数
        global UnLinkCrash
        L = logging.getLogger('adblog')
        cmd = 'pidcat com.dingogames.tastyplanet4'
        p = subprocess.Popen(cmd, close_fds=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        line = ''
        while p.poll() is None:
            out = p.stdout.read(1)
            if out=='\n':
                if 'UnsatisfiedLinkError' in line:
                    UnLinkCrash = True
                L.info(line)
                line = ''
            else:
                line = line + out

class LaunchTest(object):

    def __init__(self, params):
        logging.config.fileConfig('./logger.cfg')
        self.l = logging.getLogger('log1')
        self.params = params

    def run(self):
        logging.debug('>>>>>> Launch Test Begin')
        gatherThread = GatherLog()
        gatherThread.setDaemon(True)
        gatherThread.start()

        launchCmd = 'adb shell am start -n {0}/{1}'.format(self.params['packageID'], self.params['activity'])
        stopCmd = 'adb shell am force-stop {0}'.format(self.params['packageID'])
        counter = 1
        while True:
            logging.debug('Launch Times:{0}'.format(counter))
            self.runCmd(launchCmd)
            counter += 1
            self.sleep(self.params['spaceSecond'])
            self.runCmd(stopCmd)
            self.sleep(1)

            if UnLinkCrash:
                logging.warn('======== Find Crash ==========')
                break
            if counter > self.params['times']:
                break
        logging.debug('Total launch times:{0}'.format(counter - 1))
        logging.debug('<<<<<< Launch Test End')

    def runCmd(self, cmd):
        p = subprocess.Popen(cmd, close_fds=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        line = ''
        while p.poll() is None:
            out = p.stdout.read(1)
            if out=='\n':
                logging.info(line)
                line = ''
            else:
                line = line + out
        logging.info('runCmd retCode:{0}'.format(p.returncode))

    def sleep(self, second):
        time.sleep(second)


def main():
    params = {
        'packageID': 'com.dingogames.tastyplanet4',
        'activity': 'org.cocos2dx.cpp.AppActivity',
        'times': 3,
        'spaceSecond': 10
    }

    # make sure log folder exist
    if not os.path.exists('log'):
        os.mkdir('log')

    test = LaunchTest(params)
    test.run()

if __name__ == '__main__':
    main()
