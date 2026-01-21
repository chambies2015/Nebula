import subprocess
import asyncio
import os
import sys
import signal
from concurrent.futures import ThreadPoolExecutor

processes = {}
executor = ThreadPoolExecutor(max_workers=2)


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
                
                def check_java_processes():
                    java_processes = []
                    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            if p.info['name'] and 'java.exe' in p.info['name'].lower():
                                cmdline = p.info['cmdline']
                                if cmdline and any('minecraft' in str(arg).lower() or 'server' in str(arg).lower() or 'forge' in str(arg).lower() for arg in cmdline):
                                    java_processes.append(p)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    return java_processes
                
                loop = asyncio.get_event_loop()
                java_processes = await loop.run_in_executor(executor, check_java_processes)
                
                if java_processes:
                    print(f"[{server_name}] WARNING: Found {len(java_processes)} existing Java/Minecraft process(es)")
                    for p in java_processes:
                        print(f"[{server_name}]   - PID: {p.pid}")
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
                
                def find_java_processes():
                    java_processes = []
                    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            if p.info['name'] and 'java.exe' in p.info['name'].lower():
                                cmdline = p.info['cmdline']
                                if cmdline and any('minecraft' in str(arg).lower() or 'server' in str(arg).lower() or 'forge' in str(arg).lower() for arg in cmdline):
                                    java_processes.append(p)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    return java_processes
                
                loop = asyncio.get_event_loop()
                java_processes = await loop.run_in_executor(executor, find_java_processes)
                
                if java_processes:
                    for java_proc in java_processes:
                        print(f"[{server_name}] Found Java process: PID {java_proc.pid}")
                    
                    async def stop_java_process(java_proc):
                        print(f"[{server_name}] Stopping Java process (PID: {java_proc.pid})...")
                        try:
                            def send_sigterm():
                                java_proc.send_signal(psutil.signal.SIGTERM)
                            
                            loop = asyncio.get_event_loop()
                            await loop.run_in_executor(executor, send_sigterm)
                            print(f"[{server_name}] Sent SIGTERM to Java process (PID: {java_proc.pid}), waiting 6 seconds...")
                            
                            for i in range(12):
                                await asyncio.sleep(0.5)
                                def check_running():
                                    return java_proc.is_running()
                                is_running = await loop.run_in_executor(executor, check_running)
                                if not is_running:
                                    print(f"[{server_name}] Java process (PID: {java_proc.pid}) stopped after SIGTERM")
                                    return
                            
                            def check_and_send_sigint():
                                if java_proc.is_running():
                                    java_proc.send_signal(psutil.signal.SIGINT)
                                    return True
                                return False
                            
                            if await loop.run_in_executor(executor, check_and_send_sigint):
                                print(f"[{server_name}] Java process (PID: {java_proc.pid}) still running, sending SIGINT...")
                                for i in range(4):
                                    await asyncio.sleep(0.5)
                                    is_running = await loop.run_in_executor(executor, lambda: java_proc.is_running())
                                    if not is_running:
                                        print(f"[{server_name}] Java process (PID: {java_proc.pid}) stopped after SIGINT")
                                        return
                                
                                def kill_process():
                                    if java_proc.is_running():
                                        java_proc.kill()
                                        return True
                                    return False
                                
                                if await loop.run_in_executor(executor, kill_process):
                                    print(f"[{server_name}] Java process (PID: {java_proc.pid}) still running, force killing...")
                                    await asyncio.sleep(1)
                                    is_running = await loop.run_in_executor(executor, lambda: java_proc.is_running())
                                    if is_running:
                                        print(f"[{server_name}] WARNING: Java process (PID: {java_proc.pid}) still running after kill attempt")
                                    else:
                                        print(f"[{server_name}] Java process (PID: {java_proc.pid}) killed successfully")
                        except psutil.NoSuchProcess:
                            print(f"[{server_name}] Java process (PID: {java_proc.pid}) already exited (likely stopped with other processes)")
                        except psutil.AccessDenied as e:
                            print(f"[{server_name}] ERROR: Access denied when stopping Java process (PID: {java_proc.pid}): {e}")
                    
                    for java_proc in java_processes:
                        await stop_java_process(java_proc)
                    
                    await asyncio.sleep(2)
                    print(f"[{server_name}] Waiting additional 2 seconds for file locks to release...")
                else:
                    print(f"[{server_name}] No Java/Minecraft server process found")
            except ImportError:
                print(f"[{server_name}] psutil not available, skipping Java process detection")
            
            print(f"[{server_name}] Stopping cmd.exe process (PID: {proc.pid})...")
            try:
                def send_ctrl_c():
                    proc.send_signal(signal.CTRL_C_EVENT)
                
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(executor, send_ctrl_c)
                print(f"[{server_name}] Sent CTRL+C to cmd process, waiting 1 second...")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[{server_name}] Could not send CTRL+C: {e}")
            
            print(f"[{server_name}] Terminating cmd process...")
            
            def terminate_process():
                proc.terminate()
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, terminate_process)
            
            max_wait = 5
            waited = 0
            while waited < max_wait:
                def check_poll():
                    return proc.poll()
                
                exit_code = await loop.run_in_executor(executor, check_poll)
                if exit_code is not None:
                    print(f"[{server_name}] Process terminated successfully (exit code: {exit_code})")
                    break
                
                await asyncio.sleep(0.5)
                waited += 0.5
                if waited % 1 == 0:
                    print(f"[{server_name}] Waiting for process to terminate... ({waited:.1f}s)")
            
            def check_and_kill():
                if proc.poll() is None:
                    proc.kill()
                    return True
                return False
            
            if await loop.run_in_executor(executor, check_and_kill):
                print(f"[{server_name}] Process still running after {max_wait}s, force killing...")
                await asyncio.sleep(1)
                exit_code = await loop.run_in_executor(executor, lambda: proc.poll())
                if exit_code is None:
                    print(f"[{server_name}] WARNING: Process still running after kill attempt")
                else:
                    print(f"[{server_name}] Process killed successfully (exit code: {exit_code})")
            
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


