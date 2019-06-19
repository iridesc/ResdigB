let iscollapsed = true;
let timer;
var cookieexisted = true;
var shown = false;
const x = 'q863cq';
const y = 'fiwy';
const z = 'ug72jc';
var continued = false;
var tempe;
var aesEcb = new aesjs.ModeOfOperation.ecb(aesjs.utils.utf8.toBytes(x + y + z));


$(document).ready(function init() {
    $.cookie('resboxkey', '', { expires: -1 });
    animateinit();
    bind();

    createMarquee(
        { padding: 30 }
    );

    bindapi();


    /*$(function () {
        $('.server_status_text').popover()
    });*/

});
function loadingstart() {
    if (continued) {
        animateCSS('#main_body', 'slideOutDown', '', function () {
            $('#searchview').css('display', 'none');
            $('#app_qrcode_field').css('display', 'none');
            $('#commit_part').css('display', 'none');
            $('#main_body').css('margin-top', '0').css('display', 'none');
            //copy();
        });
        animateCSS('#header', 'slideOutUp', '', function () {
            $('#header').css('display', 'none');
        });
        loadinganimatestart();
    } else {
        loadingend();
    }
}
function loadingend() {
    loadinganimateend();
}
function bind() {
    $('#searchinput_button').click(function () {
        $('#tab .nav-link').siblings().removeClass("active show");
        $('#tabContent .tab-pane').siblings().removeClass("active show");
        $('#Pan-tab').addClass("active show");
        $('#Pan').addClass("active show");
        //submit();
        var keyword = $("#searchinput_input").val();
        cheekkey(keyword);
    });
    $('#task_button').click(function () {
        $('#tab .nav-link').siblings().removeClass("active show");
        $('#tabContent .tab-pane').siblings().removeClass("active show");
        $('#Task-tab').addClass("active show");
        $('#Task').addClass("active show");
        submit();
        recheck_button_invisible();
    });
    $('#backbutton').click(function () {
        back();
    });
    $('#top').click(function () {
        backToTop();
    });
    $('#commit_pic').click(function () {
        if ($('#commit_lg').css('display') === 'none') {
            switchtocommit()
        } else {
            commitswitchtosearchview()
        }
    });
    $('#app_qrcode_pic').click(function () {
        if ($('#app_qrcode_lg').css('display') === 'none') {
            switchtoqr()
        } else {
            qrswitchtosearchview()
        }
    })
    $('#commit_header').click(function () {
        $('#commit_board').on('show.bs.collapse', function () {
        });
        $('#commit_board').on('hide.bs.collapse', function () {
        });
    });
}
function initscroll(s) {
    $(s).bootstrapNews({
        newsPerPage: 3,
        autoplay: true,
        pauseOnHover: true,
        direction: 'up',
        newsTickerInterval: 4000,
        onToDo: function () {
            test(this)
        }
    });
}
function submit() {
    animateCSS('#main_body', 'slideOutDown', '', function () {
        $('#searchview').css('display', 'none');
        $('#app_qrcode_field').css('display', 'none');
        $('#commit_part').css('display', 'none');
        $('#main_body').css('margin-top', '0');
        $('#middlepart').removeClass('col-8 ').addClass('col-10 offset-1');
        $('#result').css('display', 'flex');
        animateCSS('#result', 'zoomInDown', 'fast');
        initcopy();
        //$('[data-toggle="popover"]').popover();
        //copy();
    });
    animateCSS('#header', 'slideOutUp', '', function () {
        $('#header').css('display', 'none');
    });
}
function recheck_button_visible() {
    $('#recheckbutton').css('visibility', 'visible');
}
function recheck_button_invisible() {
    $('#recheckbutton').css('visibility', 'hidden');
}
function historyanimationout() {
    event.stopPropagation();
    if (cookieexisted) {
        $('#search_history_suggestion').removeClass('animated fadeOut fadeIn fast').css('display', 'flex');
        animateCSS('#search_history_suggestion', 'fadeIn', 'fast');
    }
    animateCSS('#task_button', 'fadeOut', 'fast');
    $('#task_button').css('display', 'none');
    shown = true;
}
function historyanimationin() {
    if (shown) {
        if (cookieexisted) {
            animateCSS('#search_history_suggestion', 'fadeOut', 'fast');
            $('#search_history_suggestion').css('display', 'none');
            shown = false;
        }
        $('#task_button').removeClass('animated fadeIn fast fadeOut').css('display', 'flex');
        animateCSS('#task_button', 'fadeIn', 'fast');
    }
}
function back() {
    animateCSS('#result', 'hinge', 'fast', function () {
        $('#main_body').css('margin-top', '5vh');
        $('#searchview').css('display', 'flex');
        $('#result').css('display', 'none');
        $('#app_qrcode_field').css('display', 'block');
        $('#header').css('display', 'block');
        $('#commit_part').css('display', 'block');
        $('#middlepart').removeClass('col-10 offset-1').addClass('col-10 px-0 col-sm-8 mx-auto');
        animateinit();
        recheck_button_invisible();
    });
}
function drag() {
    console.info('click');
    $('#header').removeClass('animated slideInUp slideOutDown');
    if (iscollapsed) {
        animateCSS('#header', 'slideOutDown', '', function () {
            $('#header').css('marginTop', '-9vh');
        });
    } else {

        $('#header').css('marginTop', '-90vh');
        animateCSS('#header', 'slideInUp', '', function () {
            let header = document.getElementById('header');
            header.removeAttribute('style');
            console.info(iscollapsed);
        });
    }

    iscollapsed = !iscollapsed;
}
function animateinit(speed) {
    /*loadingstart('1000','#loading');*/
    $('#header').css('display', 'block');
    $('#main_body').css('margin-top', '5vh').css('display', 'flex');
    animateCSS('#header', 'bounceInDown ', speed);
    animateCSS('#main_body', 'bounceInUp', speed);
}
function animateCSS(element, animationName, speed, callback) {
    const node = $(element);
    node.addClass('animated' + ' ' + animationName + ' ' + speed);

    function handleAnimationEnd() {
        node.removeClass('animated' + ' ' + animationName + ' ' + speed);
        node.off('animationend', handleAnimationEnd);

        if (typeof callback === 'function') callback()
    }

    node.on('animationend', handleAnimationEnd)
}
function loadinganimatestart() {
    $("#loading_field").css('display', 'flex');
    animateCSS('#loading', 'heartBeat');
    timer = setTimeout('loadinganimatestart()', 1000);
}
function loadinganimateend() {
    clearTimeout(timer);
    $("#loading_field").css('display', 'none');
}
function backToTop() {
    $('#tabContent').animate(
        {
            scrollTop: top
        }, 800);
}
function switchtocommit() {
    animateCSS('#searchview', 'zoomOutLeft', 'fast', function () {
        $('#searchview').css('display', 'none');
        $('#commit_lg').css('display', 'flex');
        animateCSS('#commit_lg', 'zoomInLeft', 'fast');
        //copy();
    });
}
function commitswitchtosearchview() {
    animateCSS('#commit_lg', 'zoomOutLeft', 'fast', function () {
        $('#searchview').css('display', 'flex');
        $('#commit_lg').css('display', 'none');
        animateCSS('#searchview', 'zoomInLeft', 'fast');
    });
}
function switchtoqr() {
    animateCSS('#searchview', 'zoomOutRight', 'fast', function () {
        $('#searchview').css('display', 'none');
        $('#app_qrcode_lg').css('display', 'flex');
        animateCSS('#app_qrcode_lg', 'zoomInRight', 'fast');
        //copy();
    });
}
function qrswitchtosearchview() {
    animateCSS('#app_qrcode_lg', 'zoomOutLeft', 'fast', function () {
        $('#searchview').css('display', 'flex');
        $('#app_qrcode_lg').css('display', 'none');
        animateCSS('#searchview', 'zoomInLeft', 'fast');
    });
}
function initcopy() {
    var clipboard = new ClipboardJS('.copy');
    clipboard.on('success', function (e) {
        tempe = e;
        var trigger = $(e.trigger);
        // console.log("ria " + trigger);

        trigger.popover('show');
        trigger.on('shown.bs.popover', function () {
            setTimeout('$(tempe.trigger).popover(\'hide\')', 3000);
        });
        // console.info('test:', e);
        // console.info('Action:', e.action);
        // console.info('Text:', e.text);
        // console.info('Trigger:', e.trigger);
        e.clearSelection();
    });

    clipboard.on('error', function (e) {
        console.error('Action:', e.action);
        console.error('Trigger:', e.trigger);
    });
}
/////////////////////////////下为接口///////////////////////////////////////
function encrypt(word) {
    //添加空格
    var newword = '';
    for (var i = 0; i < word.length; i++) {
        if (word[i] == ':' && word[i - 1] == '"') {
            newword = newword + word[i] + ' '
        } else {
            newword = newword + word[i]
        }
    }
    var textBytes = Array.from(aesjs.utils.utf8.toBytes(newword));
    //补齐
    while (textBytes.length % 16 != 0) {
        textBytes.push(32);
    }
    var encryptedBytes = aesEcb.encrypt(textBytes);
    return aesjs.utils.hex.fromBytes(encryptedBytes);//encryptedhex
}
function decrypt(sstring) {
    function Str2Bytes(str) {

        var pos = 0;

        var len = str.length;

        if (len % 2 != 0) {

            return null;

        }

        len /= 2;

        var hexA = new Array();

        for (var i = 0; i < len; i++) {

            var s = str.substr(pos, 2);

            var v = parseInt(s, 16);

            hexA.push(v);

            pos += 2;

        }

        return hexA;
    }
    var bytestring = Str2Bytes(sstring);
    var decryptBytes = aesEcb.decrypt(bytestring);

    return aesjs.utils.utf8.fromBytes(decryptBytes)//decryptedutf8
}
function getElist() {
    var data = { reason: "getElist" };
    data = JSON.stringify(data);
    data = encrypt(data);
    $.post("/resdig/api/", data, function (data, status) {
        data = decrypt(data);
        data = JSON.parse(data);
        var Elist = data.Elist;
        var enginebuttonstr = "";
        var enginepanel = '';
        var temp = new Array()
        test(Elist);
        if (Elist.length > 3) {
            console.log('服务器数量异常')
        } else {
            for (var n = 0; n < Elist.length; n++) {
                var o = new Object();
                o.status = Elist[n].is_active;
                o.name = Elist[n].name;
                o.content =
                    Elist[n].system + " " +
                    Elist[n].provider + " " +
                    Elist[n].engineposition + " " +
                    Elist[n].cpu + " " +
                    Elist[n].cpufrom + " " +
                    Elist[n].memory + " " +
                    Elist[n].memoryfrom + " " +
                    Elist[n].storage + " " +
                    Elist[n].motherboard + " " +
                    Elist[n].motherboardfrom + " " +
                    Elist[n].power + " " +
                    Elist[n].powerfrom;
                temp[n] = o;
            }

            $(".server_status_color").each(function (n) {
                $(this).removeClass("btn-success btn-danger");
                temp[n].status ? $(this).addClass("btn-success").html("运行中") : $(this).addClass("btn-danger").html("停机中");
            });

            $(".server_status_small_color").each(function (n) {
                $(this).removeClass("btn-success btn-danger");
                temp[n].status ? $(this).addClass("btn-success").html("运行中") : $(this).addClass("btn-danger").html("停机中");
            });

            $(".server_status_text").each(function (n) {
                test(this);
                $(this).find(".server_name").html("服务器 " + temp[n].name);
                $(this).popover(options = {
                    content: temp[n].content,
                    title: temp[n].name,
                    placement: 'bottom'
                })
            });

            $(".server_status_small_text").each(function (n) {
                test(this);
                $(this).find(".server_name").html("服务器 " + temp[n].name);
                $(this).popover(options = {
                    content: temp[n].content,
                    title: temp[n].name,
                    placement: 'bottom'
                })
            });

        }
    });


}
function gettasklist() {
    var data = { reason: "gettasklist" };
    data = JSON.stringify(data);
    data = encrypt(data);
    $.post("/resdig/api/", data, function (data, status) {
        data = decrypt(data);
        data = JSON.parse(data);
        var tasklist = data.tasklist;
        test(tasklist);
        var temp = "";
        if (tasklist.length == 0) {
            temp = "                                <div class=\"jumbotron\">\n" +
                "                                    <h1 class=\"display-4\">emmmmm</h1>\n" +
                "                                    <p class=\"lead\">真巧，挖掘引擎正空着</p>\n" +
                "                                    <hr class=\"my-4\">\n" +
                "                                    <p>要不去首页搜一下？</p>\n" +
                "                                    <a class=\"btn btn-primary btn-lg\" href=\"#\" role=\"button\">回首页</a>\n" +
                "                                </div>"
        } else {
            $('#Task_jumbotron').remove();
            for (var n = 0; n < tasklist.length; n++) {
                temp = temp + "<li class=\"list-group-item list-group-item-action justify-content-between d-flex\">" +
                    "<div class=\"mr-1 col-1 col-sm-1 col-lg-1 sort control_button_big\">" + n + 1 +
                    "</div>" +
                    "<div class=\"col-6 col-sm-8 col-lg-6 filename text-truncate overflow-auto d-flex row\">" +
                    "<a class=\"text-center my-auto\">" + tasklist[n].keyword + "</a>" +
                    "<div class=\"progress w-100 m-0\">" +
                    "<div class=\"progress-bar progress-bar-striped progress-bar-animated\" role=\"progressbar\" aria-valuenow=\"" + tasklist[n].progress + "\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: " + tasklist[n].progress + "%\"></div>" +
                    "</div>" +
                    "</div>" +
                    "<div class=\"col-3 col-sm-2 col-lg-1 operation d-flex justify-content-sm-between\">";
                if (tasklist[n].statu == 'waiting') {
                    temp = temp + "<span class=\"mx-auto badge badge-pill badge-danger\">waiting</span>" +
                        "</div>" +
                        "</li>";
                } else {
                    temp = temp + "<span class=\"mx-auto badge badge-pill badge-primary\">" + tasklist[n].statu + "</span>" +
                        "</div>" +
                        "</li>";
                }
            }
        }
        $("#Task_table").html(temp);
    });
}
function getmessage() {
    var data = { reason: "getmessage", limit: 30 };
    data = JSON.stringify(data);
    data = encrypt(data);
    $.post('/resdig/api/', data, function (data, textStatus) {
        data = decrypt(data);
        data = JSON.parse(data);
        var tbodystr = '';
        var messagelist = data.messagelist;
        for (var i = 0; i < messagelist.length; i++) {
            tbodystr = tbodystr + "<li class=\"news-item\">" +
                "<table class=\"card news-item-sub\">" +
                "<tbody>" +
                "<tr class=\"commit_area row\">" +
                "<td class=\"col-6 commit_title\">" + messagelist[i].message + "</td>" +
                "<td class=\"col-6\">" + new Date(messagelist[i].time * 1000).toLocaleString() + "</td>" +
                "</tr>" +
                "</tbody>" +
                "</table>" +
                "</li>";
        }
        $('#commit_list_lg').html(tbodystr);
        $('#commit_list').html(tbodystr);
    });

}
function getRKamount() {
    data = encrypt(JSON.stringify({ reason: 'getamount' }));
    $.post("/resdig/api/", data, function (data, status) {
        data = decrypt(data);
        data = JSON.parse(data);
        $("#resamount").text('资源储量: ' + Math.round(data.resamount / 1000) / 10 + 'W+');
        //$("#keywordamount").text(data.keyamount);
    });
}
function getdonateinfo() {
    var data = encrypt(JSON.stringify({ reason: 'getdonateinfo' }));
    $.post('/resdig/api/', data, function (data, status) {
        data = decrypt(data);
        data = JSON.parse(data);
        var donatelist = data.donatelist;
        test(donatelist);
        var tbodystr = "<thead>" +
            "<tr>" +
            "<th>时间</th>" +
            "<th>捐赠者</th>" +
            "<th>类型</th>" +
            "<th>详情</th>" +
            "<th>留言</th>" +
            "</tr>" +
            "</thead>";
        for (var i = 0; i < donatelist.length; i++) {
            var D = donatelist[i];
            tbodystr = tbodystr + "<tr>" +
                "<td>" + new Date(D.donatetime * 1000).toLocaleString() + "</td>" +
                "<td>" + D.donator + "</td>" +
                "<td>" + D.donatetype + "</td>" +
                "<td>" + D.describe + "</td>" +
                "<td class='overflow-auto'>" + D.message + "</td>" +
                "</tr>";
        }
        $('#donation_table').html(tbodystr);
        $('#donation_table_small').html(tbodystr);
    });

}
function cheekkey(keyword) {
    function ScoreRes(reslist) {
        let new_reslist = Array()
        // score setting
        let total_score = 100
        let filesize_score_rate = 0.3
        let pic_score_rate = 0.45
        let sound_score_rate = 0.1
        let bluray_score_rate = 0.15

        let total_size = 0
        let fileamount = 1
        reslist.forEach(res => {
            if (res.filesize != 0) {
                total_size += res.filesize
                fileamount += 1
            }
        });
        let average_size = total_size / fileamount

        for (let index = 0; index < reslist.length; index++) {
            const res = reslist[index];
            let tags = Array()

            if (res.filename != null) {
                //  picture quality
                if (res.filename.indexOf('1080p') > -1 || res.filename.indexOf('BD1920') > -1) {

                    res.pic_score = 0.8
                    tags.push({ color: 'primary', name: '1080p' })

                } else if (res.filename.indexOf('720p') > -1 || res.filename.indexOf('BD1280') > -1) {

                    res.pic_score = 0.6
                    tags.push({ color: 'success', name: '720p' })

                } else if (res.filename.indexOf('480p') > -1) {
                    res.pic_score = 0.4
                    tags.push({ color: 'secondary', name: 'HD1280' })
                } else {
                    res.pic_score = 0.2
                }

                // BluRay
                if (res.filename.indexOf('BluRay') > -1) {
                    res.bluray_score = 1
                    tags.push({ color: 'primary', name: 'BluRay' })

                } else {
                    res.bluray_score = 0
                }

                // sounds quality
                if (res.filename.indexOf('DTS-HD') > -1) {
                    res.sound_score = 1
                    tags.push({ color: 'info', name: 'DTS-HD' })
                } else if(res.filename.indexOf('DTS') > -1) {
                    res.sound_score = 0.8
                    tags.push({ color: 'info', name: 'DTS' })
                }else if(res.filename.indexOf('DD5.1') > -1) {
                    res.sound_score = 0.8
                    tags.push({ color: 'info', name: 'Dolby' })
                }

            } else {
                res.sound_score = 0
                res.pic_score = 0
                res.bluray_score = 0
            }

            // file size score
            res.filesize_score = (1 + (res.filesize - average_size) / average_size) / 2
            tags.push({
                color: 'dark',
                name: res.filesize == 0 ? '未知大小' : (res.filesize / 1024).toFixed(2) + "GB"
            })

            res.tags = tags
            res.total_score = total_score * (
                res.pic_score * pic_score_rate +
                res.sound_score * sound_score_rate +
                res.filesize_score * filesize_score_rate +
                res.bluray_score * bluray_score_rate
            )
            new_reslist[index] = res
        }
        function SortByScore(a, b) {
            return b.total_score - a.total_score
        }
        new_reslist.sort(SortByScore)


        return new_reslist
    }
    if (keyword.length == 0 || keyword.length > 50) {
        animateCSS('#searchinput', 'wobble', 'fast');
        $('#alert_area').html(alert_html("错误!", "输入有误! 留言长度必须介于0-50!!!!", "alert-secondary"));
        setTimeout(function () { $('#alert_item').alert('close') }, 5000)
    } else {
        //记录用户当前搜索内容
        var mydiglist = JSON.parse($.cookie('mydiglist'));

        if (mydiglist.indexOf(keyword) == -1) {
            mydiglist.push(keyword);
            $.cookie('mydiglist', JSON.stringify(mydiglist), { expires: 30 });
        }
        var data = JSON.stringify({ reason: "cheekkey", keyword: keyword });
        data = encrypt(data);
        //$('#alert_area').html(alert("请稍等...","正在呼叫挖机调度中心！！！","alert-warning"));
        loadingstart();///
        continued = true;
        $.post("/resdig/api/", data, function (data, status) {
            test(status);
            data = decrypt(data);
            data = JSON.parse(data);
            test(data.statu);
            test(data);
            if (status == "success") {
                continued = false;

                switch (data.statu) {
                    case "digging":
                        $('#alert_area').html(alert_html("挖掘中!", "挖掘机已发动!请查看任务列表!!!", "alert-success"));
                        break;
                    case "cantfind":
                        $('#alert_area').html(alert_html("抱歉.........", "挖掘机翻遍800个网站 竟然没有挖到一丁点资源..........", "alert-secondary"));
                        break;
                    case "haveres":
                        $('#searchkeywords').html(keyword);
                        var reslist = data.reslist;

                        reslist = ScoreRes(reslist)

                        reslistmaker(reslist);
                        $.cookie('resboxkey', keyword);
                        submit();
                        recheck_button_visible();
                        //$('#recheekplace').show();
                        //成功
                        break;
                    default:
                        $('#alert_area').html(alert_html("emmmmmmm........", "似乎发生了一些奇怪的事情.....", "alert-secondary"));
                        break;
                }
            } else {
                continued = false;
                $('#alert_area').html(alert_html("emmmmmmm........", "发生了一些不可描述的问题....检查一下网络?", "alert-secondary"));
            }
            setTimeout(function () { $('#alert_item').alert('close') }, 5000);
        });
    }

}

