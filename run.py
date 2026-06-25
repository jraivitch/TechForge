from app import create_app

app = create_app()

if __name__ == '__main__':
    # Port 5000 is used by macOS AirPlay Receiver (ControlCenter), which
    # causes a 403 in the browser. Use 8000 to avoid the conflict.
    app.run(debug=True, port=8000)
