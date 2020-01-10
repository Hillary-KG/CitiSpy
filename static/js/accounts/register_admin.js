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
    // console.log("csrf", $csrftoken);

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

    var $crsf_token = {
        name: 'csrftoken',
        value: getCookie('csrftoken')
    }

    $("#register_dept_admin").submit(function (e) {
        console.log("I was clicked");
        e.preventDefault();
        var $formdata = $(this).serializeArray();
        $formdata.push($crsf_token);
        console.log($formdata);
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
                if (res.status === "success") {
                    register_dept_admin
                    // $("#register_dept_admin")[0].reset();
                    $("#form_content").css("display", "none");
                    $("#reg_errors").css("display", "none");
                    $("#login-form-main-message").css("display", "block").html("<div class='alert alert-success'>Success! User <strong>"+ res.admin_email + "</strong> has been registered successfully.</div>");
                }else{
                    if (res.status === "invalid") {
                        $("#login-form-main-message").css('display', "none");
                        $("#form_content").css("display", "block");
                        $("#reg_errors").empty();
                        $.each(res.error, function (index, value) {
                            $("#reg_errors").css('display', "block").append("<div class='alert alert-danger'>"+ value+"</div>");
                        })
                    }
                    else if(res.error == "db error"){
                        $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>Oops! An error occured while trying to create user, please try again.</div>");
                        $("#form_content").css("display", "block");
                    }else{
                        $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>"+ res.error +"</div>");
                        $("#form_content").css("display", "block");
                    }
                }      
            },
            // handle a non-successful response
            error: function(xhr,errmsg,err) {
                $('#results').html("<div class='alert alert-danger'>Oops! We have encountered an error: "+ xhr.status + ": " + xhr.responseText+
                    "<a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });
});