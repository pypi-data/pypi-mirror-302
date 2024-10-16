import matplotlib.pyplot as plt
import termplotlib as tpl

def plot_speed_graph(reports):
    download_speeds = [report['download_speed'] for report in reports]
    upload_speeds = [report['upload_speed'] for report in reports]
    labels = [f"Test {i + 1}" for i in range(len(reports))]

    x = range(len(reports))

    # Plotting using Matplotlib for regular graphical display
    plt.figure(figsize=(10, 5))
    plt.plot(x, download_speeds, marker='o', label='Download Speed (Mbps)', color='green')
    plt.plot(x, upload_speeds, marker='o', label='Upload Speed (Mbps)', color='blue')

    plt.title('Network Speed Test Results')
    plt.xlabel('Test Number')
    plt.ylabel('Speed (Mbps)')
    plt.xticks(x, labels)
    plt.legend()
    plt.grid()
    plt.savefig('speed_test_results.png')  # Save the graph as an image
    plt.show()  # Display the graph
