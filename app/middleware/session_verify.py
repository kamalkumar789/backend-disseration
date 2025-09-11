from flask import session, jsonify, request

def session_verify(app):

    @app.before_request
    def check_session():

        # Allow these routes without authentication
        public_routes = ['/auth/login', '/auth/register', '/api/organizations']

        # Skip session check for OPTIONS requests (preflight)
        if request.method == 'OPTIONS':
            return

        if request.path in public_routes:
            return 

        user_id = session.get('user_id')
        profile_id = session.get('profile_id')

        if not user_id or not profile_id:
            return jsonify({'error': 'Authentication required'}), 401