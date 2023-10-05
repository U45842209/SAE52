from flask import Flask, jsonify, request, Response
import psutil
import subprocess
import json
from datetime import datetime

app = Flask(__name__)


@app.route('/metrics', methods=['GET'])
def prometheus_metrics_general():
    # Collect SSH log metrics
    ssh_log_metrics = count_active_ssh_users()

    # Collect other system metrics as before
    # CPU
    cpu_percent = psutil.cpu_percent()  # CPU usage percentage
    cpu_count = psutil.cpu_count()  # Number of CPU cores/threads
    cpu_freq = psutil.cpu_freq()  # CPU frequency information
    cpu_stats = psutil.cpu_stats()  # CPU statistics

    # Memory
    memory_info = psutil.virtual_memory()  # Memory usage information
    swap_info = psutil.swap_memory()  # Swap space information

    # Disk
    disk_info = psutil.disk_usage('/')  # Disk usage information
    disk_partitions = psutil.disk_partitions()  # Disk partitions information
    disk_io = psutil.disk_io_counters()  # Disk I/O counters

    # Network
    network_io = psutil.net_io_counters()  # Network I/O counters
    network_if_stats = psutil.net_if_stats()  # Network interface statistics


    # Create a Prometheus-compatible response with SSH log metrics
    prometheus_metrics = (
        f'# HELP cpu_percent CPU utilization\n'
        f'# TYPE cpu_percent gauge\n'
        f'cpu_percent {cpu_percent}\n'
        f'# HELP cpu_count Number of CPU cores/threads\n'
        f'# TYPE cpu_count gauge\n'
        f'cpu_count {cpu_count}\n'
        f'# HELP cpu_frequency CPU frequency\n'
        f'# TYPE cpu_frequency gauge\n'
        f'cpu_frequency_max {cpu_freq.max}\n'
        f'cpu_frequency_min {cpu_freq.min}\n'
        f'cpu_frequency_current {cpu_freq.current}\n'
        f'# HELP cpu_stats CPU statistics\n'
        f'# TYPE cpu_stats gauge\n'
        f'cpu_ctx_switches {cpu_stats.ctx_switches}\n'
        f'cpu_interrupts {cpu_stats.interrupts}\n'
        f'cpu_soft_interrupts {cpu_stats.soft_interrupts}\n'
        f'cpu_syscalls {cpu_stats.syscalls}\n'
        f'# HELP total_memory Total memory\n'
        f'# TYPE total_memory gauge\n'
        f'total_memory {memory_info.total}\n'
        f'# HELP available_memory Available memory\n'
        f'# TYPE available_memory gauge\n'
        f'available_memory {memory_info.available}\n'
        f'# HELP total_swap_space Total swap space\n'
        f'# TYPE total_swap_space gauge\n'
        f'total_swap_space {swap_info.total}\n'
        f'# HELP free_swap_space Free swap space\n'
        f'# TYPE free_swap_space gauge\n'
        f'free_swap_space {swap_info.free}\n'
        f'# HELP total_disk_space Total disk space\n'
        f'# TYPE total_disk_space gauge\n'
        f'total_disk_space {disk_info.total}\n'
        f'# HELP free_disk_space Free disk space\n'
        f'# TYPE free_disk_space gauge\n'
        f'free_disk_space {disk_info.free}\n'
        f'# HELP disk_io_read_count Disk I/O read count\n'
        f'# TYPE disk_io_read_count counter\n'
        f'disk_io_read_count {disk_io.read_count}\n'
        f'# HELP disk_io_write_count Disk I/O write count\n'
        f'# TYPE disk_io_write_count counter\n'
        f'disk_io_write_count {disk_io.write_count}\n'
        f'# HELP network_io_bytes_sent Network I/O bytes sent\n'
        f'# TYPE network_io_bytes_sent counter\n'
        f'network_io_bytes_sent {network_io.bytes_sent}\n'
        f'# HELP network_io_bytes_recv Network I/O bytes received\n'
        f'# TYPE network_io_bytes_recv counter\n'
        f'network_io_bytes_recv {network_io.bytes_recv}\n'
        f'# HELP ssh_active_count SSH active session count\n'
        f'# TYPE ssh_active_count counter\n'
        f'ssh_active_count {ssh_log_metrics}\n'
    )
    return Response(prometheus_metrics, content_type='text/plain')


@app.route('/metrics_auth', methods=['GET'])
def prometheus_metrics_auth():

    # Get log entries on Alpine machine
    ssh_auth_log = auth_info()

    return ssh_auth_log


def count_active_ssh_users():
    try:
        ps_output = subprocess.check_output(['ps', 'aux'])
        ps_lines = ps_output.decode('utf-8').split('\n')
        ssh_processes = [line for line in ps_lines if 'sshd: ' in line and 'pts/' in line]

        # Extract usernames from SSH process lines
        usernames = set(line.split()[0] for line in ssh_processes)

        # Count the unique usernames
        active_user_count = len(usernames)

        return active_user_count

    except subprocess.CalledProcessError:
        return -1  # Error occurred


def auth_info():
    try:
        cat_output = subprocess.check_output(['cat', '/var/log/messages'])
        cat_lines = cat_output.decode('utf-8').split('\n')
        auth_processes = []
        for line in cat_lines:
            if ('auth.info' in line) or ('auth.err' in line):
                auth_processes.append(f"{line}")
        # Reverse the list of log entries
        auth_processes.reverse()
        # Convert the list of log entries to a JSON array
        return json.dumps({"logs": auth_processes})
    except subprocess.CalledProcessError:
        return json.dumps({"error": "An error occurred"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
