import argparse
import csv
import sys
import tempfile
import textwrap
import webbrowser
from dateutil import rrule, parser
from datetime import date, datetime
from itertools import groupby
from jinja2 import Template


MAX_FREQ = 0


def parse_frequencies():
    lookup_table = []
    for date_str, freq_str in csv.reader(sys.stdin):
        date = parser.parse(date_str)
        lookup_table.append((date.date(), int(freq_str)))

    return lookup_table


def create_empty_frequencies(start_date, end_date):
    return {d.date(): 0 for d in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date)}


def weekday_to_str(weekday_no):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[weekday_no][:3]


def get_start_and_end_date_from_calendar_week(year, calendar_week):
    monday = datetime.fromisocalendar(year, calendar_week, 1).date()
    sunday = datetime.fromisocalendar(year, calendar_week, 7).date()
    return monday, sunday


def pad_years(date_freq_pairs):
    first_day_of_year = date_freq_pairs[0][0]
    last_day_of_year = date_freq_pairs[-1][0]
    first_day_of_year_iso_cal = first_day_of_year.isocalendar()
    last_day_of_year_iso_cal = last_day_of_year.isocalendar()

    fst_pad_date, _ = get_start_and_end_date_from_calendar_week(first_day_of_year_iso_cal.year, first_day_of_year_iso_cal.week)
    _, end_pad_date = get_start_and_end_date_from_calendar_week(last_day_of_year_iso_cal.year, last_day_of_year_iso_cal.week)

    start_pad = [(d.date(), None) for d in rrule.rrule(rrule.DAILY, dtstart=fst_pad_date, until=first_day_of_year)][:-1]
    end_pad = [(d.date(), None) for d in rrule.rrule(rrule.DAILY, dtstart=last_day_of_year, until=end_pad_date)][1:]

    return start_pad + date_freq_pairs + end_pad


def find_max_freq(data):
    return max(data, key=lambda x: x[1])[1]


def map_to_color_space(no):
    return get_color(int((255 / MAX_FREQ) * no))


