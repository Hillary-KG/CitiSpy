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
    console.log("csrf", $csrftoken);

    // function submitData() {
    //     // body...

    // }

    //password confirmation 
    function checkPswd() {
        $('#id_confirm_password').keyup(function () {
            if ($(this).val() !== $('#id_password').val() ) {
                $("#confirm_password_err").css("display", "block").html("<div class='alert alert-danger'>"+"Passwords entered do not match"+"</div>");
            } else {
                $("#confirm_password_err").css("display", "none");
            }       
        });
    };
    checkPswd();

    $("#register_submit").click(function (e) {
        console.log("I was clicked");
        e.preventDefault();
        var $formdata = $('#register_dept_admin').serializeArray();
        $formdata.push({
            name:'csrftoken',
            value:$csrftoken
        });
        $.ajax({
            type:"POST",
            // headers:{
            //     "X-CSRFToken": $csrftoken
            // },
            url:"/accounts/registerAdmin/",
            data:$formdata,
            cache:false,
            dataType:"json",
            beforeSend: function () {
                $("#login-form-main-message").css("display", "block").html("<div class='alert alert-info'><img height=\"24px;\" src=\"/static/img/double-ring.gif\" alt=\"loading\" />  Please wait...</div>");
                $(".form_content").css("display", "none");
            },
            success: function (res) {
                if (res.status === "success") {
                    $("#form_content").css("display", "none");
                    $("#login-form-main-message").css("display", "block").html("<div class='alert alert-success'>user "+ res.user_email + " registered. Redirecting to home</div>");
                    location.href = '/accounts/userLogin/';
                }else{
                    if (res.status === "invalid") {
                        $.each(res.error, function (index, value) {
                            $("#error_id_"+index).css('display', "block").html(value);
                        })
                    }
                    if(res.error == "db error"){
                        $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>Unknown error occured while trying to create user, please try again.</div>");
                        $("#form_content").css("display", "block");
                    }
                    // if (res.error ==="password mismatch") {
                    //     $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>Passwords entered did not match</div>");
                    //     $("#form_content").css("display", "block");
                    // }     
                }      
            },
            // handle a non-successful response
            error: function(xhr,errmsg,err) {
                $('#results').html("<div class='alert alert-danger'>Oops! We have encountered an error: "+errmsg+
                    "<a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        return false;
    });
});