# iOS Shortcuts Photo Upload API

Learning project for iOS Shortcuts integration. Simple FastAPI server that accepts photo uploads with API key authentication.

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Create `.env` file:
   ```
   API_KEY=your-secret-key
   ```
4. Run the server:
   ```bash
   fastapi dev main.py
   ```

Server runs at `http://localhost:8000`

## API

### POST /upload

Upload a photo with optional filename.

**Headers:**
- `X-API-KEY`: Required authentication key

**Form Data:**
- `file`: Photo file (required)
- `filename`: Custom filename without extension (optional, defaults to timestamp)

**Response:**
```json
{
  "filename": "photo_123456789.jpg",
  "size": 1024000
}
```

## Usage Example

```bash
curl -X POST http://localhost:8000/upload \
  -H "X-API-KEY: your-secret-key" \
  -F "file=@photo.jpg" \
  -F "filename=my_photo"
```

Files are saved to `attachments/` directory.

## iOS Shortcuts Setup

1. Create new Shortcut
2. Add "Take Photo" action
3. Add "Get Contents of URL" action:
   - URL: `http://your-server:8000/upload`
   - Method: POST
   - Headers: `X-API-KEY` = `your-secret-key`
   - Request Body: Form
   - Add field: `file` = Photo from step 1
   - Add field: `filename` = custom name (optional)
4. Run the shortcut

## Project Structure

```
.
├── main.py          # FastAPI application
├── attachments/     # Uploaded photos
└── .env             # API key configuration
```
