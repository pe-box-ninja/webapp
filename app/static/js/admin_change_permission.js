function change_permission(userId, option_index) {
    alert("permission_options" + option_index)
    var new_permission = document.getElementById("permission_options" + option_index).value;
    /*     alert("Userid: " + userId);
        alert("new_permission: " + new_permission); */
    fetch('admin/change_permission', {
        method: 'POST',
        body: JSON.stringify({
            userId: userId, new_permission: new_permission
        }),
    }).then((_res) => {
        /* window.location.href = "/admin" */
    });
}