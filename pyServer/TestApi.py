import json

class TestApi(object):

    def show_usage(self, func=None, instr=None):

        if (func == 'getExposureData'):

            if (instr == 'NIRC2'):
                str =  'EtcApi?cmd=getExposureData&instr=NIRC2'
                str += '<p>'
                str += '<li>&magnitude=[mag]</li>'
                return str

            else:
                str =  'EtcApi?cmd=getExposureData&instr='
                str += '<p>'
                str += '<li>NIRC2</li>'
                str += '<li>HIRES</li>'
                return str

        else:
            str =  'EtcApi?cmd='
            str += '<p>'
            str += '<li>getExposureData</li>'
            return str



    def getExposureData(self):

        print ('getExposureData')

        #check for instrument input
        if (self.instr == None):
            if (self.output == 'json'): return None
            else                      : return self.show_usage('getExposureData')

        #call instrument specific calc and return data
        data = None
        instr = self.instr.upper()
        print (instr)
        if   (instr == 'NIRC2'): data = self.getExposureData_NIRC2()
        elif (instr == 'HIRES'): data = self.getExposureData_HIRES()
        return data


    def getExposureData_NIRC2(self):

        print ('getExposureData_NIRC2')

        #todo: check required inputs, else return usage
        #todo: return error object for client with error reason?
        if self.magnitude == None :
            if (self.output == 'json') : return None
            else                       : return self.show_usage('getExposureData', self.instr)


        #call core calculation function
        import etc_nirc2_test
        data = etc_nirc2_test.do_calc(magnitude = float(self.magnitude))

        #return data
        self.output = 'json'
        return data

