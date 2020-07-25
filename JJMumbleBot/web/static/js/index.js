function setChannelInformation() {
  var channel_list_fig = document.getElementById("channelsList");
  channel_list_fig.innerHTML = "";
  for (var chan_key of Object.keys(data_storage["channels"])) {
    var channel_name = document.createElement("figcaption");
    channel_name.innerHTML = data_storage["channels"][parseInt(chan_key)]["name"];
    channel_list_fig.appendChild(channel_name);

    var channel_list_ul = document.createElement("ul");
    channel_list_ul.classList.add("list-group");
    channel_list_ul.classList.add("list-group-flush");
    for (var user_key of Object.keys(data_storage["users"][parseInt(chan_key)])) {
        var user_li = document.createElement("li");
        user_li.classList.add("list-group-item");
        user_li.innerHTML = `${data_storage["users"][parseInt(chan_key)][user_key]["name"]}`;
        channel_list_ul.appendChild(user_li);
    }
    channel_list_fig.appendChild(channel_list_ul);
  }
}

// Function to download data to a file
function download(data, filename, type) {
    var file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}

function download_report() {
    download(JSON.stringify(data_storage), 'bot_report.json', 'text/plain')
}

function skipto_command (button_id) {
    $.ajax({
        type: 'POST',
        url: '/skipto',
        contentType: "application/json",
        data: JSON.stringify({'data': button_id})
    })
    setAudioQueueInformation();
};
function removetrack_command (button_id) {
    $.ajax({
        type: 'POST',
        url: '/removetrack',
        contentType: "application/json",
        data: JSON.stringify({'data': button_id})
    })
    setAudioQueueInformation();
};

