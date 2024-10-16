# clipunch - a CLI tool to create punchard visualizations.

clipunch consumes data from stdin. It has to be comma-separated pairs of dates
with frequencies. For example, piping the following data to clipunch creates a
punchard visualization for the complete year 2022 printed to the terminal.

```
cat << EOF | clipunch
2022-10-25,3
2022-11-07,3
2022-11-08,1
2022-11-09,3
2022-11-28,1
2022-12-04,7
2022-12-05,1
2022-12-06,1
2022-12-07,5
2022-12-08,2
2022-12-14,21
EOF
```

In case data spans more than a year, multiple punchcard visualizations -one per
year- are created in chronological order.

Note, the tools assumes that provided dates are unique. If multiple data values
for a single date are given, only the last one is visualized.


## Installation

```
pip install clipunch
```

## Usage

```
clipunch [--html]
```

Options:
  --html    Create punchcard as HTML file, which is open in browser.


## Examples:

To plot the commit activity to the
[Spring Framework](https://spring.io/projects/spring-framework), clone the
repository, create commit frequencies per day, and pip it to `clipunch`.

```
git clone https://github.com/spring-projects/spring-framework.git
git -C ./spring-framework/ log --date=short --pretty=format:%ad | \
    sort | uniq -c | awk '{print $2","$1}' | \
    clipunch --html
```

The output on the terminal will look similar to the following.

<img src="doc/spring-framework.png" width="40%"/>


```
git -C ./spring-framework/ log --author "Juergen Hoeller" --date=short --pretty=format:%ad | \
    sort | uniq -c | awk '{print $2","$1}' | \
    clipunch --html
```

[![](doc/spring-framework-html.png)](./doc/spring-framework.html)