function reslinemaker(res) {
    function getfilename(res) {
        if (res.filename == null) {
            return res.link.slice(0, 20) + '...'
        } else {
            return res.filename
        }
    }

    function GetResBuffHtml(res) {
        let buff_html = ""
        res.tags.forEach(tag => {
            buff_html += '<span class=\"mx-auto badge badge-pill badge-' + tag.color + '\">' + tag.name + "</span>"
        });
        return buff_html

    }
    return "<li class=\"list-group-item list-group-item-action justify-content-between d-flex\">" +

        "<div class=\"col-1 mr-1 col-sm-1 col-lg-1 sort control_button_big\">" +
        "</div>" +

        "<div class=\"col-6 col-sm-8 col-lg-6 filename text-truncate overflow-auto d-flex row\">" +

        "<a class=\"text-center my-auto\">" + getfilename(res) + "</a>" +
        GetResBuffHtml(res) +
        "</div>" +

        "<div class=\"col-3 col-sm-2 col-lg-1 operation d-flex justify-content-sm-between\">" +
        "<a class=\"url mx-0\" href=\"" + res.web + "\">" +
        "<img src=\"https://raw.githubusercontent.com/iridesc/ocolabstatic/master/resdig/img/url.png\" class=\"mx-0 justify-content-around originalurl control_button_big btn \">" +
        "</a>" +
        "<img src=\"https://raw.githubusercontent.com/iridesc/ocolabstatic/master/resdig/img/copy.png\" data-container=\"body\" data-toggle=\"popover\" data-placement=\"top\" data-content=\"已复制\" data-trigger=\"manual\" data-clipboard-action=\"copy\" data-clipboard-text=\"" + res.link + "\" class=\"control_button_big btn copy\">" +
        "</div>" +

        "</li>";
}