def get_color(idx):
    """ Colormap generated with this code:
    ```
    from matplotlib import cm
    colors = [(int(cm.Blues(i)[0]*255), int(cm.Blues(i)[1]*255), int(cm.Blues(i)[2]*255)) for i in range(256)]
    ```
    """
    colors = [(247, 251, 255), (246, 250, 254), (245, 249, 254), (244, 249, 254), (243, 248, 253), (243, 248, 253),
              (242, 247, 253), (241, 247, 253), (240, 246, 252), (239, 246, 252), (239, 245, 252), (238, 245, 252),
              (237, 244, 251), (236, 244, 251), (236, 243, 251), (235, 243, 251), (234, 242, 250), (233, 242, 250),
              (232, 241, 250), (232, 241, 250), (231, 240, 249), (230, 240, 249), (229, 239, 249), (228, 239, 249),
              (228, 238, 248), (227, 238, 248), (226, 237, 248), (225, 237, 248), (225, 236, 247), (224, 236, 247),
              (223, 235, 247), (222, 235, 247), (221, 234, 246), (221, 234, 246), (220, 233, 246), (219, 233, 246),
              (218, 232, 245), (218, 232, 245), (217, 231, 245), (216, 231, 245), (215, 230, 244), (215, 230, 244),
              (214, 229, 244), (213, 229, 244), (212, 228, 243), (212, 228, 243), (211, 227, 243), (210, 227, 243),
              (209, 226, 242), (209, 226, 242), (208, 225, 242), (207, 225, 242), (206, 224, 241), (206, 224, 241),
              (205, 223, 241), (204, 223, 241), (203, 222, 240), (203, 222, 240), (202, 221, 240), (201, 221, 240),
              (200, 220, 239), (200, 220, 239), (199, 219, 239), (198, 219, 239), (197, 218, 238), (196, 218, 238),
              (195, 217, 238), (193, 217, 237), (192, 216, 237), (191, 216, 236), (190, 215, 236), (188, 215, 235),
              (187, 214, 235), (186, 214, 234), (185, 213, 234), (183, 212, 234), (182, 212, 233), (181, 211, 233),
              (180, 211, 232), (178, 210, 232), (177, 210, 231), (176, 209, 231), (175, 209, 230), (173, 208, 230),
              (172, 208, 230), (171, 207, 229), (170, 207, 229), (168, 206, 228), (167, 206, 228), (166, 205, 227),
              (165, 205, 227), (163, 204, 227), (162, 203, 226), (161, 203, 226), (160, 202, 225), (158, 202, 225),
              (157, 201, 224), (155, 200, 224), (154, 199, 224), (152, 199, 223), (151, 198, 223), (149, 197, 223),
              (147, 196, 222), (146, 195, 222), (144, 194, 222), (143, 193, 221), (141, 192, 221), (139, 192, 221),
              (138, 191, 220), (136, 190, 220), (135, 189, 220), (133, 188, 219), (131, 187, 219), (130, 186, 219),
              (128, 185, 218), (127, 184, 218), (125, 184, 217), (123, 183, 217), (122, 182, 217), (120, 181, 216),
              (119, 180, 216), (117, 179, 216), (115, 178, 215), (114, 177, 215), (112, 177, 215), (111, 176, 214),
              (109, 175, 214), (107, 174, 214), (106, 173, 213), (105, 172, 213), (103, 171, 212), (102, 170, 212),
              (101, 170, 211), (99, 169, 211), (98, 168, 210), (97, 167, 210), (96, 166, 209), (94, 165, 209),
              (93, 164, 208), (92, 163, 208), (90, 163, 207), (89, 162, 207), (88, 161, 206), (87, 160, 206),
              (85, 159, 205), (84, 158, 205), (83, 157, 204), (81, 156, 204), (80, 155, 203), (79, 155, 203),
              (78, 154, 202), (76, 153, 202), (75, 152, 201), (74, 151, 201), (72, 150, 200), (71, 149, 200),
              (70, 148, 199), (69, 148, 199), (67, 147, 198), (66, 146, 198), (65, 145, 197), (64, 144, 197),
              (63, 143, 196), (62, 142, 196), (61, 141, 195), (60, 140, 195), (59, 139, 194), (58, 138, 193),
              (57, 137, 193), (56, 136, 192), (55, 135, 192), (53, 133, 191), (52, 132, 191), (51, 131, 190),
              (50, 130, 190), (49, 129, 189), (48, 128, 189), (47, 127, 188), (46, 126, 188), (45, 125, 187),
              (44, 124, 187), (43, 123, 186), (42, 122, 185), (41, 121, 185), (40, 120, 184), (39, 119, 184),
              (38, 118, 183), (37, 117, 183), (36, 116, 182), (35, 115, 182), (34, 114, 181), (33, 113, 181),
              (32, 112, 180), (31, 111, 179), (30, 110, 178), (30, 109, 178), (29, 108, 177), (28, 107, 176),
              (27, 106, 175), (26, 105, 174), (26, 104, 174), (25, 103, 173), (24, 102, 172), (23, 101, 171),
              (23, 100, 171), (22, 99, 170), (21, 98, 169), (20, 97, 168), (19, 96, 167), (19, 95, 167), (18, 94, 166),
              (17, 93, 165), (16, 92, 164), (15, 91, 163), (15, 90, 163), (14, 89, 162), (13, 88, 161), (12, 87, 160),
              (12, 86, 160), (11, 85, 159), (10, 84, 158), (9, 83, 157), (8, 82, 156), (8, 81, 156), (8, 80, 154),
              (8, 79, 153), (8, 78, 151), (8, 76, 150), (8, 75, 148), (8, 74, 146), (8, 73, 145), (8, 72, 143),
              (8, 71, 142), (8, 70, 140), (8, 69, 139), (8, 68, 137), (8, 67, 136), (8, 66, 134), (8, 65, 133),
              (8, 64, 131), (8, 63, 130), (8, 62, 128), (8, 61, 126), (8, 60, 125), (8, 59, 123), (8, 58, 122),
              (8, 57, 120), (8, 56, 119), (8, 55, 117), (8, 54, 116), (8, 53, 114), (8, 52, 113), (8, 51, 111),
              (8, 50, 110), (8, 49, 108), (8, 48, 107)]

    return colors[idx % len(colors)]


def generate_output(data, kind="terminal"):
    """

    The input has to be a nested dictionary of the following form:
    {2024: {"Mon": [(date, freq), (date, freq), ...], "Tue": [], ... }, 2023: {"Mon": [], "Tue": [], ... }, ...}
    """
    if kind == "terminal":
        generate_terminal_output(data)
    if kind == "html":
        generate_html_output(data)


