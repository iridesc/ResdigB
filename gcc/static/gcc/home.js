$(document).ready(function() {

    $("#codesubmitbutton").click(function () {

        $('#codesubmitbutton').hide();
        $('#status').html('<p class="text-info">连接中....</p>');
        $('#status').show();
        var code = $('#code').val();

        data={
            js_code:code,
            compilation_level: $("input[type='radio']:checked").attr('value'),
            output_format:'json',
            output_info:['compiled_code','errors','warnings','statistics']
        };

        console.log(data)
        $.post("/gcc/",JSON.stringify(data),function(data,status){

            $('#encryptedcode').html(data.compiledCode);
            $('#encrypterro').html('<code class="container">'+JSON.stringify(data.errors)+'</code>');
            $('#encryptwaring').html('<code class="container">'+JSON.stringify(data.warnings)+'</code>');
            $('#encryptrate').text( (data.statistics.compressedSize/data.statistics.originalSize).toFixed(2)+'%');
            $('#encryptGrate').text((data.statistics.compressedGzipSize/data.statistics.originalGzipSize).toFixed(2)+'%');
            $('#status').html('<p class="text-info">'+status+'</p>');


        }).error(function () {

            $('#status').html('<p class="text-info">'+'连接失败,请重试!'+'</p>');

        });

        setTimeout(function (){
            $('#status').hide();
            $('#codesubmitbutton').show()
        },10000);
    })
});

