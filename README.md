# BLIP Vision API Backend

FastAPI server for generating scene descriptions from images using the BLIP model.

## Setup

### 1. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: First install takes 5-10 minutes (torch is large). After that, subsequent runs will be fast.

### 3. Run Server
```bash
python app/main.py
```

or with uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Server starts at: `http://localhost:8000`

## API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Describe Scene (Multipart Upload)
```bash
POST http://localhost:8000/v1/vision/describe
Content-Type: multipart/form-data

[Binary image file]
```

### Describe Scene (Base64)
```bash
POST http://localhost:8000/v1/vision/describe-base64
Content-Type: application/json

{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgA..."
}
```

## Testing with cURL

### Test health check
```bash
curl http://localhost:8000/health
```

### Test with image file
```bash
curl -X POST -F "file=@path/to/image.jpg" http://localhost:8000/v1/vision/describe
```

### Response Example
```json
{
  "description": "a person sitting on a bench in a park",
  "confidence": 0.95,
  "processing_time_ms": 1234.5
}
```

## Documentation
After starting server, open: http://localhost:8000/docs

(Interactive Swagger UI for testing all endpoints)

## Project Folder Structure

The backend is organized by responsibility so each file stays small and easy to maintain.

```text
app/
├── main.py
│   Bootstrap FastAPI, logging, middleware, and router registration.
├── core/
│   Global application settings and logger setup.
├── routers/
│   HTTP endpoints only. `meta.py` handles health/root, `vision.py` handles BLIP APIs.
├── schemas/
│   Pydantic request/response models.
├── services/
│   Business logic. `services/vision/` holds model loading, preprocessing, inference, and postprocess helpers.
├── db/
│   Reserved for future database integration.
└── utils/
    Shared helper utilities such as file and image loaders.
```

### Folder Flow

```text
Client Request
  → router
  → service
  → helper / model loader
  → schema response
```

### Maintenance Rules

- Keep `main.py` bootstrap-only.
- Put HTTP concerns in `routers/`.
- Put inference and orchestration in `services/`.
- Move repeated data contracts into `schemas/`.
- Add new feature domains as new router and service folders, not by expanding one file forever.

## Model Info
- **Model**: Salesforce/blip-image-captioning-base
- **Size**: ~350MB (downloaded on first run)
- **Inference Time**: ~1-3 seconds per image (GPU: ~500ms)

## Production Considerations
- Add authentication (API key, JWT)
- Set specific CORS origins
- Add rate limiting
- Use GPU for faster inference
- Add model caching
- Error logging to file

## Troubleshooting

### "ModuleNotFoundError: No module named 'torch'"
```bash
pip install torch torchvision transformers
```

### "CUDA out of memory"
- Use CPU: Remove GPU code, model runs slower but works
- Or: Use smaller BLIP model variant

### "Connection refused" on localhost:8000
- Ensure server started: `python app/main.py`
- Check port 8000 is not in use: `netstat -ano | findstr :8000` (Windows)
