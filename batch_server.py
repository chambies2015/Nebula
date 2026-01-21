import subprocess
import asyncio
import os
import sys
import signal

processes = {}


async def start_batch_server(server_name, batch_script_path):
    print(f"[{server_name}] Attempting to start server...")
    print(f"[{server_name}] Batch script path: {batch_script_path}")
    
    if server_name in processes and processes[server_name] is not None:
        if processes[server_name].poll() is None:
            print(f"[{server_name}] ERROR: Server is already running (PID: {processes[server_name].pid})")
            return False, "Server is already running"
    
    try:
        if os.name == 'nt':
            print(f"[{server_name}] Checking for existing Java/Minecraft processes...")
            try:
                import psutil
                java_processes = []
                for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        if p.info['name'] and 'java.exe' in p.info['name'].lower():
                            cmdline = p.info['cmdline']
                            if cmdline and any('minecraft' in str(arg).lower() or 'server' in str(arg).lower() or 'forge' in str(arg).lower() for arg in cmdline):
                                java_processes.append(p)
                                print(f"[{server_name}] WARNING: Found existing Java/Minecraft process (PID: {p.pid})")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if java_processes:
                    print(f"[{server_name}] ERROR: Found {len(java_processes)} existing Java/Minecraft process(es). Please stop the server first or wait for processes to fully terminate.")
                    return False, f"Found {len(java_processes)} existing Java/Minecraft process(es). Server may still be shutting down."
            except ImportError:
                print(f"[{server_name}] psutil not available, skipping Java process check")
        
        if not os.path.exists(batch_script_path):
            print(f"[{server_name}] ERROR: Batch script not found at: {batch_script_path}")
            return False, f"Batch script not found: {batch_script_path}"
        
        print(f"[{server_name}] Starting batch script...")
        if os.name == 'nt':
            proc = subprocess.Popen(
                ['cmd.exe', '/k', batch_script_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            print(f"[{server_name}] Process started with PID: {proc.pid}")
        else:
            proc = subprocess.Popen(
                [batch_script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"[{server_name}] Process started with PID: {proc.pid}")
        
        processes[server_name] = proc
        await asyncio.sleep(1)
        
        if proc.poll() is None:
            print(f"[{server_name}] SUCCESS: Server process is running (PID: {proc.pid})")
        else:
            print(f"[{server_name}] WARNING: Process exited immediately with code: {proc.poll()}")
        
        return True, "Server started successfully"
    except Exception as e:
        print(f"[{server_name}] ERROR: Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, f"Failed to start server: {str(e)}"


async def stop_batch_server(server_name):
    print(f"[{server_name}] Attempting to stop server...")
    
    if server_name not in processes or processes[server_name] is None:
        print(f"[{server_name}] ERROR: Server process not found in tracked processes")
        return False, "Server process not found"
    
    proc = processes[server_name]
    print(f"[{server_name}] Found process with PID: {proc.pid}")
    
    if proc.poll() is not None:
        print(f"[{server_name}] Process already exited with code: {proc.poll()}")
        processes[server_name] = None
        return False, "Server is not running"
    
    try:
        if os.name == 'nt':
            try:
                import psutil
                print(f"[{server_name}] Searching for Java/Minecraft server process...")
                
                java_processes = []
                for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        if p.info['name'] and 'java.exe' in p.info['name'].lower():
                            cmdline = p.info['cmdline']
                            if cmdline and any('minecraft' in str(arg).lower() or 'server' in str(arg).lower() or 'forge' in str(arg).lower() for arg in cmdline):
                                java_processes.append(p)
                                print(f"[{server_name}] Found Java process: PID {p.pid}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if java_processes:
                    for java_proc in java_processes:
                        print(f"[{server_name}] Stopping Java process (PID: {java_proc.pid})...")
                        try:
                            java_proc.send_signal(psutil.signal.SIGTERM)
                            print(f"[{server_name}] Sent SIGTERM to Java process (PID: {java_proc.pid}), waiting 6 seconds...")
                            await asyncio.sleep(6)
                            
                            if java_proc.is_running():
                                print(f"[{server_name}] Java process (PID: {java_proc.pid}) still running, sending SIGINT...")
                                java_proc.send_signal(psutil.signal.SIGINT)
                                await asyncio.sleep(2)
                                
                                if java_proc.is_running():
                                    print(f"[{server_name}] Java process (PID: {java_proc.pid}) still running, force killing...")
                                    java_proc.kill()
                                    await asyncio.sleep(1)
                                    
                                    if java_proc.is_running():
                                        print(f"[{server_name}] WARNING: Java process (PID: {java_proc.pid}) still running after kill attempt")
                                    else:
                                        print(f"[{server_name}] Java process (PID: {java_proc.pid}) killed successfully")
                                else:
                                    print(f"[{server_name}] Java process (PID: {java_proc.pid}) stopped after SIGINT")
                            else:
                                print(f"[{server_name}] Java process (PID: {java_proc.pid}) stopped after SIGTERM")
                            
                            await asyncio.sleep(2)
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            print(f"[{server_name}] Error stopping Java process (PID: {java_proc.pid}): {e}")
                else:
                    print(f"[{server_name}] No Java/Minecraft server process found")
            except ImportError:
                print(f"[{server_name}] psutil not available, skipping Java process detection")
            
            print(f"[{server_name}] Stopping cmd.exe process (PID: {proc.pid})...")
            try:
                proc.send_signal(signal.CTRL_C_EVENT)
                print(f"[{server_name}] Sent CTRL+C to cmd process, waiting 1 second...")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[{server_name}] Could not send CTRL+C: {e}")
            
            print(f"[{server_name}] Terminating cmd process...")
            proc.terminate()
            
            max_wait = 5
            waited = 0
            while proc.poll() is None and waited < max_wait:
                await asyncio.sleep(0.5)
                waited += 0.5
                print(f"[{server_name}] Waiting for process to terminate... ({waited:.1f}s)")
            
            if proc.poll() is None:
                print(f"[{server_name}] Process still running after {max_wait}s, force killing...")
                proc.kill()
                await asyncio.sleep(1)
                if proc.poll() is None:
                    print(f"[{server_name}] WARNING: Process still running after kill attempt")
                else:
                    print(f"[{server_name}] Process killed successfully (exit code: {proc.poll()})")
            else:
                print(f"[{server_name}] Process terminated successfully (exit code: {proc.poll()})")
            
            await asyncio.sleep(2)
            print(f"[{server_name}] Waiting additional 2 seconds for file locks to release...")
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
        print(f"[{server_name}] SUCCESS: Server stopped successfully")
        return True, "Server stopped successfully"
    except Exception as e:
        print(f"[{server_name}] ERROR: Exception occurred while stopping: {str(e)}")
        import traceback
        traceback.print_exc()
        processes[server_name] = None
        return False, f"Failed to stop server: {str(e)}"


def is_server_running(server_name):
    if server_name not in processes or processes[server_name] is None:
        return False
    proc = processes[server_name]
    is_running = proc.poll() is None
    if is_running:
        print(f"[{server_name}] Status check: Server is running (PID: {proc.pid})")
    else:
        print(f"[{server_name}] Status check: Server is not running (exit code: {proc.poll()})")
    return is_running