async def force_kill_all_processes(server_name):
    print(f"[{server_name}] FORCE KILL: Attempting to kill all related processes...")
    
    if os.name == 'nt':
        try:
            import psutil
            
            def find_all_processes():
                java_processes = []
                cmd_processes = []
                
                for p in psutil.process_iter(['pid', 'name', 'cmdline', 'ppid']):
                    try:
                        if p.info['name']:
                            name_lower = p.info['name'].lower()
                            cmdline = p.info['cmdline'] or []
                            cmdline_str = ' '.join(str(arg) for arg in cmdline).lower()
                            
                            if 'java.exe' in name_lower:
                                if any('minecraft' in str(arg).lower() or 'server' in str(arg).lower() or 'forge' in str(arg).lower() for arg in cmdline):
                                    java_processes.append(p)
                            
                            if 'cmd.exe' in name_lower:
                                if any('atm10' in cmdline_str or 'minecraft' in cmdline_str or server_name in cmdline_str for arg in cmdline if arg):
                                    cmd_processes.append(p)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                return java_processes, cmd_processes
            
            loop = asyncio.get_event_loop()
            java_processes, cmd_processes = await loop.run_in_executor(executor, find_all_processes)
            
            killed_count = 0
            
            for java_proc in java_processes:
                try:
                    print(f"[{server_name}] FORCE KILL: Killing Java process PID {java_proc.pid}...")
                    def kill_java():
                        java_proc.kill()
                    
                    await loop.run_in_executor(executor, kill_java)
                    await asyncio.sleep(0.5)
                    
                    def check_java():
                        return java_proc.is_running()
                    
                    if not await loop.run_in_executor(executor, check_java):
                        print(f"[{server_name}] FORCE KILL: Successfully killed Java process PID {java_proc.pid}")
                        killed_count += 1
                    else:
                        print(f"[{server_name}] FORCE KILL: WARNING - Java process PID {java_proc.pid} still running")
                except psutil.NoSuchProcess:
                    print(f"[{server_name}] FORCE KILL: Java process PID {java_proc.pid} already exited")
                    killed_count += 1
                except psutil.AccessDenied as e:
                    print(f"[{server_name}] FORCE KILL: ERROR - Access denied killing Java process PID {java_proc.pid}: {e}")
            
            for cmd_proc in cmd_processes:
                try:
                    print(f"[{server_name}] FORCE KILL: Killing cmd.exe process PID {cmd_proc.pid}...")
                    def kill_cmd():
                        cmd_proc.kill()
                    
                    await loop.run_in_executor(executor, kill_cmd)
                    await asyncio.sleep(0.5)
                    
                    def check_cmd():
                        return cmd_proc.is_running()
                    
                    if not await loop.run_in_executor(executor, check_cmd):
                        print(f"[{server_name}] FORCE KILL: Successfully killed cmd.exe process PID {cmd_proc.pid}")
                        killed_count += 1
                    else:
                        print(f"[{server_name}] FORCE KILL: WARNING - cmd.exe process PID {cmd_proc.pid} still running")
                except psutil.NoSuchProcess:
                    print(f"[{server_name}] FORCE KILL: cmd.exe process PID {cmd_proc.pid} already exited")
                    killed_count += 1
                except psutil.AccessDenied as e:
                    print(f"[{server_name}] FORCE KILL: ERROR - Access denied killing cmd.exe process PID {cmd_proc.pid}: {e}")
            
            if server_name in processes:
                processes[server_name] = None
            
            print(f"[{server_name}] FORCE KILL: Completed. Killed {killed_count} process(es)")
            return True, f"Force killed {killed_count} process(es)"
            
        except ImportError:
            return False, "psutil not available for force kill"
        except Exception as e:
            print(f"[{server_name}] FORCE KILL: Exception: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error during force kill: {str(e)}"
    else:
        return False, "Force kill only available on Windows"


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
