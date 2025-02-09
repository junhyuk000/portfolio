import os

# 비정상적인 IP 차단 함수
def block_ip_linux(ip_address):
    print(f"Blocking IP: {ip_address}")
    os.system(f"sudo iptables -A INPUT -s {ip_address} -j DROP")

def unblock_ip_linux(ip_address):
    print(f"Unblocking IP on Linux: {ip_address}")
    os.system(f"sudo iptables -D INPUT -s {ip_address} -j DROP")

def block_ip_windows(ip_address):
    print(f"Blocking IP on Windows: {ip_address}")
    os.system(f'netsh advfirewall firewall add rule name="Block {ip_address}" dir=in action=block remoteip={ip_address}')
    
# 차단 ip 다시 풀기
def unblock_ip_windows(ip_address):
    rule_name = f"Block {ip_address}"
    print(f"Unblocking IP on Windows: {ip_address}")
    os.system(f'netsh advfirewall firewall delete rule name="{rule_name}"')
    
    
suspicious_ip = "10.0.66.83"
# 차단 해제할 IP
# unblock_ip_windows(suspicious_ip)

# 의심스러운 IP 예시

block_ip_windows(suspicious_ip)
