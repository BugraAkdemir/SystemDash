import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import psutil
import platform
import wmi
import os
import cputemp


app = FastAPI()

def bytes_to_mb(b):
    return round(b / (1024 * 1024), 2)

def get_cpu_temperature():
    try:
        w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
        sensors = w.Sensor()
        # Öncelikle "Tctl" içeren sensörlere bak
        for sensor in sensors:
            if sensor.SensorType == "Temperature" and ("Tctl" in sensor.Name or "Core" in sensor.Name):
                return round(sensor.Value, 1)
        # Bulamazsa ilk Temperature sensörünü döndür
        for sensor in sensors:
            if sensor.SensorType == "Temperature":
                return round(sensor.Value, 1)
        return None
    except Exception:
        return None
    


@app.get("/", response_class=HTMLResponse)
async def root():
    return html_content

@app.get("/api/stats")
async def stats():
    psutil.cpu_percent(interval=None)
    for p in psutil.process_iter():
        try:
            p.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(0.5)

    cpu_percent = psutil.cpu_percent(interval=None)
    ram_percent = psutil.virtual_memory().percent
    cpu_temp = get_cpu_temperature()
    

    procs = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            cpu = p.cpu_percent(interval=None)
            mem_mb = bytes_to_mb(p.info['memory_info'].rss) if p.info['memory_info'] else 0
            procs.append({
                "pid": p.pid,
                "name": p.info['name'],
                "cpu": cpu,
                "ram": mem_mb,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    procs = sorted(procs, key=lambda x: x['cpu'], reverse=True)[:5]

    return JSONResponse({
        "cpu": cpu_percent,
        "ram": ram_percent,
        "cpu_temp": cpu_temp,
        "processes": procs,
        "system": platform.system()
    })

html_content = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bilgisayar Durumu</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #121212;
            color: #e0e0e0;
            margin: 0; padding: 20px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        h1 {
            text-align: center; margin-bottom: 25px;
            color: #00bcd4;
            font-weight: 700; font-size: 2.5rem;
        }
        .stats {
            display: flex; justify-content: center;
            gap: 40px; margin-bottom: 40px;
            flex-wrap: wrap;
        }
        .stat-box {
            background: #1f1f1f; padding: 25px 30px;
            border-radius: 12px; width: 180px;
            text-align: center; box-shadow: 0 0 15px #00bcd4aa;
            transition: transform 0.3s ease;
        }
        .stat-box:hover {
            transform: scale(1.05);
        }
        .stat-box h3 {
            margin-bottom: 15px;
            font-size: 1.3rem; color: #00e5ff;
        }
        .stat-box p {
            font-size: 2.3rem; font-weight: 700; margin: 0;
            color: #ffffff;
        }
        table {
            width: 100%; max-width: 900px;
            margin: 0 auto 50px auto;
            border-collapse: collapse;
            background: #1f1f1f;
            border-radius: 12px; overflow: hidden;
            box-shadow: 0 0 20px #00bcd4aa;
            font-size: 1rem;
        }
        thead tr {
            background-color: #00bcd4;
            color: #121212;
            font-weight: 700; font-size: 1.1rem;
        }
        th, td {
            padding: 14px 20px;
            border-bottom: 1px solid #333;
            text-align: left;
        }
        tbody tr:hover {
            background-color: #333;
            cursor: default;
        }
        .footer {
            text-align: center;
            font-size: 0.9rem;
            color: #777;
            margin-bottom: 20px;
        }
        #fullscreen-btn {
            position: fixed; bottom: 25px; right: 25px;
            background-color: #00bcd4; border: none;
            padding: 15px 25px; border-radius: 50px;
            color: #121212; font-weight: 700; font-size: 1.1rem;
            box-shadow: 0 0 15px #00bcd4bb;
            cursor: pointer; transition: background-color 0.3s ease;
            z-index: 9999;
        }
        #fullscreen-btn:hover {
            background-color: #00e5ff;
        }
        @media (max-width: 600px) {
            .stats {
                flex-direction: column;
                align-items: center;
            }
            .stat-box {
                width: 80%;
                max-width: 300px;
            }
            table {
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <h1>Bilgisayar Durumu</h1>
    <div class="stats">
        <div class="stat-box">
            <h3>CPU Kullanımı</h3>
            <p id="cpu">-- %</p>
        </div>
        <div class="stat-box">
            <h3>RAM Kullanımı</h3>
            <p id="ram">-- %</p>
        </div>
        <div class="stat-box">
            <h3>CPU Sıcaklığı</h3>
            <p id="temp">-- °C</p>
        </div>
    </div>

    <h2 style="text-align:center; margin-bottom: 15px; color:#00bcd4;">Açık Programlar (En Çok CPU Kullanan 5)</h2>
    <table>
        <thead>
            <tr>
                <th>PID</th>
                <th>İsim</th>
                <th>CPU (%)</th>
                <th>RAM (MB)</th>
            </tr>
        </thead>
        <tbody id="process-list"></tbody>
    </table>

    <div class="footer">
        <p>FastAPI &amp; Psutil &amp; WMI ile Canlı Sistem İzleme</p>
    </div>

    <button id="fullscreen-btn" onclick="goFullScreen()">Tam Ekran</button>

    <script>
        async function fetchStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();

                document.getElementById('cpu').textContent = data.cpu.toFixed(1) + ' %';
                document.getElementById('ram').textContent = data.ram.toFixed(1) + ' %';
                document.getElementById('temp').textContent = data.cpu_temp !== null ? data.cpu_temp + ' °C' : 'N/A';

                const tbody = document.getElementById('process-list');
                tbody.innerHTML = '';

                data.processes.forEach(proc => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${proc.pid}</td>
                        <td>${proc.name}</td>
                        <td>${proc.cpu.toFixed(1)}</td>
                        <td>${proc.ram.toFixed(1)}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (error) {
                console.error('Hata:', error);
            }
        }

        fetchStats();
        setInterval(fetchStats, 2000);

        function goFullScreen() {
            const elem = document.documentElement;
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) {
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) {
                elem.msRequestFullscreen();
            }
        }
    </script>
</body>
</html>
"""
