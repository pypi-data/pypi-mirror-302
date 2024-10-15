import platform
import psutil
import socket

def get_os_info():
    """Получить информацию об операционной системе."""
    os_name = platform.system()
    os_version = platform.version()
    return f"Операционная система: {os_name}, версия: {os_version}"

def get_cpu_info():
    """Получить информацию о процессоре."""
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else "Неизвестно"
    return f"Количество ядер: {cpu_count}, Текущая частота: {cpu_freq} MHz"

def get_memory_info():
    """Получить информацию о памяти (RAM)."""
    memory = psutil.virtual_memory()
    total_memory = memory.total // (1024 ** 3)
    available_memory = memory.available // (1024 ** 3)
    return f"Всего памяти: {total_memory} GB, Доступно: {available_memory} GB"

def get_disk_info():
    """Получить информацию о дисках."""
    disk = psutil.disk_usage('/')
    total_disk = disk.total // (1024 ** 3)
    used_disk = disk.used // (1024 ** 3)
    return f"Всего места на диске: {total_disk} GB, Использовано: {used_disk} GB"

def get_network_info():
    """Получить информацию о сети (IP-адрес и имя хоста)."""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return f"Имя хоста: {hostname}, IP-адрес: {ip_address}"
