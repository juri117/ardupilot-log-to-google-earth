import datetime

from LogAnalyzer.DataflashLog import DataflashLog


GPS_TYPE_FC_POS = "POS"
GPS_TYPE_FC_AHR2 = "AHR2"
GPS_TYPE_RAW_1 = "GPS"
GPS_TYPE_RAW_2 = "GPS2"

USED_GPS_TYPE = GPS_TYPE_FC_POS

STYLE_COLORS = ["7f00ffff",
                "7f00ff00",
                "7fff0000",
                "7f0000ff"]


def generate_kml(file_names):
    if len(file_names) == 0:
        return
    if len(file_names) > 1:
        out_f = open("out.kml", 'w')
    else:
        out_f = open(file_names[0].replace(".bin", "") + ".kml", 'w')
    _write_kml(out_f, file_names)
    out_f.close()


def _write_kml(out_f, file_names):
    out_f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
    out_f.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    out_f.write("\t<Document>\n")
    out_f.write("\t\t<name>ardupilot logs</name>\n")
    out_f.write("\t\t<description></description>\n")
    for i in range(0, min(len(file_names), len(STYLE_COLORS))):
        out_f.write(
            "\t\t<Style id=\"flightPathStyle{:d}\">\n".format(i))
        out_f.write("\t\t\t<LineStyle>\n")
        out_f.write("\t\t\t\t<color>{}</color>\n".format(STYLE_COLORS[i]))
        out_f.write("\t\t\t\t<width>2</width>\n")
        out_f.write("\t\t\t</LineStyle>\n")
        # out_f.write("\t\t\t<PolyStyle>\n")
        # out_f.write("\t\t\t\t<color>7f00ff00</color>\n")
        # out_f.write("\t\t\t</PolyStyle>\n")
        out_f.write("\t\t</Style>\n")

    count = 0
    for file_name in file_names:
        out_f.write("\t\t<Placemark>\n")
        out_f.write(
            "\t\t\t<name>{}({})</name>\n".format(file_name, USED_GPS_TYPE))
        out_f.write(
            "\t\t\t<description>{}</description>\n".format(USED_GPS_TYPE))
        out_f.write("\t\t\t<styleUrl>#flightPathStyle{:d}</styleUrl>\n".format(
            count % len(STYLE_COLORS)))
        out_f.write("\t\t\t<LineString>\n")
        out_f.write("\t\t\t\t<extrude>0</extrude>\n")
        out_f.write("\t\t\t\t<tessellate>1</tessellate>\n")
        out_f.write("\t\t\t\t<altitudeMode>absolute</altitudeMode>\n")
        out_f.write("\t\t\t\t<coordinates>\n")
        logdata = DataflashLog(file_name,
                               format='bin', ignoreBadlines=True)
        for i in range(0, len(logdata.channels[USED_GPS_TYPE]['TimeUS'].dictData)):
            out_f.write("\t\t\t\t\t{:0.7f},{:0.7f},{:0.3f}\n".format(
                logdata.channels[USED_GPS_TYPE]['Lng'].listData[i][1]*1e-7,
                logdata.channels[USED_GPS_TYPE]['Lat'].listData[i][1]*1e-7,
                logdata.channels[USED_GPS_TYPE]['Alt'].listData[i][1]))

        out_f.write("\t\t\t\t</coordinates>\n")
        out_f.write("\t\t\t</LineString>\n")
        out_f.write("\t\t</Placemark>\n")
        count += 1

    out_f.write("\t</Document>\n")
    out_f.write("</kml>\n")


if __name__ == '__main__':
    file_names = ["00000002.BIN"]
    generate_kml(file_names)
    print("done")
