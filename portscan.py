import socket
import concurrent.futures
import argparse
import time
import os

os.system("clear")

banner = """
\033[1;34m
######################################
#           PortScan                 #
#             Forwell                #
######################################
\033[0m
"""
print(banner)

def scan_port(ip, port, timeout=1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return port if sock.connect_ex((ip, port)) == 0 else None
    except:
        return None

def scan_ports(ip, start_port, end_port, max_threads=200):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
    return sorted(open_ports)

def main():
    parser = argparse.ArgumentParser(description="Forwell Port Scanner")
    parser.add_argument("host", help="Hedef IP adresi veya domain")
    parser.add_argument("-s", "--start", type=int, default=1, help="Başlangıç portu")
    parser.add_argument("-e", "--end", type=int, default=1024, help="Bitiş portu")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Zaman aşımı süresi")
    parser.add_argument("-m", "--max-threads", type=int, default=200, help="Eş zamanlı thread sayısı")
    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print("Hedef çözümlenemedi.")
        return

    start_time = time.time()
    ports = scan_ports(ip, args.start, args.end, args.max_threads)
    duration = time.time() - start_time

    if ports:
        print(f"\nAçık portlar: {', '.join(map(str, ports))}")
    else:
        print("\nAçık port bulunamadı.")
    print(f"Tarama süresi: {duration:.2f} saniye")

if __name__ == "__main__":
    main()
