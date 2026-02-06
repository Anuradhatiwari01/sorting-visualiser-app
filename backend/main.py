import time
import io
import pandas as pd
from typing import List, Dict

from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.algorithms import ALGORITHMS, ALGORITHM_METADATA
from backend.utils import generate_array

app = FastAPI(title="SortVision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

last_benchmark_result = None

class BenchmarkRequest(BaseModel):
    algorithms: List[str]
    sizes: List[int]
    dataType: str
    trials: int

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main index.html page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/algorithms")
async def get_algorithms() -> Dict:
    """Returns a list of available algorithms and their metadata."""
    return ALGORITHM_METADATA

@app.post("/api/benchmark")
async def run_benchmark(payload: BenchmarkRequest):
    """Runs performance benchmarks for given algorithms."""
    global last_benchmark_result
    
    results = {}
    for algo_name in payload.algorithms:
        if algo_name not in ALGORITHMS:
            continue
        
        results[algo_name] = []
        sort_function = ALGORITHMS[algo_name]

        for size in payload.sizes:
            trial_times, total_comparisons, total_swaps = [], 0, 0
            for _ in range(payload.trials):
                arr = generate_array(size, payload.dataType)
                start_time = time.perf_counter()
                _, comparisons, swaps = sort_function(arr)
                end_time = time.perf_counter()
                trial_times.append((end_time - start_time) * 1000)
                total_comparisons += comparisons
                total_swaps += swaps
            
            results[algo_name].append({
                "size": size,
                "time": sum(trial_times) / payload.trials,
                "comparisons": total_comparisons / payload.trials,
                "swaps": total_swaps / payload.trials
            })
            

    records = [
        {"Algorithm": name, "Size": p["size"], "DataType": payload.dataType,
         "AvgTime_ms": p["time"], "AvgComparisons": p["comparisons"], "AvgSwaps_Moves": p["swaps"]}
        for name, data in results.items() for p in data
    ]
    last_benchmark_result = pd.DataFrame(records)

    return results

@app.get("/api/download-csv")
async def download_csv():
    """Downloads the last benchmark result as a CSV file."""
    if last_benchmark_result is None or last_benchmark_result.empty:
        raise HTTPException(status_code=404, detail="No benchmark data available.")

    stream = io.StringIO()
    last_benchmark_result.to_csv(stream, index=False)
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=sortvision_benchmark.csv"
    return response

@app.post("/api/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """Accepts a CSV file upload and returns the data as a JSON array."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")
    
    try:
        # Read the uploaded file in-memory
        df = pd.read_csv(io.StringIO(str(file.file.read(), 'utf-8')), header=None)
        if df.shape[1] > 1:
            raise HTTPException(status_code=400, detail="CSV must have only one column of numbers.")
        dataset = df[0].astype(int).tolist()
        return {"dataset": dataset}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