function reslistmaker(reslist) {
    thundertbodystr = '';
    thunderamount = 0;

    hqrtbodystr = '';
    hqramount = 0

    magnettbodystr = '';
    magnetamount = 0;

    ed2ktbodystr = '';
    ed2kamount = 0;

    baidutbodystr = '';
    baiduamount = 0;

    // HQR
    

    for (var i = 0; i < reslist.length; i++) {
        var res = reslist[i];
        
        if (i < 10) {
            hqrtbodystr+=reslinemaker(res)
            hqramount+=1
        } 
        
        if (res.type == 'thunder') {
            thunderamount = thunderamount + 1;

            thundertbodystr = thundertbodystr + reslinemaker(res)
        }
        
        if (res.type == 'magnet') {
            magnetamount = magnetamount + 1;

            magnettbodystr = magnettbodystr + reslinemaker(res)
        }
        
        if (res.type == 'ed2k') {
            ed2kamount = ed2kamount + 1;

            ed2ktbodystr = ed2ktbodystr + reslinemaker(res)
        }
        
        if (res.type == 'baidu') {
            baiduamount = baiduamount + 1;
            baidutbodystr = baidutbodystr + reslinemaker(res)

        }
    }
    ////后面的版本跟进资源数量

    /*$('#thunderresamount').html(thunderamount);
    $('#magnetresamount').html(magnetamount);
    $('#ed2kresamount').html(ed2kamount);
    $('#baiduresamount').html(baiduamount);
    */

    thunderamount == 0 ? thundertbodystr = "                                <div class=\"jumbotron\" id=\"Thunder_ejumbotron\">\n" +
        "                                    <h1 class=\"display-4\">emmmmm</h1>\n" +
        "                                    <p class=\"lead\">没有该类别的资源</p>\n" +
        "                                    <hr class=\"my-4\">\n" +
        "                                    <p>试试别的关键字？</p>\n" +
        "                                    <a class=\"btn btn-primary btn-lg\" href=\"#\" role=\"button\">回首页</a>\n" +
        "                                </div>" : $('#Thunder_jumbotron,#Thunder_ejumbotron').remove();

    hqramount == 0 ? hqrtbodystr = "                                <div class=\"jumbotron\">\n" +
        "                                    <h1 class=\"display-4\">emmmmm</h1>\n" +
        "                                    <p class=\"lead\">没有该类别的资源</p>\n" +
        "                                    <hr class=\"my-4\">\n" +
        "                                    <p>试试别的关键字？</p>\n" +
        "                                    <a class=\"btn btn-primary btn-lg\" href=\"#\" role=\"button\">回首页</a>\n" +
        "                                </div>" : $('#HQR_jumbotron,#HQR_ejumbotron').remove();

    magnetamount == 0 ? magnettbodystr = "                                <div class=\"jumbotron\">\n" +
        "                                    <h1 class=\"display-4\">emmmmm</h1>\n" +
        "                                    <p class=\"lead\">没有该类别的资源</p>\n" +
        "                                    <hr class=\"my-4\">\n" +
        "                                    <p>试试别的关键字？</p>\n" +
        "                                    <a class=\"btn btn-primary btn-lg\" href=\"#\" role=\"button\">回首页</a>\n" +
        "                                </div>" : $('#Magnet_jumbotron,#Magnet_ejumbotron').remove();


    ed2kamount == 0 ? ed2ktbodystr = "                                <div class=\"jumbotron\">\n" +
        "                                    <h1 class=\"display-4\">emmmmm</h1>\n" +
        "                                    <p class=\"lead\">没有该类别的资源</p>\n" +
        "                                    <hr class=\"my-4\">\n" +
        "                                    <p>试试别的关键字？</p>\n" +
        "                                    <a class=\"btn btn-primary btn-lg\" href=\"#\" role=\"button\">回首页</a>\n" +
        "                                </div>" : $('#Ed2k_jumbotron,#Ed2k_ejumbotron').remove();

    baiduamount == 0 ? baidutbodystr = "                                <div class=\"jumbotron\">\n" +
        "                                    <h1 class=\"display-4\">emmmmm</h1>\n" +
        "                                    <p class=\"lead\">没有该类别的资源</p>\n" +
        "                                    <hr class=\"my-4\">\n" +
        "                                    <p>试试别的关键字？</p>\n" +
        "                                    <a class=\"btn btn-primary btn-lg\" href=\"#\" role=\"button\">回首页</a>\n" +
        "                                </div>" : $('#Pan_jumbotron,#Pan_ejumbotron').remove();

    $('#Thunder_table').html(thundertbodystr);
    $('#HQR_table').html(hqrtbodystr);
    $('#Magnet_table').html(magnettbodystr);
    $('#Ed2k_table').html(ed2ktbodystr);
    $('#Pan_table').html(baidutbodystr);

    autosort('#Thunder_table');
    autosort('#hqr_table');
    autosort('#Magnet_table');
    autosort('#Ed2k_table');
    autosort('#Pan_table');
}
function autosort(table) {
    var len = $(table + " li").length;
    test(len);
    for (var i = 0; i < len; i++) {
        $(table).find(".sort").eq(i).html(i + 1);
    }
}
function mydigmaker() {
    if ($.cookie('mydiglist') == undefined) {
        $.cookie('mydiglist', JSON.stringify([]), { expires: 30 })
    } else {
        $('#searchinput_input').bind('click', function () {
            var mydiglist = JSON.parse($.cookie('mydiglist')).reverse();
            var liststr = '';
            if (mydiglist.length > 5) {
                mydiglist.length = 5;
            }
            for (var i = 0; i < mydiglist.length; i++) {
                liststr = liststr +
                    "<a class=\"list-group-item list-group-item-action\" onclick=\"sugclick(this)\">" + mydiglist[i] + "</a>";
            }
            $('#search_history_suggestion').html(liststr);
        });
    }

}
function sugclick(el) {
    $('#searchinput_input').val(el.innerText);
}
function alert_html(mesg1, mesg2, type) {
    $('#alert_area').html('');
    return alert = "<div id='alert_item' class=\"alert " + type + " alert-dismissible fade show\">" +
        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>" +
        "<strong>" + mesg1 + "</strong> " + mesg2 + "</div>";
}
function bindapi() {

    //用户搜索词
    mydigmaker();
    //以后跟进资源数量
    //getRKamount();
    //获取捐赠信息
    getdonateinfo();
    //获取引擎状态
    getElist();
    //任务列表
    gettasklist();
    //用户评论
    getmessage();

    //声明

    //提交关键字已移动到bind


    //提交反馈 后续版本跟进
    /*$("#feedbackbutton").click(function(){
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
                "<img src=\"/static/resdig/loading.gif\" width=\"90%\" height=\"90%\">\n" );
            $('#feedbackhelppop div:eq(2)').html("");
            $("#feedbackhelppop").popup('open');

            $.post('/resdig/api/',data, function(data,status) {
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
*/
    //提交评论
    $("#submit_button_lg").click(function () {
        var commentsmessage = $("#describe").val();
        if (0 < commentsmessage.length && commentsmessage.length < 200) {
            var data = {
                reason: 'leavemessage',
                messagefrom: 'web',
                message: commentsmessage,
            };
            data = JSON.stringify(data);
            data = encrypt(data);
            $('#alert_area').html(alert_html("请稍等...", "正在呼叫挖机调度中心！！！", "alert-warning"));
            $.post('/resdig/api/', data, function (data, status) {
                test("status" + status);
                if (status == "success") {
                    $('#alert_area').html(alert_html("恭喜!", "留言成功!", "alert-success"));
                } else {
                    $('#alert_area').html(alert_html("emmmmmmm........", "发生了一些不可描述的问题....检查一下网络?", "alert-secondary"));
                }
            });
        } else {
            $('#alert_area').html(alert_html("错误!", "输入有误! 留言长度必须介于0-200!!!!", "alert-secondary"));
        }
        setTimeout(function () { $('#alert_item').alert('close') }, 5000)

    });
    $("#submit_button").click(function () {
        var commentsmessage = $("#describe").val();
        if (0 < commentsmessage.length && commentsmessage.length < 200) {
            var data = {
                reason: 'leavemessage',
                messagefrom: 'web',
                message: commentsmessage,
            };
            data = JSON.stringify(data);
            data = encrypt(data);
            $('#alert_area').html(alert("请稍等...", "正在呼叫挖机调度中心！！！", "alert-warning"));
            $.post('/resdig/api/', data, function (data, status) {
                test("status" + status);
                if (status == "success") {
                    $('#alert_area').html(alert("恭喜!", "留言成功!", "alert-success"));
                } else {
                    $('#alert_area').html(alert("emmmmmmm........", "发生了一些不可描述的问题....检查一下网络?", "alert-secondary"));
                }
            });
        } else {
            $('#alert_area').html(alert("错误!", "输入有误! 留言长度必须介于0-200!!!!", "alert-secondary"));
        }
        setTimeout(function () { $('#alert_item').alert('close') }, 5000)

    });

    //建议
    var sugtime = 0;
    const suggap = 100;
    $('#searchinput_input').bind('input propertychange', function () {
        var nowtime = new Date().getTime();
        if (nowtime - sugtime > suggap) {
            sugtime = nowtime;
            var key = $(this).val();
            $.get('https://suggest.video.iqiyi.com/?key=' + key + '&rltnum=10', function (data, status) {
                data = JSON.parse(data);
                var liststr = '';
                if (data.data.length > 5) {
                    data.data.length = 5;
                }
                for (var i = 0; i < data.data.length; i++) {
                    liststr = liststr +
                        "<a class=\"list-group-item list-group-item-action\" onclick=\"sugclick(this)\">" + data.data[i].name + "</a>";
                }
                $('#search_history_suggestion').html(liststr)
            })
        }
    });


    //间隔 获取引擎状态 任务列表 用户搜索记录 用户评论
    setInterval(function () {
        //userkey
        mydigmaker();
        //引擎
        getElist();
        //任务
        gettasklist();
        //获取评论
        getmessage();
    }, 5000);
}
function commontab() {
    if ($.cookie('resboxkey') !== '' || $.cookie('resboxkey') != null || $.cookie('resboxkey').length !== 0 || $.cookie('resboxkey') != undefined) {
        recheck_button_visible();
    } else {
        recheck_button_invisible();
    }
}
function refresh_method() {
    $("#recheckbutton_field").html("");
    var spinner = new Spinner();
    var spintarget = $("#recheckbutton_field").get(0);
    spinner.spin(spintarget);
    var resboxkey = $.cookie('resboxkey');
    test(resboxkey);
    var data = {
        reason: 'recheek',
        keyword: resboxkey,
    };
    data = JSON.stringify(data);
    data = encrypt(data);
    $.post('/resdig/api/', data, function (data, status) {
        spinner.spin();
        if (status == 'success') {
            data = decrypt(data);
            data = JSON.parse(data);
            if (data.statu == 'digging') {
                test("digging");
                $("#recheckbutton_field").html(recheckbutton_html("Hi,已经成功扔给挖掘机啦!快去任务列表看看吧!!!"));
                $('#recheck_pop').popover({
                    trigger: 'manual',
                });
                $("#recheck_pop").popover('show');
                $("#recheck_pop").on('shown.bs.popover', function () {
                    setTimeout('$("#recheck_pop").popover(\'hide\')', 3000);
                });
                $("#recheck_pop").on('hidden.bs.popover', function () {
                    $("#recheckbutton_field").delay(3000).html(recheckbutton_html(""));
                });
            } else if (data.statu == 'timelock') {
                test("timelock");
                $("#recheckbutton_field").html(recheckbutton_html("不好意思啊,这个关键字有人在" + new Date(data.lasttime * 1000).toLocaleString() + "搜索过! 这还没过去一天呢!!! 等等再试吧!"));
                $('#recheck_pop').popover({
                    trigger: 'manual'
                });
                $("#recheck_pop").popover('show');
                $("#recheck_pop").on('shown.bs.popover', function () {
                    setTimeout('$("#recheck_pop").popover(\'hide\')', 3000);
                });
                $("#recheck_pop").on('hidden.bs.popover', function () {
                    $("#recheckbutton_field").delay(3000).html(recheckbutton_html(""));
                });
            }
        } else {
            $("#recheckbutton_field").html(recheckbutton_html("Hi,发生了一些不可描述的问题....检查一下网络?"));
            $('#recheck_pop').popover({
                trigger: 'manual'
            });
            $("#recheck_pop").popover('show');
            $("#recheck_pop").on('shown.bs.popover', function () {
                setTimeout('$("#recheckbutton").popover(\'hide\')', 3000);
            });
            $("#recheck_pop").on('hidden.bs.popover', function () {
                $("#recheckbutton_field").delay(3000).html(recheckbutton_html(""));
            });
        }
    });
}
function recheckbutton_html(popcontent) {
    return "                        <button id=\'recheck_pop\' onclick=\"refresh_method();\" class=\"btn btn-primary\" data-container=\"body\" data-toggle=\"popover\" data-placement=\"bottom\" data-content=\"" + popcontent + "\">" +
        "                            <img id=\"recheckbutton\" src=\"https://raw.githubusercontent.com/iridesc/ocolabstatic/master/resdig/img/refresh.png\">\n" +
        "                        </button>"
}
function test(t) {
    // console.log(t);
}