def generate_terminal_output(data):
    try:
        from sty import fg, rs
    except Exception:
        raise Exception("Cannot generate terminal output without the sty package: https://sty.mewo.dev/index.html")

    for year, weekday_freqs in data.items():
        print(year)
        for weekday, freqs in weekday_freqs.items():
            print(weekday, end=" ")
            for _, f in freqs:
                if f is None:
                    print("□", end="")
                else:
                    color = map_to_color_space(f)
                    print(fg(*color) + "■" + rs.fg, end="")
            print()
        print()

    print("Legend: min (0 " + fg(*map_to_color_space(0)) + "■" + rs.fg  + f"), max({MAX_FREQ} "+ fg(*map_to_color_space(MAX_FREQ)) + "■" + rs.fg + ")")


def generate_html_output(data):
    html_template_str = """<!DOCTYPE html>
        <html lang="en">
        <head>
        <title>CLIPunch</title>
        <link rel="stylesheet" href="https://unpkg.com/mvp.css">
        <style>
        :root {
            --color-accent: #adaeae14;
        }
        </style>
        </head>
        <body>

        {% for year, weekday_freqs in data.items() -%}
        <h2>{{year}}</h2>
        <table>

          {% for weekday, freqs in weekday_freqs.items() -%}
          <tr>
            <td>{{weekday}}</td>
            {% for d, f in freqs: -%}
              {% if f is none -%}
            <td><span title="{{d.strftime('%Y %b %d')}}">□</span></td>
              {% else %}
            <td><span title="{{d.strftime('%Y %b %d')}}: {{f}}" style="color:rgb{{map_to_color_space(f)}}">■</span></td>
              {%- endif %}
            {%- endfor %}
          </tr>
          {%- endfor %}
        </table>
        {%- endfor %}
        <h2>Legend</h2>
        <ul>
          <li>
            min: 0 <span title="0" style="color:rgb{{map_to_color_space(0)}}">■</span>
          </li>
          <li>
            max: {{max_freq}} <span title="{{max_freq}}" style="color:rgb{{map_to_color_space(max_freq)}}">■</span>
          </li>
          <li>
            in previous/next year:□</span>
          </li>
        </ul>
        </body>
        </html>
    """

    template = Template(textwrap.dedent(html_template_str))
    html_str = template.render(data=data, max_freq=MAX_FREQ, map_to_color_space=map_to_color_space)
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(bytes(html_str, "utf-8"))
        webbrowser.open(f"file://{fp.name}", new=2)


def main():
    global MAX_FREQ

    argsparser = argparse.ArgumentParser(description="clipunch - a CLI tool to create punchard visualizations.")
    # argsparser.add_argument("--help", action="store_true")
    argsparser.add_argument("--html", action="store_true", help="Create punchcard as HTML file, which is open in browser.")
    args = argsparser.parse_args()
    if args.html:
        output="html"
    else:
        output="terminal"

    freqs = parse_frequencies()
    MAX_FREQ = find_max_freq(freqs)

    # assumes they were inserted chronologically
    # this makes always full year periods for visualization
    start_date = date(freqs[0][0].year, 1, 1)
    end_date = date(freqs[-1][0].year, 12, 31)

    freq_dict = create_empty_frequencies(start_date, end_date)

    # Fill values from input data in 0 initialized dict
    for d, f in freqs:
        freq_dict[d] = f

    calendar_year_freqs = {}
    for year, group in groupby(freq_dict.items(), lambda x: x[0].year):
        freqs_per_year = [(d, f) for d, f in group]
        calendar_year_freqs[year] = freqs_per_year

    # Pad beginning and end of year for visualization
    # There needs to be a bit of padding in the first week of a year and the last week of a year
    for year, freqs_per_year in calendar_year_freqs.items():
        calendar_year_freqs[year] = pad_years(freqs_per_year)

    # Group per week days and generate a data structure for visualization
    # freqs_per_year_per_weekday = {2024: {"Mon": [(date, freq), (date, freq), ...], "Tue": [], ... }, 2023: {"Mon": [], "Tue": [], ... }, ...}
    freqs_per_year_per_weekday = {y: {} for y, _ in calendar_year_freqs.items()}
    for year, freqs_per_year in calendar_year_freqs.items():
        inner_dict = {weekday_to_str(i): [] for i in range(7)}
        for weekday, group in groupby(freqs_per_year, lambda x: x[0].weekday()):
            freqs_per_weekday = [(d, f) for d, f in group]
            inner_dict[weekday_to_str(weekday)] += freqs_per_weekday
        freqs_per_year_per_weekday[year] = inner_dict

    generate_output(freqs_per_year_per_weekday, kind=output)


if __name__ == "__main__":
    main()
