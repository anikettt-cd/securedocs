from app import create_app

# 👇 THIS LINE MUST BE AT THE FAR LEFT (NOT INDENTED)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)