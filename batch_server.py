import subprocess
import asyncio
import os
import sys
import signal

processes = {}


async def start_batch_server(server_name, batch_script_path):
    if server_name in processes and processes[server_name] is not None:
        if processes[server_name].poll() is None:
            return False, "Server is already running"
    
    try:
        if not os.path.exists(batch_script_path):
            return False, f"Batch script not found: {batch_script_path}"
        
        if os.name == 'nt':
            proc = subprocess.Popen(
                batch_script_path,
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            proc = subprocess.Popen(
                [batch_script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        processes[server_name] = proc
        await asyncio.sleep(1)
        return True, "Server started successfully"
    except Exception as e:
        return False, f"Failed to start server: {str(e)}"


async def stop_batch_server(server_name):
    if server_name not in processes or processes[server_name] is None:
        return False, "Server process not found"
    
    proc = processes[server_name]
    
    if proc.poll() is not None:
        processes[server_name] = None
        return False, "Server is not running"
    
    try:
        if os.name == 'nt':
            try:
                import psutil
                
                java_processes = []
                for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        if p.info['name'] and 'java.exe' in p.info['name'].lower():
                            cmdline = p.info['cmdline']
                            if cmdline and any('minecraft' in str(arg).lower() or 'server' in str(arg).lower() or 'forge' in str(arg).lower() for arg in cmdline):
                                java_processes.append(p)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if java_processes:
                    java_proc = java_processes[0]
                    try:
                        java_proc.send_signal(psutil.signal.SIGTERM)
                        await asyncio.sleep(6)
                        
                        if java_proc.is_running():
                            java_proc.send_signal(psutil.signal.SIGINT)
                            await asyncio.sleep(0.5)
                            
                            if java_proc.is_running():
                                java_proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except ImportError:
                pass
            
            proc.terminate()
            await asyncio.sleep(1)
            if proc.poll() is None:
                proc.kill()
        else:
            if proc.stdin:
                proc.stdin.write(b"stop\r\n")
                proc.stdin.flush()
            
            await asyncio.sleep(6)
            
            if proc.stdin:
                proc.stdin.write(b"\x03")
                proc.stdin.flush()
            
            await asyncio.sleep(0.5)
            
            if proc.stdin:
                proc.stdin.write(b"y\r\n")
                proc.stdin.flush()
            
            await asyncio.sleep(2)
            
            if proc.poll() is None:
                proc.terminate()
                await asyncio.sleep(1)
                if proc.poll() is None:
                    proc.kill()
            
            if proc.stdin:
                proc.stdin.close()
        
        processes[server_name] = None
        return True, "Server stopped successfully"
    except Exception as e:
        processes[server_name] = None
        return False, f"Failed to stop server: {str(e)}"


def is_server_running(server_name):
    if server_name not in processes or processes[server_name] is None:
        return False
    proc = processes[server_name]
    return proc.poll() is None
