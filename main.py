from app import app
import os

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Enable debug mode only in development
    debug_mode = os.environ.get("FLASK_ENV") == "development" or os.environ.get("DEBUG", "").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
