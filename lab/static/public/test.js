var aesEcb = new aesjs.ModeOfOperation.ecb(aesjs.utils.utf8.toBytes('q863cqfiwyug72jc'));
function encrypt(word){
    //添加空格
    var newword='';
    for (var i = 0; i <word.length; i++) {
        if (word[i]==':'&&word[i-1]=='"') {
            newword=newword+word[i]+' '
        }else {
            newword=newword+word[i]
        }
    }
    var textBytes = Array.from(aesjs.utils.utf8.toBytes(newword));
    //补齐
    while (textBytes.length%16!=0) {
        textBytes.push(32);
    }
    var encryptedBytes = aesEcb.encrypt(textBytes);
    return aesjs.utils.hex.fromBytes(encryptedBytes);//encryptedhex
}
function decrypt(sstring){
    function Str2Bytes(str){

        var pos = 0;

        var len = str.length;

        if(len %2 != 0) {

            return null;

        }

        len /= 2;

        var hexA = new Array();

        for(var i=0; i<len; i++)

        {

            var s = str.substr(pos, 2);

            var v = parseInt(s, 16);

            hexA.push(v);

            pos += 2;

        }

        return hexA;
    }
    var bytestring=Str2Bytes(sstring);
    var decryptBytes=aesEcb.decrypt(bytestring);

    return aesjs.utils.utf8.fromBytes(decryptBytes)//decryptedutf8
}

