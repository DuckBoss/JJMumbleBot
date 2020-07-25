
// https://www.w3schools.com/howto/howto_js_tabs.asp
function openPage(evt, pageName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(pageName).style.display = "block";
  evt.currentTarget.className += " active";
}

function setAudioQueueInformation() {
  document.getElementById("audio-queue-table-body").innerHTML = "";
  var now_playing_text = document.getElementById("audio-queue-now-playing");
  now_playing_text.innerHTML = `Now Playing: ${data_storage["audio_data"]["track"]["name"]}`;

  var table_body = document.getElementById("audio-queue-table-body");
  var queue_item_count = 0
  for (var queue_item of Object.keys(data_storage["audio_data"]["queue"])) {
    var track_row = document.createElement("tr");
    var track_data = document.createElement("td");
    track_data.setAttribute("scope", "row");
    track_data.innerHTML = `<font color="cyan">[${queue_item_count}]</font> - ${data_storage["audio_data"]["queue"][queue_item]["name"]}`;

    track_row.appendChild(track_data);
    table_body.appendChild(track_row);
    queue_item_count++;
  }
}

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
