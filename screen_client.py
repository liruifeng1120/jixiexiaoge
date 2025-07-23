#!/usr/bin/env python3
import webbrowser
import json
import os
import socket
import time

CONFIG_FILE = "client_config.json"

# 这里可以直接指定一个固定IP，优先级最高
FIXED_IP = "192.168.66.24"
# 例如：FIXED_IP = "192.168.1.101"

def get_ip_from_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            ip = config.get("pc_ip")
            if ip:
                return ip
    except Exception:
        pass
    return None

def ip_range_to_list(ip_range_str):
    # 解析形如 "192.168.66.1~200" 的IP范围，返回IP列表
    try:
        base, end = ip_range_str.split('~')
        base_parts = base.split('.')
        if len(base_parts) != 4:
            return [ip_range_str]
        start_num = int(base_parts[3])
        end_num = int(end)
        ip_list = []
        for i in range(start_num, end_num + 1):
            ip_list.append(f"{base_parts[0]}.{base_parts[1]}.{base_parts[2]}.{i}")
        return ip_list
    except Exception:
        return [ip_range_str]

def is_port_open(ip, port=5000, timeout=1):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def get_comma3_ip():
    # 优先使用固定IP
    if FIXED_IP:
        return FIXED_IP

    # 其次尝试从配置文件读取IP
    config_ip = get_ip_from_config()
    if config_ip:
        # 判断是否是范围
        if '~' in config_ip:
            ip_list = ip_range_to_list(config_ip)
            for ip in ip_list:
                print(f"尝试连接 {ip} ...")
                if is_port_open(ip):
                    print(f"连接成功: {ip}")
                    return ip
            print("范围内所有IP连接失败，使用默认IP")
            return "192.168.1.100"
        else:
            return config_ip

    # 默认硬编码IP
    return "192.168.1.100"  # 示例IP

def main():
    comma3_ip = get_comma3_ip()
    url = f"http://{comma3_ip}:5000"
    print(f"正在打开浏览器访问: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    main()

"""
使用说明:
- 你可以在手机存储中创建一个名为 client_config.json 的文件，内容格式如下：
  {
    "pc_ip": "192.168.1.101"
  }
- 现在支持IP范围格式，例如：
  {
    "pc_ip": "192.168.66.1~200"
  }
  程序会自动尝试范围内的IP，直到连接成功。
- 脚本启动时会读取该文件中的IP地址或IP范围作为PC的IP。
- 如果没有配置文件，则使用代码中默认的硬编码IP。
- 你也可以直接在代码中修改 FIXED_IP 变量，指定一个固定IP，优先级最高。
- 这样打包成APP后，可以通过修改配置文件或代码灵活指定PC IP。
"""