function getElist(){
    data={reason:"getElist"};
    data=JSON.stringify(data);
    data=encrypt(data);
    $.post("/api/",data,function(data,status){
        data=decrypt(data)
        data=JSON.parse(data)
        Elist=data.Elist;
        enginetablestr="";
        enginepanel='';
        tbodystr='';
        for(var n=0;n<Elist.length;n++){
            //tbody
            enginetablestr=enginetablestr
                +"<td >"
                +'<a  href=\"#Epanel'+n+'\" class=\"ui-btn ui-mini ui-btn-inline ui-btn-b ui-corner-all enginebutton \">'
                +Elist[n].name
                +'</a>'
                +"</td>";
            //
            tbodystr=tbodystr+'<td>'
            if (Elist[n].is_active) {
                tbodystr=tbodystr
                    +"<span class='flashing'>on-line</span>"
            }else {
                tbodystr=tbodystr
                    +'off-line'
            }
            tbodystr=tbodystr+'</td>'

            //
            enginepanel=enginepanel
                +'<h1 class="hightlight3 textcenter">'
                +Elist[n].name
                +'</h1>';
            if (Elist[n].system!=''){
                enginepanel=enginepanel
                    +'<h1 class="hightlight1 textcenter">'
                    +Elist[n].system+'</h1>'
            }
            if (Elist[n].provider!=''){
                enginepanel=enginepanel
                    +'<h1 class="hightlight4 textcenter">'
                    +Elist[n].provider
                    +'</h1><hr>'
            }


            enginepanel=enginepanel
                +'<ul data-role="listview" data-inset="true">'
                +'<li><h2 class="hightlight2">坐标</h2></li>'
                +'<h3>'+Elist[n].engineposition+'</h3>'

                +'<li><h2  class="hightlight2">CPU</h2></li>'
                +'<h3>'+Elist[n].cpu+'</h3>';
            if (Elist[n].cpufrom!=''){
                enginepanel=enginepanel
                    +'<h3>'
                    +Elist[n].cpufrom
                    +'</h3>'
            }

            enginepanel=enginepanel
                +'<li><h2 class="hightlight2">内存</h2></li>'
                +'<h3>'+Elist[n].memory
                +'</h3>';
            if (Elist[n].memoryfrom!=''){
                enginepanel=enginepanel
                    +'<h3>'+Elist[n].memoryfrom
                    +'</h3>'
            }


            enginepanel=enginepanel
                +'<li><h2 class="hightlight2">储存</h2></li>'
                +'<h3>'+Elist[n].storage+'</h3>';
            if (Elist[n].storagefrom!=''){
                enginepanel=enginepanel
                    +'<h3>'
                    +Elist[n].storagefrom
                    +'</h3>'
            }

            if (Elist[n].motherboard!=''){
                enginepanel=enginepanel
                    +'<li><h2 class="hightlight2">主板</h2></li>'
                    +'<h3>'
                    +Elist[n].motherboard
                    +'</h3>'
                if (Elist[n].motherboardfrom!=''){
                    enginepanel=enginepanel
                        +'<h3>'
                        +Elist[n].motherboardfrom
                        +'</h3>'
                }
            }

            if (Elist[n].power!=''){
                enginepanel=enginepanel+'<li><h2 class="hightlight2">电源</h2></li>'
                    +'<h3>'
                    +Elist[n].power
                    +'</h3>';
                if (Elist[n].powerfrom!=''){
                    enginepanel=enginepanel
                        +'<h3>'
                        +Elist[n].powerfrom
                        +'</h3>'
                }
            }


            enginepanel=enginepanel+'</ul>'

            $('#Epanel'+n).html(enginepanel)
            enginepanel=''
        };
        $("#engineinfo").html(enginetablestr);
        $('#enginestatu').html(tbodystr);

    });


}
function gettasklist(){
    data={reason:"gettasklist"};
    data=JSON.stringify(data);
    data=encrypt(data);
    $.post("/api/",data,function(data,status){
        data=decrypt(data)
        data=JSON.parse(data)
        tasklist=data.tasklist;
        enginepanel="";
        for(var n=0;n<tasklist.length;n++){
            enginepanel=enginepanel
                +"<tr>"
                +"<td>"
                +tasklist[n].keyword
                +"</td>"
                +"<td>"
                +tasklist[n].progress
                +"</td>"
                +"<td>";
            if (tasklist[n].statu=='waiting') {
                enginepanel=enginepanel+'waiting'

            }else {
                enginepanel=enginepanel+"<span class='flashing'>"+tasklist[n].statu+"</span>"


            }
            enginepanel=enginepanel
                +"</td>"
                +"</tr>";
        };
        $("#tasklist").html('<table data-role="table" data-mode="columntoggle" class="ui-responsive" id="myTable">'+enginepanel+"</table>");
    });
}
function getmessage(){
    data={reason:"getmessage",limit:30,}
    data=JSON.stringify(data)
    data=encrypt(data)
    $.post('/api/', data, function(data, textStatus) {
        data=decrypt(data)
        data=JSON.parse(data);
        tbodystr=''
        messagelist=data.messagelist
        for (var i = 0; i < messagelist.length; i++) {
            tbodystr=tbodystr
                +"<tr>"
                +"<td>"
                +new Date(messagelist[i].time*1000).toLocaleString()
                +"</td><td>"
                +messagelist[i].message
                +"</td><td >"
                +messagelist[i].messagefrom
                +"</td>" +
                "</tr>";
        }
        $('#comments').html(tbodystr)

    });

}
function getRKamount(){
    data=encrypt(JSON.stringify({reason:'getamount'}));
    $.post("/api/",data,function(data,status){
        data=decrypt(data);
        data=JSON.parse(data);
        $("#resamount").text(data.resamount);
        $("#keywordamount").text(data.keyamount);
    });

}
function gethotkey(){
    data=encrypt(JSON.stringify({reason:"gethotkey",limit:20}));
    $.post("/api/",data,function(data,status){
        data=decrypt(data);
        data=JSON.parse(data);
        hotkeylist=data.hotkeylist;
        showstr='';
        for (var i = 0; i < hotkeylist.length; i++) {
            key=hotkeylist[i]
            showstr=showstr+'<button>'+key.keyword+' '+key.hot+'</button>'
        }
        $('#hotkey').html(showstr)

    });
}
function getdonateinfo(){
    data=encrypt(JSON.stringify({reason:'getdonateinfo'}));
    $.post('/api/',data,function (data,status) {
        data=decrypt(data);
        data=JSON.parse(data);
        donatelist=data.donatelist;
        tbodystr='';
        for (var i = 0; i < donatelist.length; i++) {
            D=donatelist[i];
            tbodystr=tbodystr +
                '<tr>'+

                '<td >' +
                new Date(D.donatetime*1000).toLocaleString()+
                '</td>' +
                '<td>' +
                D.donator+
                '</td>' +
                '<td>' +
                D.donatetype+
                '</td>' +
                '<td>' +
                D.describe+
                '</td>' +
                '<td>' +
                D.message+
                '</td>' +

                '</tr>'
        }
        $('#donatetable').html(tbodystr)
    });

}
function statement(){
    if ($.cookie('popup')==undefined) {
        $('#homepagepop div:eq(0)').html("<h1>声明:</h1>");
        $('#homepagepop div:eq(1)').html(" <ol>" +
            "<li>使用本搜索引擎请遵守国家相关法律法规。</li>" +
            "<li>所有搜索结果均来源于网络，与本站无关；</li>" +
            "<li>我们不制造、储存任何形式的资源,仅记录资源的链接。</li>" +
            "<li>我们坚决反对侵权，倡导弘扬社会正能量，望网友自律。</li>" +
            "</ol>");
        $('#homepagepop div:eq(2)').html('');
        $('#homepagepop').popup("open");
        $('#homepagepop').popup({history : false});
        setTimeout(function (){$('#homepagepop').popup('close')},5000);
        $.cookie('popup','fine',{ expires: 1 })
    }
}

