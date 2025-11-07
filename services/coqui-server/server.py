"""
Custom Coqui TTS Server
Simple Flask server that wraps Coqui TTS for HTTP API
"""
from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import tempfile
import os

app = Flask(__name__)

# Initialize Coqui TTS (loads model on startup)
print("[INFO] Loading Coqui TTS model...")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
print("[SUCCESS] Coqui TTS model loaded!")

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model": "tacotron2-DDC"})

@app.route('/api/tts', methods=['GET'])
def generate_speech():
    """Generate speech from text"""
    text = request.args.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        # Generate audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            output_path = tmp.name
        
        tts.tts_to_file(text=text, file_path=output_path)
        
        # Send file and clean up
        response = send_file(output_path, mimetype='audio/wav')
        
        # Clean up temp file after sending
        @response.call_on_close
        def cleanup():
            try:
                os.unlink(output_path)
            except:
                pass
        
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
