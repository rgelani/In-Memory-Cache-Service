## 📌 Project Overview

This project is a **real-time in-memory caching system** that lets you test and visualize how different cache eviction policies work in practice: **LRU (Least Recently Used)**, **LFU (Least Frequently Used)**, **ARC (Adaptive Replacement Cache)**, and **LRU with TTL**.

It solves a common real-world problem:  
modern applications often become slow because they repeatedly:

- Call the same external APIs  
- Hit the database for the same data  
- Run expensive computations again and again  

By caching frequently accessed data **in memory**, this system helps:

- Reduce response times  
- Decrease load on databases and external services  
- Improve overall performance and scalability  

You can also paste any external JSON API URL into the dashboard, and the system will:

1. Fetch the response from the API  
2. Cache it using the selected policy  
3. Serve subsequent requests instantly from cache  
4. Show whether the data came from **API** or **cache**, along with live hit-rate changes  

---

## 🧩 What This Project Does

- Implements multiple cache policies (LRU, LFU, ARC, LRU+TTL) as reusable Python components  
- Exposes them via a **FastAPI** backend as a simple HTTP cache service  
- Provides a **React dashboard** to:
  - Switch between policies  
  - View real-time stats (hit rate, hits, misses, evictions, current size)  
  - Generate demo traffic to stress-test the cache  
  - Test external API URLs and see caching behavior visually  

---

## 🛠 Technologies & Tools

**Backend:**
- Python
- FastAPI
- Uvicorn
- Pydantic / Pydantic Settings
- `sortedcontainers` (for TTL management)
- Custom implementations of LRU, LFU, ARC, LRU+TTL

**Frontend:**
- React
- Vite
- Recharts (for live hit-rate graph)
- Fetch API

**Other:**
- CORS Middleware (to allow frontend ↔ backend communication)
- JSON-based HTTP API for integration with other services
