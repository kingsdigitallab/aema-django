
$(document).ready(function(){
    var images = $('.file-upload')
    $(images).each(function(){ 
        var src = $(this).children('a').attr('href');
        $(this).children('a').after('<a href="'+src+'" target="_blank"><img style="padding-left:30px;height:300px;" src='+src+'></img></a>')
    })
})
