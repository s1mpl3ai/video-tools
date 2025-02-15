from flask import Blueprint, request, jsonify ,current_app
videos_bp = Blueprint('videos_bp', __name__)

@videos_bp.route('/', methods=['POST'])
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
    
   