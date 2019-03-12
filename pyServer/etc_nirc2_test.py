def do_calc(magnitude):
    #return final data dictionary result
    result = {}
    result['s2n'] = 1234
    return result


#This code below will only run if this module is run from the command line
#example: python etc_nirc2.py
if __name__ == "__main__":

    #test
    data = do_calc( magnitude   = 15 )
    print ('result = ', data)
