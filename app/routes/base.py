from flask import render_template, request, redirect
import requests


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors."""
        return render_template('error/400.html'), 400

    @app.errorhandler(401)
    def not_authorized(error):
        """Handle 401 errors."""
        return render_template('error/401.html'), 401

    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors."""
        return render_template('error/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        old_site_url = 'http://adicu.github.com' + request.path
        try:
            response = requests.head(old_site_url, allow_redirects=True)
            if response.status_code == 200:
                return redirect(old_site_url)
        except requests.exceptions.ConnectionError:
            pass

        return render_template('error/404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors."""
        return render_template('error/405.html', method=request.method), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 errors."""
        return render_template('error/500.html'), 500
