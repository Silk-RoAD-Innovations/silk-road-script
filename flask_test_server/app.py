from flask import Flask, jsonify, url_for

app = Flask(__name__, static_url_path='/static')

@app.route('/image')
def get_image_url():
    image_url = {"url": url_for('static', filename='dummyimage.png', _external=True)}
    return jsonify(image_url)

@app.route('/wallpaper/update')
def get_update_info():
    update_info = {"update": url_for('static', filename='update.exe', _external=True), "version": 0}
    return jsonify(update_info)

if __name__ == '__main__':
    app.run(debug=True)