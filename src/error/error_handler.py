from flask import app


@app.errorhandler(Exception)
def all_exception_handler(error):
   return 'Error', 500

