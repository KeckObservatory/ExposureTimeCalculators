function getExposureData_NIRC2()
{

    //get values from form
    var magnitude   = document.getElementById('magnitude').value;
    var strehl      = document.getElementById('strehl').value;
    var exp_time    = document.getElementById('exp_time').value;
    var coadds      = document.getElementById('coadds').value;
    var num_dith    = document.getElementById('num_dith').value;
    var num_repeats = document.getElementById('num_repeats').value;
    var camera      = getRadioVal('camera');
    var img_filter  = getRadioVal('img_filter');
    var num_read    = getRadioVal('num_read');
    var x_extent    = getRadioVal('extent');
    var y_extent    = getRadioVal('extent');
    var ao_mode     = getRadioVal('ao_mode');
    var laser_dith  = getRadioVal('laser_dith');


    //create param object for query
    var params = 
    {
        'cmd'         : 'getExposureData',
        'output'      : 'json',
        'instr'       : 'NIRC2',
        'magnitude'   : magnitude,
        'strehl'      : strehl,
        'exp_time'    : exp_time,
        'coadds'      : coadds,
        'num_dith'    : num_dith,
        'num_repeats' : num_repeats,
        'camera'      : camera,
        'img_filter'  : img_filter,
        'num_read'    : num_read,
        'x_extent'    : x_extent,
        'y_extent'    : y_extent,
        'ao_mode'     : ao_mode,
        'laser_dith'  : laser_dith
    }
    
    //send query via ajax
    //todo: use config var and/or change this when we establish permanent server
    ajaxGet("NIRC2EtcApi", params, onGetExposureData_NIRC2);
}


function onGetExposureData_NIRC2(data)
{
    //check for no data, error
    if (!data || data.length == 0)
    {
        alert('no data returned!');
        return;
    }


    //todo: display results in divs
    var snr = data['s2n'];
    var snr_div = document.getElementById("snr_div");
    snr_div.innerHTML = "<h3>SNR = " + snr.toFixed(1).toString() + "</h3>";


}


function getRadioVal(field)
{
    var temp = document.getElementsByName(field);
    for (var i = 0; i < temp.length; i++)
        if (temp[i].checked)
            return temp[i].value;
}