function reslistmaker(reslist){
    thundertbodystr='';
    thunderamount=0;

    magnettbodystr='';
    magnetamount=0;

    ed2ktbodystr='';
    ed2kamount=0;

    baidutbodystr='';
    baiduamount=0;

    for (var i = 0; i < reslist.length; i++) {
        res=reslist[i];

        if (res.type=='thunder') {
            thunderamount=thunderamount+1;

            thundertbodystr=thundertbodystr
                +"<tr>"
                +"<td>"
                +res.id
                +"</td>"
                +"<td >"
                +'<a href="' +res.link+'" >'
                +res.link
                +'</a>'
                +"</td>"
                +"</tr>";
        }
        if (res.type=='magnet') {
            magnetamount=magnetamount+1;

            magnettbodystr=magnettbodystr+"<tr>"
                +"<td>"
                +res.id
                +"</td>"
                +"<td >"
                +'<a href="'+res.link+'">'
                +res.link
                +'</a>'
                +"</td>"
                +"</tr>";
        }
        if (res.type=='ed2k') {
            ed2kamount=ed2kamount+1;

            ed2ktbodystr=ed2ktbodystr
                +"<tr>"
                +"<td>"
                +res.id
                +"</td>"
                +"<td  >"
                +'<a href="'+res.link+'">'
                +res.link
                +'</a>'
                +"</td>"
                +"</tr>";
        }
        if (res.type=='baidu') {
            baiduamount=baiduamount+1

            baidutbodystr=baidutbodystr+"<tr>"
                +"<td>"
                +res.id
                +"</td>"+
                "<td  >"
                +'<a target="view_window" href="https://'+res.link+'">'
                +res.link
                +'</a>'
                +"</td>"
                +"<td  >"
                +'<a target="view_window" href="'+res.web+'">'
                +res.web
                +'</a>'
                +"</td>"
                +"</tr>";
        }
    }



    $('#thunderresamount').html(thunderamount);
    $('#magnetresamount').html(magnetamount);
    $('#ed2kresamount').html(ed2kamount);
    $('#baiduresamount').html(baiduamount);

    $('#thunderlist').html(thundertbodystr);
    $('#magnetlist').html(magnettbodystr);
    $('#ed2klist').html(ed2ktbodystr);
    $('#baidulist').html(baidutbodystr);



}


