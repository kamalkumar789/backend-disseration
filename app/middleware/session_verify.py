from flask import session, jsonify, request

def session_verify(app):

    @app.before_request
    def check_session():
        public_routes = ['/auth/login', '/auth/register']

        if request.path in public_routes:
            return 

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
