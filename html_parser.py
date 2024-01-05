# get the html file
# html = open('humidity.html', 'r').read()


# add data to html file
def return_html_file(data, file_name):
    html = open(file_name, 'r').read()

    html_data = '<table id="sensorTable">'
    # if data list is empty
    if not data:
        html_data += '<tr><td> No data available </td><td> No data available </td></tr><tbody>'
    else:
        html_data += ('<thead><tr><th onclick="sortTable(0)">#</th><th onclick="sortTable(1)">Value</th><th '
                      'onclick="sortTable(2)">Timestamps</th></tr></thead> <tbody>')

    # if data list is not empty
    for i in range(len(data)):
        x = data[i]
        html_data += (
                "<tr><td>" + str(i) + "</td><td>" + (x["value"]) + "</td><td>" + str(x["timestamp"]) + "</td></tr>")

    html_data += "  </tbody></table>"

    html = html.replace('data', html_data)
    return html
