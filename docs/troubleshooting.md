# NEXUS GRAPH AI - Troubleshooting Guide

## 1. Running FalkorDB in WSL2 (Windows Native Setup)
When running on Windows without Docker Desktop, FalkorDB runs directly inside WSL2 Ubuntu:
1. Install Redis 8.x and FalkorDB v4.22.1 `.so` in WSL2:
   ```bash
   # In WSL2 Ubuntu
   sudo cp falkordb.so /opt/falkordb/falkordb.so
   # Configure /etc/redis/redis.conf:
   loadmodule /opt/falkordb/falkordb.so
   bind 0.0.0.0
   protected-mode no
   ```
2. Start the FalkorDB systemd service in WSL:
   ```bash
   sudo systemctl restart falkordb
   redis-cli ping  # Returns PONG
   ```
3. **WSL2 Idle Sleep Prevention**:
   WSL2 automatically sleeps if no interactive shell or active background process is kept open. To prevent the FalkorDB service from halting when idle:
   ```bash
   # Keep an active process running in background:
   wsl -u root -e bash -c "systemctl start falkordb; while true; do sleep 3600; done"
   ```
4. **Connecting from Windows Host**:
   Windows connects to WSL via the WSL adapter IP (e.g., `172.17.109.154`) or `localhost`. The `backend/app/graph/falkor_client.py` client automatically auto-discovers and falls back between `localhost` and the WSL host IP.

## 2. Windows Port Conflicts & Port 8080
Windows TCP sockets may hold orphaned TIME_WAIT or SYSTEM reservations on port 8000.
The backend is configured to run reliably on **port 8080**:
- Backend: `uvicorn app.main:app --host 127.0.0.1 --port 8080`
- Frontend: `frontend/.env.local` is configured with `NEXT_PUBLIC_API_URL=http://localhost:8080`
- Both ports 8080 and 8000 are supported transparently in `src/lib/api.ts`.

## 3. PyTorch Windows Safetensors & Memory Mapping
**Symptom**: `OSError: [Errno 22] Invalid argument` when loading weights on Windows.
**Resolution**:
In PyTorch on Windows, loading safetensors with `low_cpu_mem_usage=True` triggers Windows filesystem memory mapping limits.
In `backend/app/llm/adapter.py`, `low_cpu_mem_usage=False` is set by default when running on CPU, which eliminates this error and loads the model smoothly.

## 4. FastAPI Event Loop Starvation with CPU Models
**Symptom**: FastAPI server appears unresponsive or times out when agents are running model inference.
**Resolution**:
Synchronous CPU model inference (`model.generate()`) runs intensive calculations in native C++. If called from an `async def` FastAPI route, it blocks the main asyncio thread loop.
All model inference endpoints are defined as synchronous `def` functions, allowing FastAPI to dispatch them automatically to worker threads in its threadpool without starving the async event loop.