function l(){

//提交关键字
    $("#diggingbutton").click(function(){
        var keyword=$("#inputbox").val();
        if (keyword.length==0||keyword.length>50) {
            $('#homepagepop div:eq(0)').html("<h1>错误!</h1>")
            $('#homepagepop div:eq(1)').html("<h1>输入有误! 关键词长度必须介于0-50!!!!</h1>")
            $('#homepagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
            $('#homepagepop').popup("open");
            setTimeout(function (){$('#homepagepop').popup('close')},5000)

        }else {
            data=JSON.stringify({reason:"cheekkey",keyword:keyword});
            data=encrypt(data);
            $('#homepagepop div:eq(0)').html("<h1>请稍等...</h1>")
            $('#homepagepop div:eq(1)').html("<h1>正在呼叫挖机调度中心！！！</h1>" +
                "<img src=\"/static/loading.gif\" width=\"90%\" height=\"90%\">\n" );
            $('#homepagepop div:eq(2)').html("");
            $('#homepagepop').popup("open");
            $.post("/api/",data,function(data,status){
                data=decrypt(data);
                data=JSON.parse(data);
                if (status=="success"){
                    switch(data.statu){

                        case "digging":
                            $('#homepagepop div:eq(0)').html("<h1>挖掘中!</h1>")
                            $('#homepagepop div:eq(1)').html("<h1>挖掘机已发动!请查看任务列表!!!</h1>")
                            $('#homepagepop div:eq(2)').html("");
                            /*
                            //记录用户当前搜索内容
                            userkeylist=JSON.parse($.cookie('userkeylist'));
                            if (userkeylist.indexOf(keyword) ==-1) {
                                userkeylist.push(keyword)
                            }
                            $.cookie('userkeylist',JSON.stringify(userkeylist));
                            */
                            break;
                        case "cantfind":
                            $('#homepagepop div:eq(0)').html("<h1>抱歉.........</h1>")
                            $('#homepagepop div:eq(1)').html("<h1>挖掘机翻遍800个网站 竟然没有挖到一丁点资源..........</h1>")
                            $('#homepagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
                            break;
                        case "haveres":
                            $('#key').html(keyword);
                            reslist=data.reslist;

                            reslistmaker(reslist);

                            $.cookie('resboxkey',keyword);
                            $('#recheekplace').show();

                            $('#homepagepop div:eq(0)').html("<h1>恭喜!</h1>");
                            $('#homepagepop div:eq(1)').html("<h1>成功挖到"+reslist.length+"条资源!</h1>")
                            $('#homepagepop div:eq(2)').html("<a href='#respage' class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\">去看看</a>");
                            break;

                        default:
                            $('#homepagepop div:eq(0)').html("<h1>emmmmmmm........</h1>");
                            $('#homepagepop div:eq(1)').html("<h1>似乎发生了一些奇怪的事情.....</h1>");
                            $('#homepagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
                            break;
                    }
                }else{
                    $('#homepagepop div:eq(0)').html("<h1>emmmmmmm........</h1>");
                    $('#homepagepop div:eq(1)').html("<h1>发生了一些不可描述的问题....检查一下网络?</h1>");
                    $('#homepagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
                }
                setTimeout(function (){$('#homepagepop').popup('close')},5000)
            });
        }
    });

//重新搜索
    $("#recheekbutton").click(function(){
        resboxkey=$.cookie('resboxkey');
        data={
            reason:'recheek',
            keyword:resboxkey,
        }
        data=JSON.stringify(data);
        data=encrypt(data);
        $('#respagepop div:eq(0)').html("<h1>请稍等...</h1>");
        $('#respagepop div:eq(1)').html("<h1>正在呼叫挖机调度中心！！！</h1>" +
            "<img src=\"/static/loading.gif\" width=\"90%\" height=\"90%\">\n" );
        $('#respagepop div:eq(2)').html("");

        $("#respagepop").popup('open');
        $.post('/api/',data, function(data,status) {
            if (status=='success') {
                data=decrypt(data);
                data=JSON.parse(data);
                if (data.statu == 'digging') {
                    $('#respagepop div:eq(0)').html("<h1>挖掘中!</h1>");
                    $('#respagepop div:eq(1)').html(" <h1>已经成功扔给挖掘机啦!快去任务列表看看吧!!!</h1>" )
                    $('#respagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" href='#homepage'>去看看</a>");

                }else if (data.statu=='timelock') {
                    $('#respagepop div:eq(0)').html("<h1>刚搜索过!</h1>");
                    $('#respagepop div:eq(1)').html(
                        "            <h1>咦?这个关键字有人在"+
                        new Date(data.lasttime*1000).toLocaleString()+
                        "搜索过! 这还没过去一天呢!!! 等等再试吧!</h1>" );
                    $('#respagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
                }
            }else {
                $('#respagepop div:eq(0)').html("<h1>emmmmmmm........</h1>");
                $('#respagepop div:eq(1)').html("<h1>发生了一些不可描述的问题....检查一下网络?</h1>");
                $('#respagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");

            }
            setTimeout(function (){$('#respagepop').popup('close')},5000)
        });
    });

//提交反馈
    $("#feedbackbutton").click(function(){
        var feedbackmessage=$("#feedbackbox").val();
        var feedbackmail=$("#feedbackmail").val();
        var feedbackphone=$("#feedbackphone").val();
        if (0<feedbackmessage.length&&feedbackmessage.length<=200) {
            data={
                reason:'feedback',
                messagefrom:'web',
                phone:feedbackphone,
                mail:feedbackmail,
                message:feedbackmessage
            };
            data=JSON.stringify(data);
            data=encrypt(data);
            $('#feedbackhelppop div:eq(0)').html("<h1>请稍等...</h1>");
            $('#feedbackhelppop div:eq(1)').html("<h1>正在呼叫挖机调度中心！！！</h1>" +
                "<img src=\"/static/loading.gif\" width=\"90%\" height=\"90%\">\n" );
            $('#feedbackhelppop div:eq(2)').html("");
            $("#feedbackhelppop").popup('open');

            $.post('/api/',data, function(data,status) {
                if (status=="success") {
                    $('#feedbackhelppop div:eq(0)').html("<h1>感谢您的反馈!</h1>");
                    $('#feedbackhelppop div:eq(1)').html("<h1>我们将不断改进!!!!</h1>");
                    $('#feedbackhelppop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
                }else {
                    $('#feedbackhelppop div:eq(0)').html("<h1>emmmmmmm........</h1>");
                    $('#feedbackhelppop div:eq(1)').html("<h1>发生了一些不可描述的问题....检查一下网络?</h1>");
                    $('#feedbackhelppop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");

                }
            });
            setTimeout(function (){$('#feedbackhelppop').popup('close')},5000)
        }else {
            $('#feedbackhelppop div:eq(0)').html("<h1>错误!</h1>")
            $('#feedbackhelppop div:eq(1)').html("<h1>反馈内容长度必须介于0-200!</h1>" );
            $('#feedbackhelppop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
            $("#feedbackhelppop").popup('open');
            setTimeout(function (){$('#feedbackhelppop').popup('close')},5000)
        }
    });

//提交评论
    $("#commentsbutton").click(function(){
        var commentsmessage=$("#commentsbox").val();
        if (0<commentsmessage.length&&commentsmessage.length<200) {
            data={
                reason:'leavemessage',
                messagefrom:'web',
                message:commentsmessage
            };
            data=JSON.stringify(data);
            data=encrypt(data);
            $('#homepagepop div:eq(0)').html("<h1>请稍等...</h1>");
            $('#homepagepop div:eq(1)').html("<h1>正在呼叫挖机调度中心！！！</h1>" +
                "<img src=\"/static/loading.gif\" width=\"90%\" height=\"90%\">\n" );
            $('#homepagepop div:eq(2)').html("");

            $("#homepagepop").popup('open');
            $.post('/api/',data, function(data,status) {
                if (status=="success") {
                    $('#homepagepop div:eq(0)').html("<h1>恭喜!</h1>");
                    $('#homepagepop div:eq(1)').html("<h1>留言成功!</h1>");
                    $('#homepagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
                }else {
                    $('#homepagepop div:eq(0)').html("<h1>emmmmmmm........</h1>");
                    $('#homepagepop div:eq(1)').html("<h1>发生了一些不可描述的问题....检查一下网络?</h1>");
                    $('#homepagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
                }
            });
            setTimeout(function (){$('#homepagepop').popup('close')},5000)
        }else {
            $('#homepagepop div:eq(0)').html("<h1>错误!</h1>");
            $('#homepagepop div:eq(1)').html("<h1>输入有误! 留言长度必须介于0-200!!!!</h1>");
            $('#homepagepop div:eq(2)').html("<a  class=\"ui-btn ui-mini ui-btn-b ui-corner-all ui-btn-inline\" data-rel=\"back\">OK</a>");
            $('#homepagepop').popup("open");
            setTimeout(function (){$('#homepagepop').popup('close')},5000)
        }
    });
}
function cheekkey(keyword){
    data=JSON.stringify({reason:"cheekkey",keyword:keyword});
    data=encrypt(data);

    $.post("/api/",data,function(data,status){
            data=decrypt(data);
            data=JSON.parse(data);
            if (status=="success"){

                console.log("连接成功");
                switch(data.statu){

                    case "digging":
                        console.log("digging");
                        break;
                    case "cantfind":
                        console.log("cantfind");
                        break;
                    case "haveres":
                        console.log("haveres");

                        console.log(data.reslist);
                        break;

                    default:
                        console.log("unknow");
                        break;
                }
            }else{
                console.log("连接失败");
            }
        }

    );


}
console.log('-------------------------------------------------');

cheekkey('妈妈的朋友')

console.log('-------------------------------------------------');