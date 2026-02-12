from app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug mode is on for development (auto-reloads when you save files)
    app.run(debug=True)