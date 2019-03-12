import json

class EtcApi(object):

    def show_usage(self, func=None, instr=None):

        if (func == 'getExposureData'):

            if (instr == 'NIRES'):
                str =  'EtcApi?cmd=getExposureData&instr=NIRES'
                str += '<p>'
                str += '<li>&magnitude=[mag_src]</li>'
                str += '<li>&coadds=[coadds]</li>'
                str += '<li>&exposure time=[exp_time]</li>'
                str += '<li>&dither pattern=[dither]</li>'
                str += '<li>&dither repeat=[dith_repeats]</li>'
                str += '<li>&observation wavelength=[obs_wave]</li>'
                return str

            elif (instr == 'NIRC2'):
                str = 'EtcApi?cmd=getExposureData&instr=NIRC2'
                str += '<p>'
                str += '<li>&magnitude=[mag]</li>'
                str += '<li>&coadds=[coadds]</li>'
                return str

            else:
                str =  'EtcApi?cmd=getExposureData&instr='
                str += '<p>'
                str += '<li>NIRES</li>'
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
        if   (instr == 'NIRC2'): data = self.getExposureData_NIRC2()
        elif (instr == 'NIRES'): data = self.getExposureData_NIRES()
        elif (instr == 'HIRES'): data = self.getExposureData_HIRES()
        return data


    def getExposureData_NIRC2(self):

        print ('getExposureData_NIRC2')

        #todo: check required inputs, else return usage
        #todo: return error object for client with error reason?
        if self.magnitude == None or self.coadds == None:
            if (self.output == 'json') : return None
            else                       : return self.show_usage('getExposureData', self.instr)


        #call core calculation function
        import etc_nirc2
        data = etc_nirc2.do_calc(   magnitude   = float(self.magnitude),
                                    strehl      = float(self.strehl),  
                                    exp_time    = float(self.exp_time),  
                                    coadds      = int(self.coadds), 
                                    num_dith    = int(self.num_dith),  
                                    num_repeats = int(self.num_repeats),  
                                    x_extent    = int(self.x_extent), 
                                    y_extent    = int(self.y_extent), 
                                    camera      = self.camera, 
                                    img_filter  = self.img_filter, 
                                    num_read    = int(self.num_read), 
                                    ao_mode     = int(self.ao_mode),  
                                    laser_dith  = int(self.laser_dith)
                                )

        #return data
        self.output = 'json'
        return data

    def getExposureData_NIRES(self):

        print ('getExposureData_NIRES')

        #todo: check required inputs, else return usage
        #todo: return error object for client with error reason?
        if self.mag_src == None or self.coadds == None:
            if (self.output == 'json') : return None
            else                       : return self.show_usage('getExposureData', self.instr)


        #call core calculation function
        import etc_nires_simple
        data = etc_nires_simple.do_calc(   mag_src      = float(self.mag_src),
                                           exp_time     = float(self.exp_time),  
                                           coadds       = int(self.coadds), 
                                           dither       = self.dither, 
                                           dith_repeats = int(self.dith_repeats),  
                                           obs_wave     = float(self.obs_wave),
                                           seeing       = float(self.seeing),
                                           num_reads    = int(self.num_reads), 
                                           airmass      = float(self.airmass),  
                                           water_vap_col  = self.water_vap_col
                                )

        #return data
        self.output = 'json'
        return data

