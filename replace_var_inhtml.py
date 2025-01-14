import json
import re

# 示例 HTML 代码
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event and Weather Information</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f0f8ff;
        }
        .container {
            width: 80%;
            max-width: 1000px;
            margin: 20px;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            overflow: hidden;
        }
        .highlight {
            background-color: #e0f7fa;
            border-radius: 8px;
            padding: 10px;
            transition: transform 0.2s;
        }
        .highlight:hover {
            transform: scale(1.05);
        }
        .event {
            margin-bottom: 15px;
            padding: 15px;
            border-top: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .event:hover {
            background-color: #f9f9f9;
        }
        .map-container {
            width: 100%;
            height: 400px;
            margin-top: 20px;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
        }
        .leaflet-container {
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
        }
        .tooltip-bubble {
            position: absolute;
            background-color: white;
            border: 1px solid #ccc;
            padding: 5px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            pointer-events: none;
            white-space: nowrap;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>📅 Events with Good Weather and Low Pollution</h1>
    <div id="events">
        <!-- Dynamic Content based on JavaScript will be loaded here -->
    </div>
    <div class="map-container" id="map"></div>
</div>

<script>
    // Sample data
    var searched_result = [{'city': 'Aarhus', 'title': 'Mandagsfilm i børnebiblioteket', 'price': '0', 'library': 'Hovedbiblioteket', 'longitude': 10.200179, 'latitude': 56.156617, 'date': '2014-08-04'}];
    var pollution_data = [{'date': '2014-08-01', 'average_particullate_matter': 66.81935854356952, 'pollution_condition': 'Good'}];
    var weather_data = [{'date': '2014-08-01', 'weather': '☀️', 'average_temperature': 21.4, 'average_wind_speed': 10.1}];

    // Find events with good weather and low pollution
    function filterEvents(searched_result, pollution_data, weather_data) {
        const goodDays = pollution_data.filter(p => p.pollution_condition === 'Good')
            .map(p => p.date);
        const weatherGoodDays = weather_data.filter(w => w.weather === '☀️')
            .map(w => w.date);
        return searched_result.filter(event =>
            goodDays.includes(event.date) && weatherGoodDays.includes(event.date)
        );
    }

    const filteredEvents = filterEvents(searched_result, pollution_data, weather_data);
    const eventContainer = document.getElementById('events');

    filteredEvents.forEach(event => {
        const eventEl = document.createElement('div');
        eventEl.className = 'highlight event';
        eventEl.innerHTML = `<strong>${event.title}</strong> - ${event.date} 🌤️
            <br>Location: ${event.library}, ${event.city}`
        eventContainer.appendChild(eventEl);
    });

    // Initialize Leaflet map
    const map = L.map('map').setView([56.156617, 10.200179], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        opacity: 0.5
    }).addTo(map);

    // Add markers
    filteredEvents.forEach(event => {
        const marker = L.marker([event.latitude, event.longitude]).addTo(map);
        marker.bindTooltip(`<div class="tooltip-bubble">${event.title}<br>${event.date}</div>`, {
            direction: 'top',
            permanent: false,
            sticky: true
        });
    });
</script>

</body>
</html>
"""


def update_js_arrays(html_content, replacements):
    """
    批量更新 HTML/JavaScript 中数组的内容，并保持 JSON 格式的元素为合法的 JSON。

    参数:
    - html_content: str，HTML 内容。
    - replacements: str，JSON 格式的变量名和新值列表，例如：'[{"variable": "final_result", "value": ["a", "b", "c"]}]'

    返回:
    - 更新后的 HTML 内容。
    """
    # 将 JSON 格式字符串解析为 Python 列表
    try:
        replacement_list = json.loads(replacements)
    except json.JSONDecodeError:
        raise ValueError("输入的 replacements 必须是有效的 JSON 格式")

    # 遍历替换列表，逐一替换数组内容
    for item in replacement_list:
        variable_name = item.get("variable")
        new_value = item.get("value")
        if not variable_name or not isinstance(new_value, list):
            continue  # 跳过不完整的项目或非列表的值

        # 构造新的数组内容
        def format_element(element):
            if isinstance(element, (dict, list)):
                return json.dumps(element, ensure_ascii=False)  # 保持 JSON 格式
            else:
                return f'"{element}"'  # 字符串元素加引号

        new_array_content = ",\n".join([f'        {format_element(v)}' for v in new_value])
        replacement = f"const {variable_name} = [\n{new_array_content}\n        ];"

        # 正则表达式匹配原始数组
        pattern = rf'(?:const|var|let)\s+{variable_name}\s*=\s*\[.*?\];'
        html_content = re.sub(pattern, lambda m: replacement, html_content, flags=re.DOTALL)

    return html_content
#
# #
# replacements_json = json.dumps([{'variable': 'searched_result', 'value': [{'city': 'Aarhus', 'title': 'Mandagsfilm i bÃ¸rnebiblioteket', 'price': '0', 'library': 'Hovedbiblioteket', 'longitude': 10.200179, 'latitude': 56.156617, 'date': '2014-08-04'}, {'city': 'Aarhus', 'title': 'International Playgroup', 'price': '0', 'library': 'Hovedbiblioteket', 'longitude': 10.200179, 'latitude': 56.156617, 'date': '2014-08-01'}, {'city': 'Aarhus', 'title': 'International Playgroup', 'price': '0', 'library': 'Hovedbiblioteket', 'longitude': 10.200179, 'latitude': 56.156617, 'date': '2014-08-15'}, {'city': 'Viby J', 'title': 'Bustur til Store Bogdag ved Hald Hovedgaard lÃ¸rdag 9. august', 'price': '110', 'library': 'Viby Bibliotek', 'longitude': 10.164431, 'latitude': 56.130402, 'date': '2014-08-09'}, {'city': 'Aarhus V', 'title': 'Forfatterspirer - SAXOs forfatterklub', 'price': '0', 'library': 'Hasle Bibliotek', 'longitude': 10.167345, 'latitude': 56.179458, 'date': '2014-08-04'}, {'city': 'Aarhus', 'title': 'ByggelÃ¸rdag', 'price': '0', 'library': 'Hovedbiblioteket', 'longitude': 10.200179, 'latitude': 56.156617, 'date': '2014-08-09'}, {'city': 'Viby J', 'title': 'Artmoney â\x80?penge med dobbeltvÃ¦rdi ', 'price': '0', 'library': 'Viby Bibliotek', 'longitude': 10.164431, 'latitude': 56.130402, 'date': '2014-08-01'}]}, {'variable': 'pollution_data', 'value': [{'date': '2014-08-01', 'average_particullate_matter': 66.81935854356952, 'pollution_condition': 'Good'}, {'date': '2014-08-02', 'average_particullate_matter': 80.37908314773571, 'pollution_condition': 'Good'}, {'date': '2014-08-03', 'average_particullate_matter': 91.33991431576344, 'pollution_condition': 'Good'}, {'date': '2014-08-04', 'average_particullate_matter': 99.42586148230636, 'pollution_condition': 'Good'}, {'date': '2014-08-05', 'average_particullate_matter': 105.38195991091314, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-06', 'average_particullate_matter': 108.35381093788666, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-07', 'average_particullate_matter': 110.84666542934916, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-08', 'average_particullate_matter': 112.6560257362039, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-09', 'average_particullate_matter': 66.81935854356952, 'pollution_condition': 'Good'}, {'date': '2014-08-10', 'average_particullate_matter': 114.32433958178667, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-11', 'average_particullate_matter': 114.97595737441227, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-12', 'average_particullate_matter': 115.01903148973028, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-13', 'average_particullate_matter': 113.60746102449887, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-14', 'average_particullate_matter': 112.14771250927988, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-15', 'average_particullate_matter': 66.81935854356952, 'pollution_condition': 'Good'}, {'date': '2014-08-16', 'average_particullate_matter': 110.57477264291016, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-17', 'average_particullate_matter': 113.3337973273942, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-18', 'average_particullate_matter': 115.7442078074734, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-19', 'average_particullate_matter': 115.92222686216284, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-20', 'average_particullate_matter': 117.02104986389509, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-21', 'average_particullate_matter': 113.32641982182628, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-22', 'average_particullate_matter': 66.81935854356952, 'pollution_condition': 'Good'}, {'date': '2014-08-23', 'average_particullate_matter': 114.55720273447167, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-24', 'average_particullate_matter': 115.23164903489234, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-25', 'average_particullate_matter': 114.21977852016828, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-26', 'average_particullate_matter': 116.10501732244497, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-27', 'average_particullate_matter': 117.7142492576095, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-28', 'average_particullate_matter': 114.5087617545162, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-29', 'average_particullate_matter': 114.9814789037367, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-30', 'average_particullate_matter': 114.79759032417718, 'pollution_condition': 'Unhealthy'}, {'date': '2014-08-31', 'average_particullate_matter': 118.4754469809453, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-01', 'average_particullate_matter': 119.6681901138332, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-02', 'average_particullate_matter': 120.34119803266518, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-03', 'average_particullate_matter': 117.8618844345459, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-04', 'average_particullate_matter': 115.7634403612967, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-05', 'average_particullate_matter': 114.69497803761446, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-06', 'average_particullate_matter': 115.93497123236824, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-07', 'average_particullate_matter': 115.90604893590697, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-08', 'average_particullate_matter': 114.18689680772086, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-09', 'average_particullate_matter': 111.43518776292996, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-10', 'average_particullate_matter': 112.76928668646374, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-11', 'average_particullate_matter': 112.58236667903984, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-12', 'average_particullate_matter': 111.58464024993812, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-13', 'average_particullate_matter': 66.81935854356952, 'pollution_condition': 'Good'}, {'date': '2014-09-14', 'average_particullate_matter': 110.20188381588716, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-15', 'average_particullate_matter': 111.26392755506062, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-16', 'average_particullate_matter': 109.3392647240782, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-17', 'average_particullate_matter': 110.61387960900768, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-18', 'average_particullate_matter': 114.75792656520665, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-19', 'average_particullate_matter': 116.25957374412272, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-20', 'average_particullate_matter': 115.90875556792874, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-21', 'average_particullate_matter': 117.11045378619154, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-22', 'average_particullate_matter': 116.88960807968326, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-23', 'average_particullate_matter': 115.45029076961148, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-24', 'average_particullate_matter': 115.60388827023014, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-25', 'average_particullate_matter': 113.8519472284088, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-26', 'average_particullate_matter': 111.65567774065823, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-27', 'average_particullate_matter': 112.37465973768867, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-28', 'average_particullate_matter': 113.68006836179164, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-29', 'average_particullate_matter': 114.92324764909677, 'pollution_condition': 'Unhealthy'}, {'date': '2014-09-30', 'average_particullate_matter': 113.1759899343418, 'pollution_condition': 'Unhealthy'}, {'date': '2014-10-01', 'average_particullate_matter': 111.90848214285714, 'pollution_condition': 'Unhealthy'}]}, {'variable': 'weather_data', 'value': [{'date': '2014-08-01', 'weather': '☀️', 'average_temperature': 21.4, 'average_wind_speed': 10.1}, {'date': '2014-08-02', 'weather': '☀️', 'average_temperature': 22.7, 'average_wind_speed': 16.8}, {'date': '2014-08-03', 'weather': '🌧️', 'average_temperature': 21.8, 'average_wind_speed': 9.4}, {'date': '2014-08-04', 'weather': '🌤️', 'average_temperature': 19.4, 'average_wind_speed': 10.7}, {'date': '2014-08-05', 'weather': '🌧️', 'average_temperature': 17.8, 'average_wind_speed': 5.1}, {'date': '2014-08-06', 'weather': '🌤️', 'average_temperature': 18.5, 'average_wind_speed': 8.3}, {'date': '2014-08-07', 'weather': '🌤️', 'average_temperature': 18.9, 'average_wind_speed': 6.6}, {'date': '2014-08-08', 'weather': '🌤️', 'average_temperature': 19.5, 'average_wind_speed': 7.7}, {'date': '2014-08-09', 'weather': '🌤️', 'average_temperature': 18.7, 'average_wind_speed': 15.4}, {'date': '2014-08-10', 'weather': '🌤️', 'average_temperature': 19.3, 'average_wind_speed': 14.8}, {'date': '2014-08-11', 'weather': '🌤️', 'average_temperature': 18.6, 'average_wind_speed': 16.4}, {'date': '2014-08-12', 'weather': '❄️', 'average_temperature': 16.5, 'average_wind_speed': 13.0}, {'date': '2014-08-13', 'weather': '🌧️', 'average_temperature': 15.5, 'average_wind_speed': 9.7}, {'date': '2014-08-14', 'weather': '🌤️', 'average_temperature': 16.8, 'average_wind_speed': 12.0}, {'date': '2014-08-15', 'weather': '🌤️', 'average_temperature': 16.5, 'average_wind_speed': 13.6}, {'date': '2014-08-16', 'weather': '❄️', 'average_temperature': 14.8, 'average_wind_speed': 20.7}, {'date': '2014-08-17', 'weather': '🌧️', 'average_temperature': 14.5, 'average_wind_speed': 11.8}, {'date': '2014-08-18', 'weather': '❄️', 'average_temperature': 14.1, 'average_wind_speed': 15.3}, {'date': '2014-08-19', 'weather': '❄️', 'average_temperature': 13.9, 'average_wind_speed': 22.5}, {'date': '2014-08-20', 'weather': '❄️', 'average_temperature': 14.5, 'average_wind_speed': 23.1}, {'date': '2014-08-21', 'weather': '❄️', 'average_temperature': 13.6, 'average_wind_speed': 16.3}, {'date': '2014-08-22', 'weather': '❄️', 'average_temperature': 13.8, 'average_wind_speed': 11.9}, {'date': '2014-08-23', 'weather': '❄️', 'average_temperature': 13.4, 'average_wind_speed': 13.3}, {'date': '2014-08-24', 'weather': '❄️', 'average_temperature': 12.6, 'average_wind_speed': 18.8}, {'date': '2014-08-25', 'weather': '❄️', 'average_temperature': 13.5, 'average_wind_speed': 18.2}, {'date': '2014-08-26', 'weather': '❄️', 'average_temperature': 14.2, 'average_wind_speed': 10.8}, {'date': '2014-08-27', 'weather': '❄️', 'average_temperature': 14.7, 'average_wind_speed': 10.4}, {'date': '2014-08-28', 'weather': '❄️', 'average_temperature': 14.6, 'average_wind_speed': 8.6}, {'date': '2014-08-29', 'weather': '🌧️', 'average_temperature': 14.8, 'average_wind_speed': 8.5}, {'date': '2014-08-30', 'weather': '🌧️', 'average_temperature': 15.1, 'average_wind_speed': 9.4}, {'date': '2014-08-31', 'weather': '🌧️', 'average_temperature': 15.4, 'average_wind_speed': 15.1}, {'date': '2014-09-01', 'weather': '🌤️', 'average_temperature': 16.2, 'average_wind_speed': 13.9}, {'date': '2014-09-02', 'weather': '❄️', 'average_temperature': 15.5, 'average_wind_speed': 5.6}, {'date': '2014-09-03', 'weather': '❄️', 'average_temperature': 14.7, 'average_wind_speed': 5.8}, {'date': '2014-09-04', 'weather': '❄️', 'average_temperature': 14.3, 'average_wind_speed': 7.3}, {'date': '2014-09-05', 'weather': '🌧️', 'average_temperature': 14.3, 'average_wind_speed': 8.3}, {'date': '2014-09-06', 'weather': '🌤️', 'average_temperature': 18.6, 'average_wind_speed': 12.5}, {'date': '2014-09-07', 'weather': '🌧️', 'average_temperature': 17.4, 'average_wind_speed': 7.7}, {'date': '2014-09-08', 'weather': '🌧️', 'average_temperature': 13.5, 'average_wind_speed': 11.5}, {'date': '2014-09-09', 'weather': '🌧️', 'average_temperature': 15.2, 'average_wind_speed': 21.6}, {'date': '2014-09-10', 'weather': '🌧️', 'average_temperature': 14.7, 'average_wind_speed': 13.1}, {'date': '2014-09-11', 'weather': '🌧️', 'average_temperature': 15.8, 'average_wind_speed': 10.2}, {'date': '2014-09-12', 'weather': '🌧️', 'average_temperature': 14.5, 'average_wind_speed': 6.8}, {'date': '2014-09-13', 'weather': '🌧️', 'average_temperature': 15.7, 'average_wind_speed': 10.6}, {'date': '2014-09-14', 'weather': '🌧️', 'average_temperature': 16.7, 'average_wind_speed': 19.6}, {'date': '2014-09-15', 'weather': '🌧️', 'average_temperature': 16.8, 'average_wind_speed': 20.3}, {'date': '2014-09-16', 'weather': '🌤️', 'average_temperature': 16.2, 'average_wind_speed': 17.6}, {'date': '2014-09-17', 'weather': '🌧️', 'average_temperature': 15.2, 'average_wind_speed': 13.9}, {'date': '2014-09-18', 'weather': '🌧️', 'average_temperature': 16.6, 'average_wind_speed': 14.8}, {'date': '2014-09-19', 'weather': '🌧️', 'average_temperature': 14.9, 'average_wind_speed': 10.9}, {'date': '2014-09-20', 'weather': '🌧️', 'average_temperature': 13.2, 'average_wind_speed': 3.5}, {'date': '2014-09-21', 'weather': '❄️', 'average_temperature': 14.3, 'average_wind_speed': 15.4}, {'date': '2014-09-22', 'weather': '❄️', 'average_temperature': 10.6, 'average_wind_speed': 19.5}, {'date': '2014-09-23', 'weather': '❄️', 'average_temperature': 10.0, 'average_wind_speed': 6.5}, {'date': '2014-09-24', 'weather': '🌧️', 'average_temperature': 12.8, 'average_wind_speed': 9.5}, {'date': '2014-09-25', 'weather': '❄️', 'average_temperature': 12.4, 'average_wind_speed': 18.2}, {'date': '2014-09-26', 'weather': '🌧️', 'average_temperature': 14.8, 'average_wind_speed': 16.1}, {'date': '2014-09-27', 'weather': '❄️', 'average_temperature': 13.2, 'average_wind_speed': 18.3}, {'date': '2014-09-28', 'weather': '❄️', 'average_temperature': 14.2, 'average_wind_speed': 11.8}, {'date': '2014-09-29', 'weather': '🌧️', 'average_temperature': 15.3, 'average_wind_speed': 7.5}, {'date': '2014-09-30', 'weather': '❄️', 'average_temperature': 14.1, 'average_wind_speed': 10.0}]}]
#  )
# #
# # # 调用函数
# updated_html = update_js_arrays(html_content, replacements_json)
# #
# # # 输出结果
# # print("更新后的HTML:")
# print(updated_html)