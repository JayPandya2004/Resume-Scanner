from flask import Flask, request, jsonify
from resume_parser import parse_resume
import pickle

app = Flask(__name__)

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route('/rank', methods=['POST'])
def rank_resumes():
    job_desc = request.form['job_description']
    files = request.files.getlist('resumes')
    
    resume_data = []
    features = []

    for f in files:
        parsed = parse_resume(f)
        resume_data.append(parsed)

        # Example: feature = number of skills + job desc length
        feature_vec = [len(parsed['skills']), len(job_desc.split())]
        features.append(feature_vec)

    predictions = model.predict(features)

    ranked = sorted(zip(resume_data, predictions), key=lambda x: x[1], reverse=True)

    return jsonify([
        {"rank": i+1, "score": float(score), "data": data}
        for i, (data, score) in enumerate(ranked)
    ])

if __name__ == '__main__':
    app.run(debug=True)
