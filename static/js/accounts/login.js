$(document).ready(function(){
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

    var $csrf_token = {
        name: "csrfmiddlewaretoken",
        value: getCookie('csrftoken')
    };
    var $myId = $("#login_form >#form_content > .form-group > button").attr('class');
    console.log($myId);
    $("#name_form").submit(function(e){
        console.log("I am in submit");
        e.preventDefault();
        var $form_data = $(this).serializeArray();
        $form_data.push($csrf_token);
        // console.log("form data", $form_data)
        $.ajax({
            url: '/accounts/userLogin/',
            method: 'POST',
            data: $form_data,
            cache: false,
            dataType: 'json',
            beforeSend: function(){
                $("#login-form-main-message").css("display", "block").html("<div class='alert alert-info'>  Please wait...</div>");
                $("#form_content").css("display", "none");
            },
            success: function(data){
                console.log("response data", data)
                if (data.status === "ok"){
                    if (data.to === "verify") {
                        //redirect to account verification
                    } else {
                        if (data.to === "user") {
                            //redirect to user account
                            $("#login-form-main-message").css("display", "block").html("<div class='alert alert-info'> Success! login you in, please wait...</div>");
                            $("#form_content").css("display", "none");
                            location.href = "{% url 'user:home' %}"
                        }else{
                            $("#login-form-main-message").css("display", "block").html("<div class='alert alert-success'> Success! login you in, please wait...</div>");
                            $("#form_content").css("display", "none");
                            location.href = '/em_dept/dashboard/';
                        }
                    }
                } else {
                    if (data.error == 'incorrect password') {
                        $("#form_content").css("display", "block");
                        $("#id_password").val('');
                        $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>Oops! Incorrect email or password</div>");
                        // location.href = "{% url 'login' %}";
                    }
                    else if (data.error === "account not found") {
                        $("#form_content").css("display", "block");
                        $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>Oops! Account not found</div>");
                        // location.href = "{% url 'login' %}";
                    }
                    else{
                        $("#login-form-main-message").css("display", "none");
                        $.each(data.form_errors, function (index, value) {
                            $("#form_errors").css('display', "block").append("<div class='alert alert-danger'>"+ value+"</div>")
                            // $('#error_'+index).css('display', "block").html(value);
                        } );
                        $("#form_content").css("display", "block");
                    }
                }
            },
            error:function(xhr,errmsg,err){
                console.log("error error error!!!");
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
        // return false;
    });
});