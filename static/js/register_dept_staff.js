// using jQuery
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


$('#register_submit').click(function (e) {
    console.log("clicked here");
    // body...
    e.preventDefault();
    var $formdata = $('#register_dept_staff').serializeArray();
    console.log("Form data", $formdata);
    $formdata.push({
        name: "csrfmiddlewaretoken",
        value: getCookie('csrftoken')
    }
    );
    $.ajax({
        type:'POST',
        url:'/accounts/registerDeptStaff/',
        data:$formdata,
        beforeSend: function () {
            console.log("past url def");
            // body...
            $("#login-form-main-message").css("display", "block").html("<div class='alert alert-info'><img height=\"24px;\" src=\"/static/img/double-ring.gif\" alt=\"loading\" />  Please wait...</div>");
            $(".form_content").css("display", "none");
        },
        cache:false,
        dataType:"json",
        success: function (data) {
            if (data.status === "fail" ) {
                $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>"+data.error+"</div>");
                $("#form_content").css("display", "block");
            }
            if (data.status === "success") {
                $("#form_content").css("display", "none");
                $("#login-form-main-message").css("display", "block").html("<div class='alert alert-success'>"+"user"+data.email+"registered"+"</div>");
                if (data.user === 1) {
                    setTimeout(location.href='/police/home/', 3000);
                }
                if (data.user === 2) {
                    setTimeout(location.href='/health/home/', 3000);
                }
                if (data.user === 3) {
                    setTimeout(location.href='/PrivateEmReponse/home/', 3000);
                }
                if (data.user === 4) {
                    setTimeout(location.href='/deptAdmin/home/', 3000);
                }
                if (data.user === 4) {
                    setTimeout(location.href='/admin/home/', 3000);
                }
            }
        }

    });

});