from flask import Flask, request

app = Flask(__name__)

@app.route("/api/report", methods=["POST"])
def report():
    data = request.json
    print("Received report:", data)
    return {"message": "Data received successfully"}, 200

if __name__ == "__main__":
    app.run(port=5000)
