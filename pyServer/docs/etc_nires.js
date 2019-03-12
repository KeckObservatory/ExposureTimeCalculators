function getExposureData_NIRES()
{

    //get values from form
    var mag_src   = document.getElementById('mag_src').value;
    var exp_time    = document.getElementById('exp_time').value;
    var coadds      = document.getElementById('coadds').value;
    var dith_repeats = document.getElementById('dith_repeat').value;
    var obs_wave    = document.getElementById('obs_wave').value;
    var seeing      = document.getElementById('seeing').value;
    var dither      = getRadioVal('dither');
    var num_read    = getRadioVal('num_read');
    var airmass     = getRadioVal('airmass');
    var water_vap_col = getRadioVal('water_vap_col');

    //create param object for query
    var params = 
    {
        'cmd'         : 'getExposureData',
        'output'      : 'json',
        'instr'       : 'NIRES',
        'mag_src'     : mag_src,
        'exp_time'    : exp_time,
        'coadds'      : coadds,
        'dither'      : dither,
        'dith_repeats' : dith_repeats,
        'num_read'    : num_read,
        'obs_wave'    : obs_wave,
        'seeing'      : seeing,
        'airmass'     : airmass,
        'water_vap_col' : water_vap_col
    }
    
    //send query via ajax
    //todo: use config var and/or change this when we establish permanent server
    ajaxGet("NIRESEtcApi", params, onGetExposureData_NIRES);
}


function onGetExposureData_NIRES(data)
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