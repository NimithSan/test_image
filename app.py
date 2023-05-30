from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in the request'}), 400
    
    image_file = request.files['image']
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)
    
    return jsonify({'message': 'Image uploaded successfully'}), 200


@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(image_path):
        return jsonify({'error': 'Image not found'}), 404
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/images', methods=['GET'])
def get_all_images():
    image_files = os.listdir(app.config['UPLOAD_FOLDER'])
    image_urls = []
    for filename in image_files:
        image_urls.append(request.host_url + 'image/' + filename)
    
    return jsonify({'images': image_urls})


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
