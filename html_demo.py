charts_html_code="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relationship between Pollutant amount and Weather Temperature</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #fff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 80%;
            max-width: 800px;
        }
        canvas {
            border-radius: 8px;
        }
        .tooltip {
            position: absolute;
            background: #333;
            color: #fff;
            border-radius: 4px;
            padding: 5px;
            font-size: 12px;
            pointer-events: none;
            z-index: 100;
            display: none;
        }

        .tooltip::after {
            content: ' ';
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #333 transparent transparent transparent;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<div class="container">
    <canvas id="lineChart"></canvas>
    <div id="tooltip" class="tooltip"></div>
</div>

<script>
    const searched_result = [
        {"date": "2014-08-01", "average_particullate_matter": 66.81935854356952, "average_temperature": 21.4},
        {"date": "2014-08-02", "average_particullate_matter": 80.37908314773571, "average_temperature": 22.7},
        {"date": "2014-08-03", "average_particullate_matter": 91.33991431576344, "average_temperature": 21.8},
        {"date": "2014-08-04", "average_particullate_matter": 99.42586148230636, "average_temperature": 19.4},
        {"date": "2014-08-05", "average_particullate_matter": 105.38195991091314, "average_temperature": 17.8},
        {"date": "2014-08-06", "average_particullate_matter": 108.35381093788666, "average_temperature": 18.5},
        {"date": "2014-08-07", "average_particullate_matter": 110.84666542934916, "average_temperature": 18.9},
        {"date": "2014-08-08", "average_particullate_matter": 112.6560257362039, "average_temperature": 19.5},
        {"date": "2014-08-09", "average_particullate_matter": 66.81935854356952, "average_temperature": 18.7},
        {"date": "2014-08-10", "average_particullate_matter": 114.32433958178667, "average_temperature": 19.3},
        {"date": "2014-08-11", "average_particullate_matter": 114.97595737441227, "average_temperature": 18.6},
        {"date": "2014-08-12", "average_particullate_matter": 115.01903148973028, "average_temperature": 16.5},
        {"date": "2014-08-13", "average_particullate_matter": 113.60746102449887, "average_temperature": 15.5},
        {"date": "2014-08-14", "average_particullate_matter": 112.14771250927988, "average_temperature": 16.8},
        {"date": "2014-08-15", "average_particullate_matter": 66.81935854356952, "average_temperature": 16.5},
        {"date": "2014-08-16", "average_particullate_matter": 110.57477264291016, "average_temperature": 14.8},
        {"date": "2014-08-17", "average_particullate_matter": 113.3337973273942, "average_temperature": 14.5},
        {"date": "2014-08-18", "average_particullate_matter": 115.7442078074734, "average_temperature": 14.1},
        {"date": "2014-08-19", "average_particullate_matter": 115.92222686216284, "average_temperature": 13.9},
        {"date": "2014-08-20", "average_particullate_matter": 117.02104986389509, "average_temperature": 14.5},
        {"date": "2014-08-21", "average_particullate_matter": 113.32641982182628, "average_temperature": 13.6},
        {"date": "2014-08-22", "average_particullate_matter": 66.81935854356952, "average_temperature": 13.8},
        {"date": "2014-08-23", "average_particullate_matter": 114.55720273447167, "average_temperature": 13.4},
        {"date": "2014-08-24", "average_particullate_matter": 115.23164903489234, "average_temperature": 12.6},
        {"date": "2014-08-25", "average_particullate_matter": 114.21977852016828, "average_temperature": 13.5},
        {"date": "2014-08-26", "average_particullate_matter": 116.10501732244497, "average_temperature": 14.2},
        {"date": "2014-08-27", "average_particullate_matter": 117.7142492576095, "average_temperature": 14.7},
        {"date": "2014-08-28", "average_particullate_matter": 114.5087617545162, "average_temperature": 14.6},
        {"date": "2014-08-29", "average_particullate_matter": 114.9814789037367, "average_temperature": 14.8},
        {"date": "2014-08-30", "average_particullate_matter": 114.79759032417718, "average_temperature": 15.1},
        {"date": "2014-08-31", "average_particullate_matter": 118.4754469809453, "average_temperature": 15.4},
        {"date": "2014-09-01", "average_particullate_matter": 119.6681901138332, "average_temperature": 16.2},
        {"date": "2014-09-02", "average_particullate_matter": 120.34119803266518, "average_temperature": 15.5},
        {"date": "2014-09-03", "average_particullate_matter": 117.8618844345459, "average_temperature": 14.7},
        {"date": "2014-09-04", "average_particullate_matter": 115.7634403612967, "average_temperature": 14.3},
        {"date": "2014-09-05", "average_particullate_matter": 114.69497803761446, "average_temperature": 14.3},
        {"date": "2014-09-06", "average_particullate_matter": 115.93497123236824, "average_temperature": 18.6},
        {"date": "2014-09-07", "average_particullate_matter": 115.90604893590697, "average_temperature": 17.4},
        {"date": "2014-09-08", "average_particullate_matter": 114.18689680772086, "average_temperature": 13.5},
        {"date": "2014-09-09", "average_particullate_matter": 111.43518776292996, "average_temperature": 15.2},
        {"date": "2014-09-10", "average_particullate_matter": 112.76928668646374, "average_temperature": 14.7},
        {"date": "2014-09-11", "average_particullate_matter": 112.58236667903984, "average_temperature": 15.8},
        {"date": "2014-09-12", "average_particullate_matter": 111.58464024993812, "average_temperature": 14.5},
        {"date": "2014-09-13", "average_particullate_matter": 66.81935854356952, "average_temperature": 15.7},
        {"date": "2014-09-14", "average_particullate_matter": 110.20188381588716, "average_temperature": 16.7},
        {"date": "2014-09-15", "average_particullate_matter": 111.26392755506062, "average_temperature": 16.8},
        {"date": "2014-09-16", "average_particullate_matter": 109.3392647240782, "average_temperature": 16.2},
        {"date": "2014-09-17", "average_particullate_matter": 110.61387960900768, "average_temperature": 15.2},
        {"date": "2014-09-18", "average_particullate_matter": 114.75792656520665, "average_temperature": 16.6},
        {"date": "2014-09-19", "average_particullate_matter": 116.25957374412272, "average_temperature": 14.9},
        {"date": "2014-09-20", "average_particullate_matter": 115.90875556792874, "average_temperature": 13.2},
        {"date": "2014-09-21", "average_particullate_matter": 117.11045378619154, "average_temperature": 14.3},
        {"date": "2014-09-22", "average_particullate_matter": 116.88960807968326, "average_temperature": 10.6},
        {"date": "2014-09-23", "average_particullate_matter": 115.45029076961148, "average_temperature": 10.0},
        {"date": "2014-09-24", "average_particullate_matter": 115.60388827023014, "average_temperature": 12.8},
        {"date": "2014-09-25", "average_particullate_matter": 113.8519472284088, "average_temperature": 12.4},
        {"date": "2014-09-26", "average_particullate_matter": 111.65567774065823, "average_temperature": 14.8},
        {"date": "2014-09-27", "average_particullate_matter": 112.37465973768867, "average_temperature": 13.2},
        {"date": "2014-09-28", "average_particullate_matter": 113.68006836179164, "average_temperature": 14.2},
        {"date": "2014-09-29", "average_particullate_matter": 114.92324764909677, "average_temperature": 15.3},
        {"date": "2014-09-30", "average_particullate_matter": 113.1759899343418, "average_temperature": 14.1}
        ];

    const data = {
        labels: searched_result.map(item => item.date),
        datasets: [{
            label: 'Particulates 🌫️',
            data: searched_result.map(item => item.average_particullate_matter),
            borderColor: 'rgb(255, 99, 132)',
            fill: false,
            tension: 0.1
        }, {
            label: 'Temperature 🌡️',
            data: searched_result.map(item => item.average_temperature),
            borderColor: 'rgb(54, 162, 235)',
            fill: false,
            tension: 0.1
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                tooltip: {
                    enabled: false,
                    external: function(context) {
                        const tooltipEl = document.getElementById('tooltip');
                        if (context.tooltip.opacity === 0) {
                            tooltipEl.style.opacity = 0;
                            return;
                        }

                        const dataIndex = context.tooltip.dataPoints[0].dataIndex;
                        tooltipEl.innerHTML = `
                            <strong>Date:</strong> ${searched_result[dataIndex].date}<br>
                            💨 <strong>Particulates:</strong> ${searched_result[dataIndex].average_particullate_matter.toFixed(2)}<br>
                            🌡️ <strong>Temperature:</strong> ${searched_result[dataIndex].average_temperature.toFixed(1)} °C
                        `;

                        const position = context.chart.canvas.getBoundingClientRect();
                        tooltipEl.style.opacity = 1;
                        tooltipEl.style.left = position.left + window.pageXOffset + context.tooltip.caretX - (tooltipEl.offsetWidth / 2) + 'px';
                        tooltipEl.style.top = position.top + window.pageYOffset + context.tooltip.caretY - tooltipEl.offsetHeight - 10 + 'px';
                    }
                },
            },
            scales: {
                x: {
                    grid: {
                        display: true,
                        borderDash: [8, 4],
                    }
                },
                y: {
                    grid: {
                        display: true,
                        borderDash: [8, 4],
                    }
                }
            }
        }
    };

    const lineChart = new Chart(
        document.getElementById('lineChart'),
        config
    );
</script>

</body>
</html>
"""
events_html_code="""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title></title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f9f9f9;
    }
    .calendar {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 10px;
      padding: 20px;
      max-width: 1200px;
      margin: auto;
    }
    .day {
      background: #ffffff;
      border-radius: 15px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      padding: 10px;
      text-align: center;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .day:hover {
      transform: scale(1.05);
      background-color: #e3f2fd;
    }
    .date {
      font-size: 1.2em;
      font-weight: bold;
    }
    .weather {
      font-size: 2em;
      margin: 10px 0;
    }
    .pollution {
      font-size: 0.9em;
      color: #555;
    }
    .highlight {
      background-color: #fff9c4 !important;
    }
    .tooltip {
      display: none;
      position: absolute;
      background: #ffffff;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      padding: 15px;
      z-index: 10;
      animation: fadeIn 0.3s ease;
      width: 300px;
    }
    .day:hover .tooltip {
      display: block;
    }
    .map {
      height: 200px;
      width: 100%;
      margin-top: 10px;
      border-radius: 10px;
    }
  </style>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
<div class="calendar" id="calendar"></div>

<script>
  const searched_result = [
    {"city": "Aarhus", "title": "Mandagsfilm i bÃ¸rnebiblioteket", "price": "0", "library": "Hovedbiblioteket", "longitude": 10.200179, "latitude": 56.156617, "date": "2014-08-04"},
    {"city": "Aarhus", "title": "International Playgroup", "price": "0", "library": "Hovedbiblioteket", "longitude": 10.200179, "latitude": 56.156617, "date": "2014-08-01"},
    {"city": "Aarhus", "title": "International Playgroup", "price": "0", "library": "Hovedbiblioteket", "longitude": 10.200179, "latitude": 56.156617, "date": "2014-08-15"},
    {"city": "Viby J", "title": "Bustur til Store Bogdag ved Hald Hovedgaard lÃ¸rdag 9. august", "price": "110", "library": "Viby Bibliotek", "longitude": 10.164431, "latitude": 56.130402, "date": "2014-08-09"},
    {"city": "Aarhus V", "title": "Forfatterspirer - SAXOs forfatterklub", "price": "0", "library": "Hasle Bibliotek", "longitude": 10.167345, "latitude": 56.179458, "date": "2014-08-04"},
    {"city": "Aarhus", "title": "ByggelÃ¸rdag", "price": "0", "library": "Hovedbiblioteket", "longitude": 10.200179, "latitude": 56.156617, "date": "2014-08-09"},
    {"city": "Viby J", "title": "Artmoney â?penge med dobbeltvÃ¦rdi ", "price": "0", "library": "Viby Bibliotek", "longitude": 10.164431, "latitude": 56.130402, "date": "2014-08-01"}
  ];

  const pollutionData = [
    {"date": "2014-08-01", "average_particullate_matter": 66.81935854356952, "pollution_condition": "Good"},
    {"date": "2014-08-02", "average_particullate_matter": 80.37908314773571, "pollution_condition": "Good"},
    {"date": "2014-08-03", "average_particullate_matter": 91.33991431576344, "pollution_condition": "Good"},
    {"date": "2014-08-04", "average_particullate_matter": 99.42586148230636, "pollution_condition": "Good"},
    {"date": "2014-08-05", "average_particullate_matter": 105.38195991091314, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-06", "average_particullate_matter": 108.35381093788666, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-07", "average_particullate_matter": 110.84666542934916, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-08", "average_particullate_matter": 112.6560257362039, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-09", "average_particullate_matter": 66.81935854356952, "pollution_condition": "Good"},
    {"date": "2014-08-10", "average_particullate_matter": 114.32433958178667, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-11", "average_particullate_matter": 114.97595737441227, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-12", "average_particullate_matter": 115.01903148973028, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-13", "average_particullate_matter": 113.60746102449887, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-14", "average_particullate_matter": 112.14771250927988, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-15", "average_particullate_matter": 66.81935854356952, "pollution_condition": "Good"},
    {"date": "2014-08-16", "average_particullate_matter": 110.57477264291016, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-17", "average_particullate_matter": 113.3337973273942, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-18", "average_particullate_matter": 115.7442078074734, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-19", "average_particullate_matter": 115.92222686216284, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-20", "average_particullate_matter": 117.02104986389509, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-21", "average_particullate_matter": 113.32641982182628, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-22", "average_particullate_matter": 66.81935854356952, "pollution_condition": "Good"},
    {"date": "2014-08-23", "average_particullate_matter": 114.55720273447167, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-24", "average_particullate_matter": 115.23164903489234, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-25", "average_particullate_matter": 114.21977852016828, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-26", "average_particullate_matter": 116.10501732244497, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-27", "average_particullate_matter": 117.7142492576095, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-28", "average_particullate_matter": 114.5087617545162, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-29", "average_particullate_matter": 114.9814789037367, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-30", "average_particullate_matter": 114.79759032417718, "pollution_condition": "Unhealthy"},
    {"date": "2014-08-31", "average_particullate_matter": 118.4754469809453, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-01", "average_particullate_matter": 119.6681901138332, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-02", "average_particullate_matter": 120.34119803266518, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-03", "average_particullate_matter": 117.8618844345459, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-04", "average_particullate_matter": 115.7634403612967, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-05", "average_particullate_matter": 114.69497803761446, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-06", "average_particullate_matter": 115.93497123236824, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-07", "average_particullate_matter": 115.90604893590697, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-08", "average_particullate_matter": 114.18689680772086, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-09", "average_particullate_matter": 111.43518776292996, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-10", "average_particullate_matter": 112.76928668646374, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-11", "average_particullate_matter": 112.58236667903984, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-12", "average_particullate_matter": 111.58464024993812, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-13", "average_particullate_matter": 66.81935854356952, "pollution_condition": "Good"},
    {"date": "2014-09-14", "average_particullate_matter": 110.20188381588716, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-15", "average_particullate_matter": 111.26392755506062, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-16", "average_particullate_matter": 109.3392647240782, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-17", "average_particullate_matter": 110.61387960900768, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-18", "average_particullate_matter": 114.75792656520665, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-19", "average_particullate_matter": 116.25957374412272, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-20", "average_particullate_matter": 115.90875556792874, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-21", "average_particullate_matter": 117.11045378619154, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-22", "average_particullate_matter": 116.88960807968326, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-23", "average_particullate_matter": 115.45029076961148, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-24", "average_particullate_matter": 115.60388827023014, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-25", "average_particullate_matter": 113.8519472284088, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-26", "average_particullate_matter": 111.65567774065823, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-27", "average_particullate_matter": 112.37465973768867, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-28", "average_particullate_matter": 113.68006836179164, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-29", "average_particullate_matter": 114.92324764909677, "pollution_condition": "Unhealthy"},
    {"date": "2014-09-30", "average_particullate_matter": 113.1759899343418, "pollution_condition": "Unhealthy"},
    {"date": "2014-10-01", "average_particullate_matter": 111.90848214285714, "pollution_condition": "Unhealthy"}
  ];

  const weatherData = [
    {"date": "2014-08-01", "weather": "☀️", "average_temperature": 21.4, "average_wind_speed": 10.1},
    {"date": "2014-08-02", "weather": "☀️", "average_temperature": 22.7, "average_wind_speed": 16.8},
    {"date": "2014-08-03", "weather": "🌧️", "average_temperature": 21.8, "average_wind_speed": 9.4},
    {"date": "2014-08-04", "weather": "🌤️", "average_temperature": 19.4, "average_wind_speed": 10.7},
    {"date": "2014-08-05", "weather": "🌧️", "average_temperature": 17.8, "average_wind_speed": 5.1},
    {"date": "2014-08-06", "weather": "🌤️", "average_temperature": 18.5, "average_wind_speed": 8.3},
    {"date": "2014-08-07", "weather": "🌤️", "average_temperature": 18.9, "average_wind_speed": 6.6},
    {"date": "2014-08-08", "weather": "🌤️", "average_temperature": 19.5, "average_wind_speed": 7.7},
    {"date": "2014-08-09", "weather": "🌤️", "average_temperature": 18.7, "average_wind_speed": 15.4},
    {"date": "2014-08-10", "weather": "🌤️", "average_temperature": 19.3, "average_wind_speed": 14.8},
    {"date": "2014-08-11", "weather": "🌤️", "average_temperature": 18.6, "average_wind_speed": 16.4},
    {"date": "2014-08-12", "weather": "❄️", "average_temperature": 16.5, "average_wind_speed": 13.0},
    {"date": "2014-08-13", "weather": "🌧️", "average_temperature": 15.5, "average_wind_speed": 9.7},
    {"date": "2014-08-14", "weather": "🌤️", "average_temperature": 16.8, "average_wind_speed": 12.0},
    {"date": "2014-08-15", "weather": "🌤️", "average_temperature": 16.5, "average_wind_speed": 13.6},
    {"date": "2014-08-16", "weather": "❄️", "average_temperature": 14.8, "average_wind_speed": 20.7},
    {"date": "2014-08-17", "weather": "🌧️", "average_temperature": 14.5, "average_wind_speed": 11.8},
    {"date": "2014-08-18", "weather": "❄️", "average_temperature": 14.1, "average_wind_speed": 15.3},
    {"date": "2014-08-19", "weather": "❄️", "average_temperature": 13.9, "average_wind_speed": 22.5},
    {"date": "2014-08-20", "weather": "❄️", "average_temperature": 14.5, "average_wind_speed": 23.1},
    {"date": "2014-08-21", "weather": "❄️", "average_temperature": 13.6, "average_wind_speed": 16.3},
    {"date": "2014-08-22", "weather": "❄️", "average_temperature": 13.8, "average_wind_speed": 11.9},
    {"date": "2014-08-23", "weather": "❄️", "average_temperature": 13.4, "average_wind_speed": 13.3},
    {"date": "2014-08-24", "weather": "❄️", "average_temperature": 12.6, "average_wind_speed": 18.8},
    {"date": "2014-08-25", "weather": "❄️", "average_temperature": 13.5, "average_wind_speed": 18.2},
    {"date": "2014-08-26", "weather": "❄️", "average_temperature": 14.2, "average_wind_speed": 10.8},
    {"date": "2014-08-27", "weather": "❄️", "average_temperature": 14.7, "average_wind_speed": 10.4},
    {"date": "2014-08-28", "weather": "❄️", "average_temperature": 14.6, "average_wind_speed": 8.6},
    {"date": "2014-08-29", "weather": "🌧️", "average_temperature": 14.8, "average_wind_speed": 8.5},
    {"date": "2014-08-30", "weather": "🌧️", "average_temperature": 15.1, "average_wind_speed": 9.4},
    {"date": "2014-08-31", "weather": "🌧️", "average_temperature": 15.4, "average_wind_speed": 15.1},
    {"date": "2014-09-01", "weather": "🌤️", "average_temperature": 16.2, "average_wind_speed": 13.9},
    {"date": "2014-09-02", "weather": "❄️", "average_temperature": 15.5, "average_wind_speed": 5.6},
    {"date": "2014-09-03", "weather": "❄️", "average_temperature": 14.7, "average_wind_speed": 5.8},
    {"date": "2014-09-04", "weather": "❄️", "average_temperature": 14.3, "average_wind_speed": 7.3},
    {"date": "2014-09-05", "weather": "🌧️", "average_temperature": 14.3, "average_wind_speed": 8.3},
    {"date": "2014-09-06", "weather": "🌤️", "average_temperature": 18.6, "average_wind_speed": 12.5},
    {"date": "2014-09-07", "weather": "🌧️", "average_temperature": 17.4, "average_wind_speed": 7.7},
    {"date": "2014-09-08", "weather": "🌧️", "average_temperature": 13.5, "average_wind_speed": 11.5},
    {"date": "2014-09-09", "weather": "🌧️", "average_temperature": 15.2, "average_wind_speed": 21.6},
    {"date": "2014-09-10", "weather": "🌧️", "average_temperature": 14.7, "average_wind_speed": 13.1},
    {"date": "2014-09-11", "weather": "🌧️", "average_temperature": 15.8, "average_wind_speed": 10.2},
    {"date": "2014-09-12", "weather": "🌧️", "average_temperature": 14.5, "average_wind_speed": 6.8},
    {"date": "2014-09-13", "weather": "🌧️", "average_temperature": 15.7, "average_wind_speed": 10.6},
    {"date": "2014-09-14", "weather": "🌧️", "average_temperature": 16.7, "average_wind_speed": 19.6},
    {"date": "2014-09-15", "weather": "🌧️", "average_temperature": 16.8, "average_wind_speed": 20.3},
    {"date": "2014-09-16", "weather": "🌤️", "average_temperature": 16.2, "average_wind_speed": 17.6},
    {"date": "2014-09-17", "weather": "🌧️", "average_temperature": 15.2, "average_wind_speed": 13.9},
    {"date": "2014-09-18", "weather": "🌧️", "average_temperature": 16.6, "average_wind_speed": 14.8},
    {"date": "2014-09-19", "weather": "🌧️", "average_temperature": 14.9, "average_wind_speed": 10.9},
    {"date": "2014-09-20", "weather": "🌧️", "average_temperature": 13.2, "average_wind_speed": 3.5},
    {"date": "2014-09-21", "weather": "❄️", "average_temperature": 14.3, "average_wind_speed": 15.4},
    {"date": "2014-09-22", "weather": "❄️", "average_temperature": 10.6, "average_wind_speed": 19.5},
    {"date": "2014-09-23", "weather": "❄️", "average_temperature": 10.0, "average_wind_speed": 6.5},
    {"date": "2014-09-24", "weather": "🌧️", "average_temperature": 12.8, "average_wind_speed": 9.5},
    {"date": "2014-09-25", "weather": "❄️", "average_temperature": 12.4, "average_wind_speed": 18.2},
    {"date": "2014-09-26", "weather": "🌧️", "average_temperature": 14.8, "average_wind_speed": 16.1},
    {"date": "2014-09-27", "weather": "❄️", "average_temperature": 13.2, "average_wind_speed": 18.3},
    {"date": "2014-09-28", "weather": "❄️", "average_temperature": 14.2, "average_wind_speed": 11.8},
    {"date": "2014-09-29", "weather": "🌧️", "average_temperature": 15.3, "average_wind_speed": 7.5},
    {"date": "2014-09-30", "weather": "❄️", "average_temperature": 14.1, "average_wind_speed": 10.0}
  ];


  const calendarEl = document.getElementById('calendar');
  const monthDays = Array.from({ length: 31 }, (_, i) => i + 1);
  const maps = {}; // Store map instances to prevent reinitialization

  monthDays.forEach(day => {
    const dayStr = `2014-08-${day.toString().padStart(2, '0')}`;
    const weather = weatherData.find(w => w.date === dayStr);
    const pollution = pollutionData.find(p => p.date === dayStr);
    const event = searched_result.find(e => e.date === dayStr);

    const dayEl = document.createElement('div');
    dayEl.classList.add('day');

    if (event) {
      dayEl.classList.add('highlight');
    }

    dayEl.innerHTML = `
                <div class="date">${day}</div>
                <div class="weather">${weather ? weather.weather : '🌥️'}</div>
                <div class="pollution">${pollution ? `Air Quaility:${pollution.pollution_condition}` : ''}</div>
                ${event ? `<div class="tooltip animate__animated animate__fadeIn">
                    <strong>${event.title}</strong><br>
                    <p>🏢: ${event.city}, 💵: ${event.price}</p>
                    <div id="map${day}" class="map"></div>
                </div>` : ''}
            `;

    calendarEl.appendChild(dayEl);

    if (event) {
      dayEl.addEventListener('mouseenter', () => {
        const mapId = `map${day}`;
        const mapEl = document.getElementById(mapId);
        if (!maps[mapId]) {
          const map = L.map(mapEl).setView([event.latitude, event.longitude], 13);
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
          }).addTo(map);
          L.marker([event.latitude, event.longitude]).addTo(map)
                  .bindPopup("📖: " +event.library)
                  .openPopup();
          maps[mapId] = map; // Store the map instance
        }
      });
    }
  });
</script>
</body>
</html>

"""
route_html_code="""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title> </title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
        }
        .container {
            width: 80%;
            margin: auto;
            padding: 20px;
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        #map {
            height: 500px;
            border-radius: 15px;
        }
        .route-rank-buttons {
            text-align: center;
            margin-top: 20px;
        }
        .route-rank-buttons button {
            margin: 5px;
            padding: 10px 20px;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .route-rank-buttons button:hover {
            background-color: #ddd;
        }
        .route-details {
            margin-top: 20px;
            padding: 10px;
            background-color: #ececec;
            border-radius: 10px;
        }
        .route-segment {
            margin-top: 10px;
            padding: 10px;
            border-radius: 10px;
            transition: background-color 0.2s;
            cursor: pointer;
            position: relative;
        }
        .route-segment:hover {
            background-color: #ddd;
        }
        .tooltip {
            position: absolute;
            top: -10px;
            right: 10px;
            background-color: white;
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: none;
            z-index: 1000;
        }
        .route-segment:hover .tooltip {
            display: block;
        }
        .emoji {
            font-size: 1.2em;
        }
    </style>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
</head>
<body>

<div class="container">
    <h2>Route Plan</h2>
    <div id="map"></div>

    <div class="route-rank-buttons">
        <button onclick="displayRoute(1)">Route rank 1</button>
        <button onclick="displayRoute(2)">Route rank 2</button>
        <button onclick="displayRoute(3)">Route rank 3</button>
    </div>

    <div class="route-details" id="route-details">
        <p>Pick a route to see details</p>
    </div>
</div>

<script>
    // Mock data structure for searched_result for demonstration
    const searched_result = [
        {"route_rank": 1, "path": [{"REPORT_ID": "WALKING", "DURATION_IN_SEC": 53.0, "POINT_1_LNG": 10.21284, "POINT_1_LAT": 56.16184, "POINT_2_LNG": 10.21197608217426, "POINT_2_LAT": 56.161017815103236, "VELOCITY": 2.0}, {"REPORT_ID": "190100", "DURATION_IN_SEC": 202.0, "POINT_1_LNG": 10.21197608217426, "POINT_1_LAT": 56.161017815103236, "POINT_2_LNG": 10.209599775463175, "POINT_2_LAT": 56.14892750591274, "VELOCITY": 7.4}, {"REPORT_ID": "179009", "DURATION_IN_SEC": 49.0, "POINT_1_LNG": 10.20872971106246, "POINT_1_LAT": 56.144719132186395, "POINT_2_LNG": 10.209599775463175, "POINT_2_LAT": 56.14892750591274, "VELOCITY": 9.7}, {"REPORT_ID": "206475", "DURATION_IN_SEC": 48.0, "POINT_1_LNG": 10.204415905418273, "POINT_1_LAT": 56.14171141881423, "POINT_2_LNG": 10.20872971106246, "POINT_2_LAT": 56.144719132186395, "VELOCITY": 9.9}, {"REPORT_ID": "179038", "DURATION_IN_SEC": 36.0, "POINT_1_LNG": 10.1989185595246, "POINT_1_LAT": 56.14063267124548, "POINT_2_LNG": 10.204415905418273, "POINT_2_LAT": 56.14171141881423, "VELOCITY": 10.0}, {"REPORT_ID": "206131", "DURATION_IN_SEC": 62.0, "POINT_1_LNG": 10.192723647815683, "POINT_1_LAT": 56.1417522836526, "POINT_2_LNG": 10.1989185595246, "POINT_2_LAT": 56.14063267124548, "VELOCITY": 8.1}, {"REPORT_ID": "206184", "DURATION_IN_SEC": 72.0, "POINT_1_LNG": 10.192723647815683, "POINT_1_LAT": 56.1417522836526, "POINT_2_LNG": 10.186632644180236, "POINT_2_LAT": 56.13959744418457, "VELOCITY": 10.3}, {"REPORT_ID": "190206", "DURATION_IN_SEC": 46.0, "POINT_1_LNG": 10.186632644180236, "POINT_1_LAT": 56.13959744418457, "POINT_2_LNG": 10.179150601188667, "POINT_2_LAT": 56.13844851575673, "VELOCITY": 11.1}, {"REPORT_ID": "184675", "DURATION_IN_SEC": 89.0, "POINT_1_LNG": 10.179150601188667, "POINT_1_LAT": 56.13844851575673, "POINT_2_LNG": 10.166163050262412, "POINT_2_LAT": 56.131053962866226, "VELOCITY": 12.9}, {"REPORT_ID": "WALKING", "DURATION_IN_SEC": 64.8, "POINT_1_LNG": 10.166163050262412, "POINT_1_LAT": 56.131053962866226, "POINT_2_LNG": 10.164431, "POINT_2_LAT": 56.130402, "VELOCITY": 2.0}], "total_duration": 721.7, "total_distance": 5941.4, "average_velocity": 8.2},
        {"route_rank": 2, "path": [{"REPORT_ID": "WALKING", "DURATION_IN_SEC": 53.0, "POINT_1_LNG": 10.21284, "POINT_1_LAT": 56.16184, "POINT_2_LNG": 10.21197608217426, "POINT_2_LAT": 56.161017815103236, "VELOCITY": 2.0}, {"REPORT_ID": "190100", "DURATION_IN_SEC": 202.0, "POINT_1_LNG": 10.21197608217426, "POINT_1_LAT": 56.161017815103236, "POINT_2_LNG": 10.209599775463175, "POINT_2_LAT": 56.14892750591274, "VELOCITY": 7.4}, {"REPORT_ID": "179009", "DURATION_IN_SEC": 49.0, "POINT_1_LNG": 10.20872971106246, "POINT_1_LAT": 56.144719132186395, "POINT_2_LNG": 10.209599775463175, "POINT_2_LAT": 56.14892750591274, "VELOCITY": 9.7}, {"REPORT_ID": "206475", "DURATION_IN_SEC": 48.0, "POINT_1_LNG": 10.204415905418273, "POINT_1_LAT": 56.14171141881423, "POINT_2_LNG": 10.20872971106246, "POINT_2_LAT": 56.144719132186395, "VELOCITY": 9.9}, {"REPORT_ID": "179038", "DURATION_IN_SEC": 36.0, "POINT_1_LNG": 10.1989185595246, "POINT_1_LAT": 56.14063267124548, "POINT_2_LNG": 10.204415905418273, "POINT_2_LAT": 56.14171141881423, "VELOCITY": 10.0}, {"REPORT_ID": "206131", "DURATION_IN_SEC": 62.0, "POINT_1_LNG": 10.192723647815683, "POINT_1_LAT": 56.1417522836526, "POINT_2_LNG": 10.1989185595246, "POINT_2_LAT": 56.14063267124548, "VELOCITY": 8.1}, {"REPORT_ID": "206078", "DURATION_IN_SEC": 62.0, "POINT_1_LNG": 10.186880262565637, "POINT_1_LAT": 56.14251885276732, "POINT_2_LNG": 10.192723647815683, "POINT_2_LAT": 56.1417522836526, "VELOCITY": 8.4}, {"REPORT_ID": "184703", "DURATION_IN_SEC": 60.0, "POINT_1_LNG": 10.179336344162948, "POINT_1_LAT": 56.138322977998705, "POINT_2_LNG": 10.186880262565637, "POINT_2_LAT": 56.14251885276732, "VELOCITY": 11.0}, {"REPORT_ID": "184649", "DURATION_IN_SEC": 93.0, "POINT_1_LNG": 10.166318618385276, "POINT_1_LAT": 56.13096577062022, "POINT_2_LNG": 10.179336344162948, "POINT_2_LAT": 56.138322977998705, "VELOCITY": 12.4}, {"REPORT_ID": "WALKING", "DURATION_IN_SEC": 66.4, "POINT_1_LNG": 10.166318618385276, "POINT_1_LAT": 56.13096577062022, "POINT_2_LNG": 10.164431, "POINT_2_LAT": 56.130402, "VELOCITY": 2.0}], "total_duration": 731.3, "total_distance": 5876.6, "average_velocity": 8.0},
        {"route_rank": 3, "path": [{"REPORT_ID": "WALKING", "DURATION_IN_SEC": 47.1, "POINT_1_LNG": 10.21284, "POINT_1_LAT": 56.16184, "POINT_2_LNG": 10.2121812711639, "POINT_2_LAT": 56.16107681293822, "VELOCITY": 2.0}, {"REPORT_ID": "182683", "DURATION_IN_SEC": 75.0, "POINT_1_LNG": 10.2121812711639, "POINT_1_LAT": 56.16107681293822, "POINT_2_LNG": 10.207060089618722, "POINT_2_LAT": 56.16816672029917, "VELOCITY": 11.3}, {"REPORT_ID": "187774", "DURATION_IN_SEC": 90.0, "POINT_1_LNG": 10.207060089618722, "POINT_1_LAT": 56.16816672029917, "POINT_2_LNG": 10.201380373016264, "POINT_2_LAT": 56.17122707649042, "VELOCITY": 7.1}, {"REPORT_ID": "180872", "DURATION_IN_SEC": 43.0, "POINT_1_LNG": 10.201380373016264, "POINT_1_LAT": 56.17122707649042, "POINT_2_LNG": 10.194338714120931, "POINT_2_LAT": 56.16945046812791, "VELOCITY": 11.2}, {"REPORT_ID": "180926", "DURATION_IN_SEC": 67.0, "POINT_1_LNG": 10.194338714120931, "POINT_1_LAT": 56.16945046812791, "POINT_2_LNG": 10.185844404928275, "POINT_2_LAT": 56.163969409207326, "VELOCITY": 12.1}, {"REPORT_ID": "180980", "DURATION_IN_SEC": 45.0, "POINT_1_LNG": 10.185844404928275, "POINT_1_LAT": 56.163969409207326, "POINT_2_LNG": 10.182659856483497, "POINT_2_LAT": 56.15898299999999, "VELOCITY": 13.4}, {"REPORT_ID": "181034", "DURATION_IN_SEC": 38.0, "POINT_1_LNG": 10.182659856483497, "POINT_1_LAT": 56.15898299999999, "POINT_2_LNG": 10.182616305557303, "POINT_2_LAT": 56.15498346925998, "VELOCITY": 11.8}, {"REPORT_ID": "181088", "DURATION_IN_SEC": 43.0, "POINT_1_LNG": 10.182616305557303, "POINT_1_LAT": 56.15498346925998, "POINT_2_LNG": 10.183499758266407, "POINT_2_LAT": 56.149807565419565, "VELOCITY": 13.5}, {"REPORT_ID": "181142", "DURATION_IN_SEC": 37.0, "POINT_1_LNG": 10.183499758266407, "POINT_1_LAT": 56.149807565419565, "POINT_2_LNG": 10.186762304229774, "POINT_2_LAT": 56.14563850929, "VELOCITY": 13.7}, {"REPORT_ID": "189994", "DURATION_IN_SEC": 56.0, "POINT_1_LNG": 10.186762304229774, "POINT_1_LAT": 56.14563850929, "POINT_2_LNG": 10.186756880950952, "POINT_2_LAT": 56.14258759218248, "VELOCITY": 8.0}, {"REPORT_ID": "184729", "DURATION_IN_SEC": 55.0, "POINT_1_LNG": 10.186756880950952, "POINT_1_LAT": 56.14258759218248, "POINT_2_LNG": 10.179150601188667, "POINT_2_LAT": 56.13844851575673, "VELOCITY": 12.0}, {"REPORT_ID": "184675", "DURATION_IN_SEC": 89.0, "POINT_1_LNG": 10.179150601188667, "POINT_1_LAT": 56.13844851575673, "POINT_2_LNG": 10.166163050262412, "POINT_2_LAT": 56.131053962866226, "VELOCITY": 12.9}, {"REPORT_ID": "WALKING", "DURATION_IN_SEC": 64.8, "POINT_1_LNG": 10.166163050262412, "POINT_1_LAT": 56.131053962866226, "POINT_2_LNG": 10.164431, "POINT_2_LAT": 56.130402, "VELOCITY": 2.0}], "total_duration": 749.8, "total_distance": 7405.7, "average_velocity": 9.9}
        ];

    let map = L.map('map').setView([56.16184, 10.21284], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        opacity: 0.5
    }).addTo(map);

    function displayRoute(rank) {
        // Clear existing layers
        map.eachLayer(function (layer) {
            if (layer instanceof L.Polyline) {
                map.removeLayer(layer);
            }
        });
        const route = searched_result.find(r => r.route_rank === rank);
        if (route) {
            document.getElementById('route-details').innerHTML = `
                <p>Speed: ${route.average_velocity} km/h 🚀</p>
                <p>Distance: ${route.total_distance} m 📏</p>
                <p>Duration: ${route.total_duration} sec ⏰</p>
            `;
            route.path.forEach(segment => {
                const line = L.polyline([
                    [segment.POINT_1_LAT, segment.POINT_1_LNG],
                    [segment.POINT_2_LAT, segment.POINT_2_LNG]
                ], {
                    color: 'red',
                    weight: 18,
                    opacity: 2 / segment.VELOCITY
                }).addTo(map);

                let segmentDiv = document.createElement('div');
                segmentDiv.className = 'route-segment';
                segmentDiv.innerHTML = `Route ID: ${segment.REPORT_ID} 📍`;
                segmentDiv.onmouseover = () => map.fitBounds(line.getBounds());

                let tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                tooltip.innerHTML = `
                    <p>Speed: ${segment.VELOCITY} km/h</p>
                    <p>ID: ${segment.REPORT_ID}</p>
                    <p>Duration: ${segment.DURATION_IN_SEC} sec</p>
                `;
                segmentDiv.appendChild(tooltip);

                document.getElementById('route-details').appendChild(segmentDiv);
            });

            const startMarker = L.marker([route.path[0].POINT_1_LAT, route.path[0].POINT_1_LNG]).addTo(map)
                .bindPopup('Start', {closeOnClick: false, autoClose: false}).openPopup();
            const endMarker = L.marker([route.path[route.path.length - 1].POINT_2_LAT, route.path[route.path.length - 1].POINT_2_LNG]).addTo(map)
                .bindPopup('End', {closeOnClick: false, autoClose: false}).openPopup();
        }
    }

    displayRoute(1); // Default to display rank 1 route
</script>

</body>
</html>

"""
closet_address="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Closest Parking Addresses</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            width: 80%;
            background: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            padding: 20px;
        }

        .parking-card {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
        }

        .parking-card:hover {
            background-color: #f0f8ff;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .info, .occupancy {
            display: flex;
            flex-direction: column;
        }

        .info h4, .occupancy h4 {
            margin: 5px 0;
        }

        .info small {
            color: #777;
        }

        .emoji {
            font-size: 2rem;
            margin-right: 10px;
        }

        .popup {
            visibility: hidden;
            background-color: #fff;
            border: 1px solid #ccc;
            padding: 10px;
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-radius: 6px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            z-index: 10;
            width: fit-content;
            transition: visibility 0.3s ease;
        }

        .parking-card:hover .popup {
            visibility: visible;
        }
        
        .grid-line {
            background: repeating-linear-gradient(90deg, #ebebeb, #ebebeb 1px, transparent 1px, transparent 20px);
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            right: 0;
            pointer-events: none;
        }

        .heading {
            text-align: center;
            margin-bottom: 20px;
            position: relative;
        }

    </style>
</head>
<body>

<div class="container">
    <div class="heading">
        <h2>🚗 Closest Parking Near Tilst Bibliotek</h2>
        <div class="grid-line"></div>
    </div>
    <div id="parking-list">
        <!-- Parking cards will be dynamically inserted here -->
    </div>
</div>

<script>
    const searched_result = [
        {"date": "2014-05-22", "longitude": 10.197, "latitude": 56.1527, "garagecode": "SCANDCENTER", "occupancy rate": 0.4462609970674487},
        {"date": "2014-05-23", "longitude": 10.197, "latitude": 56.1527, "garagecode": "SCANDCENTER", "occupancy rate": 0.7021505376344086},
        {"date": "2014-05-25", "longitude": 10.197, "latitude": 56.1527, "garagecode": "SCANDCENTER", "occupancy rate": 0.2785714285714285},
        {"date": "2014-05-26", "longitude": 10.197, "latitude": 56.1527, "garagecode": "SCANDCENTER", "occupancy rate": 0.3617775537634408},
        {"date": "2014-05-27", "longitude": 10.197, "latitude": 56.1527, "garagecode": "SCANDCENTER", "occupancy rate": 0.3447076612903225}
        ];

    const parkingList = document.getElementById('parking-list');

    searched_result.forEach(parking => {
        const card = document.createElement('div');
        card.className = 'parking-card';
        
        card.innerHTML = `
            <div class="info">
                <h4>${parking.garagecode}</h4>
                <small>${parking.date}</small>
            </div>
            <div class="occupancy">
                <h4>🔄 Occupancy Rate: ${Math.round(parking.occupancy_rate * 100)}%</h4>
            </div>
            <div class="popup">
                <strong>Coordinates:</strong><br>
                Longitude: ${parking.longitude} <br>
                Latitude: ${parking.latitude}
            </div>
        `;
        
        parkingList.appendChild(card);
    });
</script>

</body>
</html>
"""