import requests
import time

def detect_faces(api_key, api_secret, image_path):
    detect_url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    detect_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "return_attributes": "facequality"
    }

    files = {
        "image_file": open(image_path, "rb")
    }

    response = requests.post(detect_url, data=detect_data, files=files)
    return response.json()

def analyze_faces(api_key, api_secret, face_tokens):
    analyze_url = "https://api-us.faceplusplus.com/facepp/v3/face/analyze"
    analyze_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "face_tokens": ','.join(face_tokens),
        "return_attributes": "gender,age,beauty"
    }

    time.sleep(2)  # Ajouter une pause de 2 secondes entre les requêtes
    response = requests.post(analyze_url, data=analyze_data)
    return response.json()

def is_beautiful(beauty_score, threshold=70):
    return beauty_score >= threshold

def evaluate_image(api_key, api_secret, image_path, threshold=70):
    print("Starting face detection...")
    detect_result = detect_faces(api_key, api_secret, image_path)
    print(f"Detection result: {detect_result}")
    
    if "faces" in detect_result and detect_result["faces"]:
        face_tokens = [face["face_token"] for face in detect_result["faces"]]
        analyze_result = analyze_faces(api_key, api_secret, face_tokens)
        print(f"Analyze result: {analyze_result}")

        if "faces" in analyze_result:
            for face in analyze_result["faces"]:
                beauty = face["attributes"]["beauty"]
                female_beauty_score = beauty['female_score']
                male_beauty_score = beauty['male_score']
                is_beautiful_result = is_beautiful(female_beauty_score, threshold)
                return {
                    "beautiful": is_beautiful_result,
                    "female_score": female_beauty_score,
                    "male_score": male_beauty_score
                }
    return {"beautiful": False, "female_score": 0, "male_score": 0}

if __name__ == "__main__":
    api_key = "D-0FxSRjadOI6gja3opbnwjtxaLWlqKy"
    api_secret = "JceEOYbLxQQnhn1MRgRw7UEu12dS18Uf"
    image_path = "/Users/frederic/tinder-bot/profile_image.jpg"  # Path to the extracted image

    print(f"Evaluating image at: {image_path}")
    result = evaluate_image(api_key, api_secret, image_path)
    print(f"Image: {'Belle' if result['beautiful'] else 'Pas Belle'} (Female Score: {result['female_score']}, Male Score: {result['male_score']})")
