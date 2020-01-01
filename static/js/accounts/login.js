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
// var csrftoken = getCookie('csrftoken');

$("#login_submit").click(function(e) {
        console.log("clicked");
        e.preventDefault();
        var $formdata = $("#login_form").serializeArray();
        $formdata.push({
            name: "csrfmiddlewaretoken",
            value: getCookie('csrftoken')
        }
        );
        $.ajax({
            type: "POST",
            url: "/accounts/userLogin/",
            data: $formdata,
            beforeSend: function() {
                $("#login-form-main-message").css("display", "block").html("<div class='alert alert-info'><img height=\"24px;\" src=\"/static/images/double-ring.gif\" alt=\"loading\" />  Please wait...</div>");
                $("#form_content").css("display", "none");

            },
            cache: false,
            dataType: "json",
            success: function(data) {
                if (data.error === 'incorrect password') {
                    $("#form_content").css("display", "block");
                    $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>Email or Password Incorrect</div>");
                    // location.href = '/accounts/userLogin/';
                }

                if (data.error === 'account not found') {
                    $("#form_content").css("display", "block");
                    $("#login-form-main-message").css("display", "block").html("<div class='alert alert-danger'>Account not found</div>");
                    // location.href = '/accounts/userLogin/';
                }

                if (data.status === "ok") {
                    if (data.to !== "verify"){  
                        if (data.data === undefined) {
                            console.log('user_data is empty');
                        }else{
                            console.log('user_data is not empty');
                            existing_users_array = JSON.parse(localStorage.getItem("logedin_users") || "[]");
                            // console.log("existing_users_array is: ",existing_users_array);
                            found = false;
                            for (var i = 0; i < existing_users_array.length; i++) {
                                user_object_here = existing_users_array[i]
                                curr_id = user_object_here.data
                                // console.log("curr_id is: ",curr_id);
                                if (curr_id == data.data) {
                                    found = true;
                                    existing_users_array[i].data = data.data
                                    // remove the existing user for updating
                                    new_existing_users_array = existing_users_array.slice(i)
                                    console.log("new_existing_users_array 1 is: ",new_existing_users_array);
                                    // add the new user info for updating
                                    new_existing_users_array.push(data.data);
                                    // console.log("new_existing_users_array 2 is: ",new_existing_users_array);
                                    localStorage.setItem("logedin_users", JSON.stringify(existing_users_array));
                                    // console.log("localStorage true setItem is: ",JSON.parse(localStorage.getItem("logedin_users")));
                                    // console.log("login_phone_number existing for updating is: ",data.user_data.login_phone_number);
                                }
                            }
                            // console.log("found is: ",found);
                            if (found == false) {
                                existing_users_array.push(data.data);
                                localStorage.setItem("logedin_users", JSON.stringify(existing_users_array));
                                console.log("localStorage false setItem is: ",JSON.parse(localStorage.getItem("logedin_users")));
                            }
                        }
                        location.href = "/em_dept/dashboard/";
                    }else{
                        $("#login-form-main-message").css("display", "block").html("");
                        $("#form_content").css("display", "none");
                        $("#second_content").css("display", "block");
                    }

                }
            }
        });
        return false;
    });