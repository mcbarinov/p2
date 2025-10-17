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

## Cloudflare Tunnel Setup (for iOS Shortcuts Testing)

To test from your iPhone, you need to expose your local server to the internet using Cloudflare Tunnel.

### Install cloudflared

**macOS:**
```bash
brew install cloudflared
```

**Other platforms:**
Download from [developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

### Quick Dev Mode (temporary URL, no registration)

For quick testing, run in a separate terminal:
```bash
just tunnel
```

This generates a temporary URL (changes on restart). **No Cloudflare account needed** - works immediately after install. Perfect for one-off testing.

### Persistent Setup (requires registration, recommended for development)

For a permanent URL that never changes:

1. Sign up for free Cloudflare account at [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up)
2. Authenticate cloudflared:
   ```bash
   cloudflared tunnel login
   ```
3. Create a named tunnel:
   ```bash
   cloudflared tunnel create ios-shortcuts
   ```
4. Get your tunnel ID from the output and create a config file at `~/.cloudflared/config.yml`:
   ```yaml
   tunnel: <your-tunnel-id>
   credentials-file: /Users/<your-username>/.cloudflared/<tunnel-id>.json

   ingress:
     - hostname: your-tunnel-name.cfargotunnel.com
       service: http://localhost:8000
     - service: http_status:404
   ```
5. Run the tunnel:
   ```bash
   cloudflared tunnel run ios-shortcuts
   ```

**Advantage:** Your URL stays the same forever. Set it once in iOS Shortcuts and never update it again.

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

1. Start your server with `just dev`
2. Start tunnel with `just tunnel` and copy the URL (e.g., `https://abc-123.trycloudflare.com`)
3. Open Shortcuts app on iOS and tap **+** to create new Shortcut
4. Add **"Take Photo"** action
5. Add **"Get Contents of URL"** action and configure it:
   - **URL:** `https://abc-123.trycloudflare.com/upload` (use your tunnel URL)
   - **Method:** Tap and select **POST**
   - **Headers:** Tap "Add new header"
     - Key: `X-API-KEY`
     - Value: `your-secret-key` (from your .env file)
   - **Request Body:** Tap and select **Form**
   - **Form fields:** After selecting Form, tap **"Add new field"** button
     - Field name: `file`
     - Field value: Tap the field and select **"Photo"** (the output from Take Photo action above)
   - **Optional:** Add another field with name `filename` and custom value
6. Name your shortcut (e.g., "Upload Photo")
7. Run the shortcut to test

**Tip:** Use the persistent tunnel setup to get a permanent URL, so you don't need to update it in your shortcut every time you restart.

## Project Structure

```
.
├── main.py          # FastAPI application
├── justfile         # Task runner for dev and tunnel
├── attachments/     # Uploaded photos
└── .env             # API key configuration
```
