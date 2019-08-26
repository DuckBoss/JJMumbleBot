$(document).ready(function() {
    var cpu_data = 0;
    var ram_data = 0;
    var update_int = 1000;

    function updateInterval() {
        update_int = parseInt(document.getElementById('update-interval').value);
        console.log('updated interval: ' + update_int);
    }

    setInterval(() => socket.emit("get-cpu-info"), update_int);
    socket.on('get-cpu-info', function(data) {
        data = JSON.parse(data);
        cpu_data = parseInt(data.cpu);
        document.getElementById('diag-cpu-info').innerHTML = data.cpu+'%';
    });

    setInterval(() => socket.emit("get-ram-info"), update_int);
    socket.on('get-ram-info', function(data) {
        data = JSON.parse(data);
        ram_data = parseInt(data.ram);
        document.getElementById('diag-ram-info').innerHTML = data.ram+'%';
    });

    setInterval(() => socket.emit("get-online-clients"), update_int);
    // socket.emit("get-active-clients");
    socket.on('get-online-clients', function(data) {
        data = JSON.parse(data);
        document.getElementById('online-users').innerHTML = data.users;
    });

    // setInterval(() => socket.emit("get-whisper-clients"), 1000);
    // socket.emit("get-active-clients");
    socket.on('get-whisper-clients', function(data) {
        console.log(data);
        data = JSON.parse(data);
        document.getElementById('whisper-users').innerHTML = data.users;
        console.log(data);
    });


    var system_chart = new Chart(document.getElementById("system-info-chart"), {
            type: 'bar',
            data: {
              labels: ["CPU", "RAM"],
              datasets: [
                {
                  label: "Usage (%)",
                  backgroundColor: ["#3e95cd", "#8e5ea2"],
                  data: [0, 0]
                }
              ]
            },
            options: {
              animation: {
                easing: 'easeOutQuart',
                duration: 600
              },
              responsive: false,
              maintainAspectRatio: true,
              legend: { display: false },
              scales: {
                yAxes:[{
                    ticks: {
                        min: 0,
                        max: 100,
                        beginAtZero: true
                    }
                }]
              },
              title: {
                display: true,
                text: 'System Information'
              }
            }
    });
    function update_chart() {
        system_chart.data.datasets[0].data[0] = cpu_data;
        system_chart.data.datasets[0].data[1] = ram_data;
        system_chart.update();
        console.log('updated chart');
    }
    setInterval(() => update_chart(), update_int);



});