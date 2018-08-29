$(document).ready(function() {
    $("#menu-bar").click(function() {
        if($("#menu-bar-icon").hasClass('fa-arrows-alt')) {
            $("#menu-bar-icon").removeClass('fa-arrows-alt');
            $("#menu-bar-icon").addClass('fa-arrows-alt-h');
            $("#block-menu").show();
            $("body").css('overflow','hidden');
        } else {
            $("#menu-bar-icon").addClass('fa-arrows-alt');
            $("#menu-bar-icon").removeClass('fa-arrows-alt-h');
            $("#block-menu").hide();
            $("body").css('overflow','auto');
        }
    });
});