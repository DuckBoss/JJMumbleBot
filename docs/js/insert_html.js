$.get("https://duckboss.github.io/JJMumbleBot/pages/templates/navbar.html", function(data){
    $("#table_of_contents").html(data);
});
$.get("https://duckboss.github.io/JJMumbleBot/pages/templates/footer.html", function(data){
    $("footer").html(data);
});
