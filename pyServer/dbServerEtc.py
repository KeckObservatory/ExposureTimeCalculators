import sys
import json
import socketserver
import socket
import math
import io
import matplotlib.pyplot as plt
from easyHTTP import EasyHTTPHandler, EasyHTTPServer, EasyHTTPServerThreaded


import EtcApi
import TestApi


Globals = {}

class TestAppHandler (EasyHTTPHandler):
    def echo (self, req, qstr):
        return self.response (json.dumps(qstr), self.PlainTextType)

    def callme (self, req, qstr):
        return self.response("called me", self.HTMLType)

    def get (self, req, qstr):
        global Globals
        return self.response(json.dumps(Globals), self.PlainTextType)
    
    def set (self, req, qstr):
        global Globals
        Globals.update (qstr)
        return self.response("done", self.HTMLType)

    def fileupload(self, req, qstr):
        return self.response(qstr['content'][0], self.PlainTextType)

    def echoJpeg(self, req, qstr):
        imgContent = qstr.get('imgcontent')
        if not imgContent:
            return None, ""

        imgData = imgContent[0]
        return self.response(imgData, "image/jpeg")

    def getResult(self, req, qstr):
        paramA = self.floatVal(qstr, 'paramA', 1)
        paramB = self.floatVal(qstr, 'paramB', 1)
        result = {'result': (paramA + paramB) }
        return self.response(json.dumps(result), self.PlainTextType)

    def getImage(self, req, qstr):
        fig = plt.figure(figsize=(4,4))
        length, freq = self.intVal(qstr, 'paramL', 1), self.floatVal(qstr, 'paramF', 1)
        xdata = range(length * 100)
        data = [ math.sin(freq*x/50*math.pi) for x in xdata ]
        plt.plot (xdata, data, 'r-')
        imgData = io.BytesIO()
        fig.savefig(imgData, format='png')
        plt.close(fig)
        imgData.seek(0);
        buf = imgData.read()
        return self.response(buf, 'image/png')



    # -------------------- DEFINE YOUR APIs BELOW-------------------------


    def NIRC2EtcApi(self, req, qstr):

        #create api object
        api = EtcApi.EtcApi()

        #get command
        cmd = self.getDefValue(qstr, 'cmd', None)
        if cmd == None: return self.response(api.show_usage(), self.HTMLType)

        #assign default values from URL parameters
        api.output      = self.getDefValue(qstr, 'output',      'txt')
        api.instr       = self.getDefValue(qstr, 'instr',       None)

        #---NIRC2 specific inputs---
        api.magnitude   = self.getDefValue(qstr, 'magnitude',   None)
        api.strehl      = self.getDefValue(qstr, 'strehl',      None)
        api.exp_time    = self.getDefValue(qstr, 'exp_time',    None)
        api.coadds      = self.getDefValue(qstr, 'coadds',      None)
        api.num_dith    = self.getDefValue(qstr, 'num_dith',    None)
        api.num_repeats = self.getDefValue(qstr, 'num_repeats', None)
        api.camera      = self.getDefValue(qstr, 'camera',      None)
        api.img_filter  = self.getDefValue(qstr, 'img_filter',  None)
        api.num_read    = self.getDefValue(qstr, 'num_read',    None)
        api.x_extent    = self.getDefValue(qstr, 'x_extent',    None)
        api.y_extent    = self.getDefValue(qstr, 'y_extent',    None)
        api.ao_mode     = self.getDefValue(qstr, 'ao_mode',     None)
        api.laser_dith  = self.getDefValue(qstr, 'laser_dith',  None)


        # Call the api method and send return contents to browser
        cmdToCall = getattr(api, cmd)
        result = cmdToCall()
        if api.output == 'txt' or api.output == 'html':
            return self.response(result, self.HTMLType)
        else:
            return self.response(json.dumps(result), self.PlainTextType)

    def NIRESEtcApi(self, req, qstr):

        #create api object
        api = EtcApi.EtcApi()

        #get command
        cmd = self.getDefValue(qstr, 'cmd', None)
        if cmd == None: return self.response(api.show_usage(), self.HTMLType)

        #assign default values from URL parameters
        api.output      = self.getDefValue(qstr, 'output',      'txt')
        api.instr       = self.getDefValue(qstr, 'instr',       None)

        #---NIRC2 specific inputs---
        api.mag_src   = self.getDefValue(qstr, 'mag_src',   None)
        api.exp_time    = self.getDefValue(qstr, 'exp_time',    None)
        api.coadds      = self.getDefValue(qstr, 'coadds',      None)
        api.dither    = self.getDefValue(qstr, 'dither',    None)
        api.dith_repeats = self.getDefValue(qstr, 'dith_repeats', None)
        api.num_read    = self.getDefValue(qstr, 'num_read',    None)
        api.seeing      = self.getDefValue(qstr, 'seeing', None)
        api.water_vap_col = self.getDefValue(qstr, 'water_vap_col', None)


        # Call the api method and send return contents to browser
        cmdToCall = getattr(api, cmd)
        result = cmdToCall()
        if api.output == 'txt' or api.output == 'html':
            return self.response(result, self.HTMLType)
        else:
            return self.response(json.dumps(result), self.PlainTextType)

    def TestApi(self, req, qstr):

        #create api object
        api = TestApi.TestApi()

        #get command
        cmd = self.getDefValue(qstr, 'cmd', None)
        if cmd == None: return self.response(api.show_usage(), self.HTMLType)

        #assign default values from URL parameters
        api.output      = self.getDefValue(qstr, 'output',      'txt')
        api.instr       = self.getDefValue(qstr, 'instr',       None)
        api.magnitude   = self.getDefValue(qstr, 'magnitude',   None)
        api.coadds      = self.getDefValue(qstr, 'coadds',      None)

        # Call the api method and send return contents to browser
        cmdToCall = getattr(api, cmd)
        print (cmdToCall)
        result = cmdToCall()
        if api.output == 'txt' or api.output == 'html':
            return self.response(result, self.HTMLType)
        else:
            return self.response(json.dumps(result), self.PlainTextType)



if __name__ == "__main__":
    import signal
    import os

    def terminate(signum, frame):
        print ("SIGINT, terminated")
        os._exit(os.EX_OK)

    signal.signal (signal.SIGINT, terminate)
    try:
        port = int(sys.argv[1])
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print ("HTTPD server started", hostname, ip, port)

        TestAppHandler.DocRoot = "docs"
        TestAppHandler.logEnabled = True
        ts = EasyHTTPServer (('', port), TestAppHandler)
        ts.run4ever()
    except Exception as e:
        print (e)

