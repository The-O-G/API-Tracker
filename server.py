from flask import Flask, request, jsonify, render_template
from auth_wrapper import require_auth
from model_ops import Model_Operations
from url_processor import URLProcessor
from response_parser import ResponseParser
from models import URLList
import json

app = Flask(__name__)
db = Model_Operations()

# -----------------------------------------------------------
# FRONTEND - Serve the HTML interface
# -----------------------------------------------------------
@app.route('/')
def index():
    """Serve the main frontend interface."""
    return render_template("static.html")

# -----------------------------------------------------------
# CREATE - Add a new URL
# -----------------------------------------------------------
@app.route('/api/urls', methods=['POST'])
@require_auth
def create_url():
    """
    Create a new URL entry.
    Expected JSON body:
    {
        "name": "string",
        "url": "string",
        "is_active": bool (optional, default: true),
        "has_filter": bool (optional, default: false),
        "filter_value": "string" (optional, filter function code)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if 'name' not in data or 'url' not in data:
            return jsonify({"error": "Missing required fields: name, url"}), 400
        
        new_url = db.create_url(
            name=data['name'],
            url=data['url'],
            is_active=data.get('is_active', True),
            has_filter=data.get('has_filter', False),
            filter_value=data.get('filter_value')
        )
        
        return jsonify({
            "message": "URL created successfully",
            "data": {
                "id": new_url.id,
                "name": new_url.name,
                "url": new_url.url,
                "is_active": new_url.is_active,
                "has_filter": new_url.has_filter,
                "filter": new_url.filter
            }
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# READ - Get a single URL by ID
# -----------------------------------------------------------
@app.route('/api/urls/<int:url_id>', methods=['GET'])
@require_auth
def get_url(url_id):
    """Get a single URL by its ID."""
    try:
        url_item = db.get_url(url_id)
        
        if not url_item:
            return jsonify({"error": "URL not found"}), 404
        
        return jsonify({
            "id": url_item.id,
            "name": url_item.name,
            "url": url_item.url,
            "is_active": url_item.is_active,
            "has_filter": url_item.has_filter,
            "filter": url_item.filter
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# READ - Get all URLs
# -----------------------------------------------------------
@app.route('/api/urls', methods=['GET'])
@require_auth
def get_all_urls():
    """Get all URLs, with optional filtering by active status."""
    try:
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        
        if active_only:
            urls = db.get_all_active_urls()
        else:
            urls = db.get_all_urls()
        
        url_list = [
            {
                "id": url.id,
                "name": url.name,
                "url": url.url,
                "is_active": url.is_active,
                "has_filter": url.has_filter,
                "filter": url.filter
            }
            for url in urls
        ]
        
        return jsonify({
            "count": len(url_list),
            "urls": url_list
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# UPDATE - Update an existing URL
# -----------------------------------------------------------
@app.route('/api/urls/<int:url_id>', methods=['PUT', 'PATCH'])
@require_auth
def update_url(url_id):
    """
    Update an existing URL.
    Accepts partial updates - only provided fields will be updated.
    Expected JSON body (all fields optional):
    {
        "name": "string",
        "url": "string",
        "is_active": bool,
        "has_filter": bool,
        "filter": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        updated_url = db.update_url(url_id, **data)
        
        if not updated_url:
            return jsonify({"error": "URL not found"}), 404
        
        return jsonify({
            "message": "URL updated successfully",
            "data": {
                "id": updated_url.id,
                "name": updated_url.name,
                "url": updated_url.url,
                "is_active": updated_url.is_active,
                "has_filter": updated_url.has_filter,
                "filter": updated_url.filter
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# DELETE - Delete a URL
# -----------------------------------------------------------
@app.route('/api/urls/<int:url_id>', methods=['DELETE'])
@require_auth
def delete_url(url_id):
    """Delete a URL by its ID."""
    try:
        success = db.delete_url(url_id)
        
        if not success:
            return jsonify({"error": "URL not found"}), 404
        
        return jsonify({"message": "URL deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# RUN - Process all active URLs
# -----------------------------------------------------------
@app.route('/api/urls/run', methods=['POST'])
@require_auth
def run_urls():
    """
    Process all active URLs by fetching their content and applying filters.
    Returns the parsed results from all URLs.
    """
    try:
        list_urls = db.get_all_active_urls()
        
        if not list_urls:
            return jsonify({
                "message": "No active URLs to process",
                "results": []
            }), 200
        
        processor = URLProcessor()
        responses = processor.check_urls(list_urls)
        
        parsed_values = ResponseParser().parse_all(responses, list_urls)
        
        return jsonify({
            "message": "URLs processed successfully",
            "processed_count": len(responses),
            "total_active_urls": len(list_urls),
            "results": parsed_values
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# Health check endpoint
# -----------------------------------------------------------
@app.route('/api/health', methods=['GET'])
@require_auth
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "URL Processor API"
    }), 200


# -----------------------------------------------------------
# Error handlers
# -----------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)