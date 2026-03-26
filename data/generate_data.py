import pandas as pd
import numpy as np

n = 20000

data = pd.DataFrame({
    "timestamp": pd.date_range(start="2026-01-01", periods=n, freq="S"),
    "user_id": np.random.randint(1000, 5000, n),
    "session_id": np.random.randint(10000, 20000, n),
    "video_id": np.random.randint(1, 500, n),
    "bitrate": np.random.choice([240, 360, 480, 720, 1080], n),
    "startup_time": np.round(np.random.exponential(2, n), 2),
    "buffer_count": np.random.poisson(1.2, n),
    "buffer_duration": np.round(np.random.exponential(1.5, n), 2),
    "watch_time": np.random.randint(30, 1800, n),
    "error_code": np.random.choice([0, 1, 2], n, p=[0.9, 0.08, 0.02]),
    "device_type": np.random.choice(["mobile", "desktop", "tv"], n),
    "network_type": np.random.choice(["WiFi", "4G", "5G"], n)
})

data.to_csv("../backend/streaming_data.csv", index=False)
print("Data generated!")