from flask import Blueprint, request, jsonify, current_app, abort
videos_bp = Blueprint('videos_bp', __name__)
from app.middlewares.auth import require_api_key

@videos_bp.route('/', methods=['POST'])
@require_api_key
def upload_video():
    if 'video' not in request.files:
        return jsonify({'message': 'No file provided'}), 400
    file = request.files['video']
    label = request.form.get('label')
    if not label:
        return jsonify({'message': 'No label provided'}), 400
    try: 
        video = current_app.video_service.create(file, label)
        response = {
            "message": "Video uploaded successfully",
            "video_id": video.id,
            "filename": video.file_name,
            "duration": video.length,
            "size": video.size,
            "upload_time": video.uploaded_at
        }
        print(response)
        return jsonify(response), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

@videos_bp.route('/<int:id>/link', methods=['GET'])
def get_video_link(id):
        try: 
            video = current_app.video_service.get(id)
        except Exception as e:
            current_app.logger.exception("Error retrieving video with id %s", id)
            return jsonify({'message': str(e)}), 503
        
        if not video:
            current_app.logger.error("Video not found for id %s", id)
            return jsonify({'message': 'Video not found'}), 404
        
        expiry_time_minutes = request.args.get('expiry_time_minutes',type=int)
        current_app.logger.info("Received expiry_time_minutes: %s for video id: %s", expiry_time_minutes, id)
        try: 
            download_url = current_app.video_service.get_video_link(id, expiry_time_minutes)
        except Exception as e:
            current_app.logger.exception("Error generating download link for video id %s", id)
            return jsonify({'message': str(e)}), 500
        
        return jsonify({'download_url': download_url, 'expires_in': expiry_time_minutes}), 200


@videos_bp.route('/download-file', methods=['GET'])
def download_file():
    token = request.args.get('token')
    if not token:
        abort(400, description="Missing token")

    try: 
        return current_app.video_service.download(token)
    except Exception as e:
        return jsonify({'message': str(e)}), 500