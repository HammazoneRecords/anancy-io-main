"""System Health Checks - Low-level monitoring functions

Provides detailed system monitoring using psutil and system commands.
"""

import psutil
import os
import time
import socket
from typing import Dict, Any
from datetime import datetime

class SystemChecks:
    """Collection of system health check functions.

    Each check returns a dictionary with:
    - status: 'healthy', 'warning', 'critical', or 'error'
    - value: The measured value
    - message: Human-readable description
    """

    def check_cpu(self) -> Dict[str, Any]:
        """Check CPU usage and load.

        Returns:
            Dict with CPU health information
        """
        try:
            # Get CPU usage percentage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Get CPU load averages
            load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)
            cpu_count = psutil.cpu_count() or 1

            # Calculate load percentage
            load_percent = (load_avg[0] / cpu_count) * 100 if load_avg[0] > 0 else 0

            # Determine status
            if cpu_percent > 90 or load_percent > 200:
                status = 'critical'
                message = f"High CPU usage: {cpu_percent:.1f}%, Load: {load_percent:.1f}%"
            elif cpu_percent > 75 or load_percent > 150:
                status = 'warning'
                message = f"Elevated CPU usage: {cpu_percent:.1f}%, Load: {load_percent:.1f}%"
            else:
                status = 'healthy'
                message = f"CPU usage normal: {cpu_percent:.1f}%, Load: {load_percent:.1f}%"

            return {
                'status': status,
                'usage': cpu_percent,
                'load': load_percent,
                'message': message
            }

        except Exception as e:
            return {
                'status': 'error',
                'usage': None,
                'load': None,
                'message': f"CPU check failed: {e}"
            }

    def check_memory(self) -> Dict[str, Any]:
        """Check memory utilization.

        Returns:
            Dict with memory health information
        """
        try:
            mem = psutil.virtual_memory()
            mem_percent = mem.percent

            # Calculate available memory in GB
            available_gb = mem.available / (1024**3)

            # Determine status
            if mem_percent > 95 or available_gb < 0.5:
                status = 'critical'
                message = f"Critical memory usage: {mem_percent:.1f}%, {available_gb:.1f}GB available"
            elif mem_percent > 85 or available_gb < 1.0:
                status = 'warning'
                message = f"High memory usage: {mem_percent:.1f}%, {available_gb:.1f}GB available"
            else:
                status = 'healthy'
                message = f"Memory usage normal: {mem_percent:.1f}%, {available_gb:.1f}GB available"

            return {
                'status': status,
                'usage': mem_percent,
                'available_gb': available_gb,
                'message': message
            }

        except Exception as e:
            return {
                'status': 'error',
                'usage': None,
                'available_gb': None,
                'message': f"Memory check failed: {e}"
            }

    def check_disk(self) -> Dict[str, Any]:
        """Check disk space utilization.

        Returns:
            Dict with disk health information
        """
        try:
            # Check root filesystem
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent

            # Calculate free space in GB
            free_gb = disk.free / (1024**3)

            # Determine status
            if disk_percent > 98 or free_gb < 0.1:
                status = 'critical'
                message = f"Critical disk usage: {disk_percent:.1f}%, {free_gb:.1f}GB free"
            elif disk_percent > 95 or free_gb < 0.5:
                status = 'warning'
                message = f"High disk usage: {disk_percent:.1f}%, {free_gb:.1f}GB free"
            else:
                status = 'healthy'
                message = f"Disk usage normal: {disk_percent:.1f}%, {free_gb:.1f}GB free"

            return {
                'status': status,
                'usage': disk_percent,
                'free_gb': free_gb,
                'message': message
            }

        except Exception as e:
            return {
                'status': 'error',
                'usage': None,
                'free_gb': None,
                'message': f"Disk check failed: {e}"
            }

    def check_load(self) -> Dict[str, Any]:
        """Check system load average.

        Returns:
            Dict with load health information
        """
        try:
            if hasattr(psutil, 'getloadavg'):
                load_avg = psutil.getloadavg()
                cpu_count = psutil.cpu_count() or 1

                # Use 1-minute load average
                load_1min = load_avg[0]
                load_normalized = load_1min / cpu_count

                # Determine status
                if load_normalized > 3.0:
                    status = 'critical'
                    message = f"Critical load: {load_1min:.2f} ({load_normalized:.2f}x CPU count)"
                elif load_normalized > 2.0:
                    status = 'warning'
                    message = f"High load: {load_1min:.2f} ({load_normalized:.2f}x CPU count)"
                else:
                    status = 'healthy'
                    message = f"Load normal: {load_1min:.2f} ({load_normalized:.2f}x CPU count)"

                return {
                    'status': status,
                    'load': load_1min,
                    'normalized': load_normalized,
                    'message': message
                }
            else:
                # Windows or other system without getloadavg
                return {
                    'status': 'healthy',
                    'load': 0.0,
                    'normalized': 0.0,
                    'message': "Load average not available on this platform"
                }

        except Exception as e:
            return {
                'status': 'error',
                'load': None,
                'normalized': None,
                'message': f"Load check failed: {e}"
            }

    def check_network(self) -> Dict[str, Any]:
        """Check network connectivity and latency.

        Returns:
            Dict with network health information
        """
        try:
            # Test DNS resolution
            start_time = time.time()
            try:
                socket.gethostbyname('google.com')
                dns_time = (time.time() - start_time) * 1000  # Convert to ms
            except socket.gaierror:
                return {
                    'status': 'critical',
                    'latency': None,
                    'message': "DNS resolution failed - no internet connectivity"
                }

            # Test HTTP connectivity (simple)
            try:
                import urllib.request
                start_time = time.time()
                req = urllib.request.Request('http://www.google.com', method='HEAD')
                urllib.request.urlopen(req, timeout=5)
                http_time = (time.time() - start_time) * 1000
                total_latency = dns_time + http_time
            except Exception:
                # DNS works but HTTP might not
                total_latency = dns_time
                if dns_time > 5000:
                    return {
                        'status': 'critical',
                        'latency': total_latency,
                        'message': f"Network connectivity issues - high latency ({total_latency:.0f}ms)"
                    }
                else:
                    return {
                        'status': 'warning',
                        'latency': total_latency,
                        'message': f"Limited connectivity - DNS OK but HTTP issues ({total_latency:.0f}ms)"
                    }

            # Determine status based on latency
            if total_latency > 5000:
                status = 'critical'
                message = f"Poor network performance: {total_latency:.0f}ms latency"
            elif total_latency > 2000:
                status = 'warning'
                message = f"Slow network: {total_latency:.0f}ms latency"
            else:
                status = 'healthy'
                message = f"Network healthy: {total_latency:.0f}ms latency"

            return {
                'status': status,
                'latency': total_latency,
                'message': message
            }

        except Exception as e:
            return {
                'status': 'error',
                'latency': None,
                'message': f"Network check failed: {e}"
            }

    def check_processes(self) -> Dict[str, Any]:
        """Check process health and zombie processes.

        Returns:
            Dict with process health information
        """
        try:
            # Get all processes
            all_processes = psutil.pids()
            zombie_count = 0
            error_processes = 0

            # Check for zombie processes
            for pid in all_processes[:100]:  # Check first 100 processes for performance
                try:
                    proc = psutil.Process(pid)
                    if proc.status() == psutil.STATUS_ZOMBIE:
                        zombie_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    error_processes += 1
                    continue

            # Determine status
            if zombie_count > 10:
                status = 'critical'
                message = f"Critical: {zombie_count} zombie processes detected"
            elif zombie_count > 5:
                status = 'warning'
                message = f"Warning: {zombie_count} zombie processes detected"
            else:
                status = 'healthy'
                message = f"Process health normal: {len(all_processes)} total processes"

            return {
                'status': status,
                'zombie_count': zombie_count,
                'total_processes': len(all_processes),
                'message': message
            }

        except Exception as e:
            return {
                'status': 'error',
                'zombie_count': None,
                'total_processes': None,
                'message': f"Process check failed: {e}"
            }

    def get_system_summary(self) -> Dict[str, Any]:
        """Get a quick system summary.

        Returns:
            Dict with basic system information
        """
        try:
            return {
                'cpu_count': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(),
                'memory_total': psutil.virtual_memory().total,
                'memory_used': psutil.virtual_memory().used,
                'memory_percent': psutil.virtual_memory().percent,
                'disk_total': psutil.disk_usage('/').total,
                'disk_used': psutil.disk_usage('/').used,
                'disk_percent': psutil.disk_usage('/').percent,
                'boot_time': psutil.boot_time(),
                'process_count': len(psutil.pids()),
                'platform': os.uname().sysname if hasattr(os, 'uname') else 'Unknown',
            }
        except Exception as e:
            return {'error': f"Failed to get system summary: {e}"}
