#-*- coding: UTF-8 -*-

import sys,os,time,re,datetime
#import grp,pwd

class FileServer:
    _basedir = None
    _savedir = None
    _time_setp = 120
    
    def __init__(self, base_dir, save_dir, time_setp):
        self._basedir = base_dir
        self._savedir = save_dir
        self._time_setp = time_setp
        
    def listDir(self, dirname=None):
        if dirname is None:
            dirname = self._basedir
        try:
            dirs = os.listdir(dirname)
            tmp = []
            for ds in dirs:
                if not re.findall("^\.", ds):   #排除以点开头的文件
                    tmp.append(ds)
            for i in range(0, len(tmp)):
                path = os.path.join(dirname, tmp[i])
                if os.path.isfile(path):
                    finfo = os.stat(path)
                    if(time.time() - finfo.st_mtime < self._time_setp):
                        #uid = finfo.st_uid
                        #user = pwd.getpwuid(uid)[0]
                        user = ""
                        #gid = finfo.st_gid
                        #group = grp.getgrgid(gid)[0]
                        editime = datetime.datetime.fromtimestamp(finfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        f = editime + "&nbsp;&nbsp;"+ user +"&nbsp;&nbsp;" + path
                        self.writeHTML(f)
                        #sys.exit()
                if os.path.isdir(path):
                    self.listDir(path)
                    
        except IOError, e:
            print e
    
    def writeHTML(self, content):
        content = content.replace(self._basedir,"")
        dirs = self._savedir + time.strftime('%Y-%m',time.localtime(time.time())) + "/"

        if not os.path.isdir(dirs):
            os.makedirs(dirs)
        op_file = dirs + time.strftime('%d',time.localtime(time.time()))+".html"
        if not os.path.exists(op_file):
            open(op_file, 'a').close()
            
        fr = open(op_file, 'r')
        rf = fr.read()
        fr.close()
        #fa = open(op_file, 'a')
        fw = open(op_file, 'w')
        content = content + rf
        fw.write("<br> \n" + content)
        fw.close()
   
if __name__=='__main__':
    fs = FileServer("/home/ptp/", "/home/www/FileServer/", 60)  #要监控的目录,HTML 保存的目录,定期运行的时间（秒）
    fs.listDir()

