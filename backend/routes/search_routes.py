from flask import Blueprint, request, jsonify
from auth import token_required, get_optional_user
from models import HistoryModel, SavedAnswerModel
from services.search_service import SearchService

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/api/search', methods=['POST'])
def search():
    data = request.get_json(silent=True) or {}
    query = data.get('query', '').strip()
    file_name = data.get('file_name', '')
    file_content = data.get('file_content', '')

    if not query and not file_content:
        return jsonify({'success': False, 'error': 'Search query or uploaded file is required.'}), 400

    # Execute parallel multi-source search + consensus detection + file code analysis
    result = SearchService.execute_multi_source_search(query, file_name=file_name, file_content=file_content)

    # If the user is logged in, auto-log query in search history
    user = get_optional_user()
    if user:
        try:
            HistoryModel.add(
                user_id=user['id'],
                query=query,
                topic=result.get('topic', 'general'),
                sources_count=len(result.get('sources_searched', []))
            )
        except Exception as e:
            print(f"Error logging search history: {e}")

    return jsonify(result), 200

@search_bp.route('/api/related', methods=['POST'])
def related_questions():
    data = request.get_json(silent=True) or {}
    query = data.get('query', '').strip()
    questions = SearchService.get_related_questions(query) if query else []
    return jsonify({'success': True, 'questions': questions}), 200

@search_bp.route('/api/history', methods=['GET'])
@token_required
def get_history():
    user = getattr(request, 'current_user', None)
    history = HistoryModel.get_by_user(user['id'])
    return jsonify({'success': True, 'history': history}), 200

@search_bp.route('/api/history/save', methods=['POST'])
@token_required
def save_answer():
    user = getattr(request, 'current_user', None)
    data = request.get_json(silent=True) or {}

    query_id = data.get('query_id', '')
    source = data.get('source', '').strip()
    answer = data.get('answer', '').strip()
    url = data.get('url', '')
    confidence = float(data.get('confidence', 0.5))

    if not source or not answer:
        return jsonify({'success': False, 'error': 'Source and answer body are required.'}), 400

    saved_id = SavedAnswerModel.save(
        user_id=user['id'],
        query_id=query_id,
        source=source,
        answer=answer,
        url=url,
        confidence=confidence
    )

    return jsonify({'success': True, 'message': 'Saved', 'saved_id': saved_id}), 200

@search_bp.route('/api/saved', methods=['GET'])
@token_required
def get_saved():
    user = getattr(request, 'current_user', None)
    saved = SavedAnswerModel.get_by_user(user['id'])
    return jsonify({'success': True, 'saved': saved}), 200
