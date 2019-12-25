$(document).ready(function(){
    console.log("I was loaded !");
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var $csrftoken = getCookie('csrftoken');

    // function submitData() {
    //     // body...

    // }

    $("#register_submit").click(function (e) {
        e.preventDefault();
        var $formdata = $('#register_form').serializeArray();
        $formdata.push({
            name:'csrftoken',
            value:$csrftoken
        });
        $.ajax({
            type:"POST",
            url:"/accounts/registerAdmin/",
            data:$formdata,
            cache:false,
            dataType:"json",
            beforeSend: function () {
                $("#login-form-main-message").css("display", "block").html("<div class='alert alert-info'><img height=\"24px;\" src=\"/static/img/double-ring.gif\" alt=\"loading\" />  Please wait...</div>");
                $(".form_content").css("display", "none");
            },
            success: function (res) {
                if (res.status === "ok") {
                    $("#form_content").css("display", "none");
                    $("#login-form-main-message").css("display", "block").html("<div class='alert alert-success'>user "+ res.user_email + " registered. Redirecting to home</div>");
                    console.log("response 1 ==>>>>>>", res);
                    setTimeout(location.href ='/home/', 6000000);
                }else if (res.status === "fail" && res.error === "password mismatch") {
                    $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>"+"Passwords entered did not match"+"</div>");
                    $("#form_content").css("display", "block");
                    console.log("response 2 ==>>>>>>", res);
                    setTimeout(location.href='/accounts/registerAdmin/', 6000000);
                }else {
                    $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>"+"Unknown error occured, please try again."+"</div>");
                    $("#form_content").css("display", "block");
                    console.log("response 3 ==>>>>>>", res);
                    setTimeout(function () {
                        location.href='/accounts/registerAdmin/';
                    }, 600000);
                }
            },
            // handle a non-successful response
            error: function(xhr,errmsg,err) {
                $('#results').html("<div class='alert alert-danger'>Oops! We have encountered an error: "+errmsg+
                    "<a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });
})