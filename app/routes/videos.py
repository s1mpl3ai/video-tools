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
    

@videos_bp.route('/<int:video_id>/trim', methods=['POST'])
@require_api_key
def trim_video(video_id):
    # Accept start and end times from form data or JSON
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    try:
        start = float(data.get('start'))
        end = float(data.get('end'))
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid start or end time provided'}), 400

    if start < 0 or end <= start:
        return jsonify({'message': 'Start time must be non-negative and end time must be greater than start time'}), 400

    try:
        new_video = current_app.video_service.trim_video(video_id, start, end)
    except ValueError as ve:
        current_app.logger.error("Validation error trimming video %s: %s", video_id, str(ve))
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        current_app.logger.exception("Error trimming video with id %s", video_id)
        return jsonify({'message': str(e)}), 500

    response = {
        'message': 'Video trimmed successfully',
        'new_video_id': new_video.id,
        'file_name': new_video.file_name,
        'duration': new_video.length,
        'size': new_video.size,
        'label': new_video.label,
        'upload_time': new_video.uploaded_at
    }
    return jsonify(response), 200

@videos_bp.route('/merge', methods=['POST'])
@require_api_key
def merge_videos():
    # Expect a JSON body with a key "video_ids" as a list of integers.
    data = request.get_json()
    if not data or 'video_ids' not in data:
        return jsonify({'message': 'video_ids are required'}), 400

    video_ids = data.get('video_ids')
    if not isinstance(video_ids, list) or not video_ids:
        return jsonify({'message': 'video_ids must be a non-empty list'}), 400

    try:
        new_video = current_app.video_service.merge_videos(video_ids)
    except Exception as e:
        current_app.logger.exception("Error merging videos: %s", video_ids)
        return jsonify({'message': str(e)}), 500

    response = {
        'message': 'Videos merged successfully',
        'new_video_id': new_video.id,
        'file_name': new_video.file_name,
        'duration': new_video.length,
        'size': new_video.size,
        'label': new_video.label,
        'upload_time': new_video.uploaded_at
    }
    return jsonify(response), 200

@videos_bp.route('/all', methods=['GET'])
def get_all_videos():
    try:
        video_list = current_app.video_service.get_all_videos()
        return jsonify({"videos": video_list}), 200
    except Exception as e:
        current_app.logger.exception("Error fetching all videos")
        return jsonify({"message": str(e)}), 500
