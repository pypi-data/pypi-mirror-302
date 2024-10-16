# SpeedX

`SpeedX` is a terminal-based network speed testing utility that allows you to measure download speed, upload speed, and latency (ping). It provides a convenient way to test your network's performance directly from the command line, with results displayed both graphically and in ASCII format.

## Features

- **Network Speed Testing:** Measure download speed, upload speed, and latency (ping).
- **Graphical Display:** View test results using `matplotlib` for a graphical representation.
- **Terminal ASCII Plot:** Visualize the results in the terminal using `termplotlib` for ASCII plots.
- **History Tracking:** Save and view the history of previous speed tests.
- **JSON Reports:** Automatically save test results to a JSON file for future reference.

## Installation

Install `SpeedX` via `pip`:

```bash
pip install speedx
```


## Usage

`SpeedX` can be used directly from the terminal using the** **`speedx` command. Here are the available subcommands:

### Run a Speed Test

`speedx test`

This command runs a new network speed test and displays the results, including download speed, upload speed, latency, and server information.

### View Test History

`speedx history`

Displays the history of previous speed tests and visualizes the results using ASCII plots in the terminal.

### Example Output


# Running a speed test
$ speedx test

Download Speed: 99.83 Mbps
Upload Speed: 19.31 Mbps
Latency (Ping): 50.09 ms
IP Address: 192.168.31.124
Server: Sonepat, India (speedtest.sonepat.softechinfosol.com:8080)
