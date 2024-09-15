from website import create_app

flask_app = create_app()

if __name__ == '__main__':
    # 0.0.0.0 both local host and local ip address
    # debug=True when dev, debug=False when deploy
    flask_app.run(host='0.0.0.0', debug=True)