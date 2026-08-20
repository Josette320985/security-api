from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VALID_API_KEY = "my-secret-api-key-123"
UNAUTHORIZED_RESPONSE = {"error": "Unauthorized: Invalid or missing API key"}


def validate_api_key():
    """
    Validate the x-api-key header against the configured API key.
    Returns None if valid, or a (response, status_code) tuple if invalid.
    """
    api_key = request.headers.get("x-api-key")
    if api_key != VALID_API_KEY:
        return jsonify(UNAUTHORIZED_RESPONSE), 401
    return None


@app.route("/health", methods=["GET"])
def health():
    """Public health check endpoint."""
    return jsonify({"status": "ok"})


@app.route("/api/data", methods=["GET"])
def get_data():
    """Protected GET endpoint that requires a valid API key."""
    auth_error = validate_api_key()
    if auth_error:
        return auth_error

    return jsonify(
        {
            "message": "Protected data",
            "course": "Security Exercise",
            "status": "success",
        }
    )


@app.route("/api/data", methods=["POST"])
def post_data():
    """Protected POST endpoint that requires a valid API key."""
    auth_error = validate_api_key()
    if auth_error:
        return auth_error

    return jsonify({"message": "POST received"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
