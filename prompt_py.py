
def get_html_generate_prompt(query,searched_result,other_results):
    html_generate_prompt=f"""
    
The user wants to search for {query}.
The system retrieves a list of JSON data formatted as:
searched_result = [{searched_result}]
Additionally, there is a separate list of unrelated results to be displayed in a dark-themed style:
{other_results}

Create an HTML page to display all this data. The page should include smooth animations, hover effects, and interactive clickable elements.

Use tooltips or pop-up bubbles to display detailed information, such as map data, in an intuitive and concise way.
Design the UI with rounded corners, soft shadows, visible grid lines, and rich emoji usage. Adopt a calendar-style layout to represent each day.

Ensure that the searched_result data is visually highlighted, while other data is shown in a dark theme.
Utilize Leaflet for any map-based features.

Preserve the provided variable names exactly as they are, and dynamically generate UI components based on the data.

Provide an HTML page code that strictly adheres to the given variable names. The page content should dynamically adjust based on the variable values, meaning replacing the variable values will automatically update the HTML page.
    """
    return html_generate_prompt
def get_data_prompt(data_info):
    data_prompt=f"""
    我有下面几个数据库，他们每个键的数据类型和范围如下所示：
    {data_info}
    如果你想查询数据，你可以通过调用函数get_data(查询数据名称，数据库名称)
    数据名称可以是日期，或者具体的数据名称，输入格式可以是列表
    return的是查询到的对应的数据列表，列表的每个元素是有相同键名的字典
    比如good_weather=get_data(['☀️','🌤️'],'weather')
    return：got corresponding data：overview:{{'length': 14, 'keys': dict_keys(['date', 'weather', 'average_temperature', 'average_wind_speed'])}}
    你负责查到对应的数据，如果这个查询不能同时完成，比如后面的查询需要依赖前面的查询结果，那么需要按照依赖关系写出合理的查询程序
    只回答代码，每行函数都要有变量
    最终得出的数据变量是searched_result,是搜索到的数据列表，和get_data的返回格式一致
    """
    return data_prompt

know_data_prompt="""
    我有下面几个数据库
    events：city,title,price,library,longitude,latitude,date
    pollution：longitude,latitude,date,average_particullate_matter,pollution_condition
    weather：date,weather,average_temperature,average_wind_speed
    parking：date,longitude,latitude,garagecode,occupancy rate
    
    你的职责是根据用户需求返回一个关键和相关的数据库列表，以json格式返回
    用户：我想知道天气好和污染小的时候有什么活动
    Return: 
    {
        "key_database":["events"],
        "related_databases": ["pollution", "weather"]
    }
    """

