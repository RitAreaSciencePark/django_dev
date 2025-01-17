$(document).one('submit','#refresh_form',function(e){
    e.preventDefault();
    $("#refresh_btn").hide();
    setTimeout(() => {
        $('#refresh_form').submit();
    }, 10000);
});
