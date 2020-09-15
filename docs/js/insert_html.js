$.get("https://duckboss.github.io/JJMumbleBot/wiki/templates/navbar.html", function(data){
    $("#table_of_contents").html(data);
});
$.get("https://duckboss.github.io/JJMumbleBot/wiki/templates/footer.html", function(data){
    $("footer").html(data);
});
