import requests
import os
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

def is_beautiful(beauty_score, threshold=7):
    return beauty_score >= threshold

def main():
    api_key = "D-0FxSRjadOI6gja3opbnwjtxaLWlqKy"
    api_secret = "JceEOYbLxQQnhn1MRgRw7UEu12dS18Uf"
    image_folder = "/Users/frederic/tinder-bot/"  # Remplacez par le chemin de votre dossier
    threshold = 70  # Seuil pour décider si une image est "belle" ou "pas belle"

    for image_name in os.listdir(image_folder):
        if image_name.lower().endswith('.png'):
            image_path = os.path.join(image_folder, image_name)
            
            if os.path.isfile(image_path):
                print(f"Analyzing {image_name}...")
                detect_result = detect_faces(api_key, api_secret, image_path)
                
                if "faces" in detect_result and detect_result["faces"]:
                    face_tokens = [face["face_token"] for face in detect_result["faces"]]
                    analyze_result = analyze_faces(api_key, api_secret, face_tokens)
                    
                    if "faces" in analyze_result:
                        for face in analyze_result["faces"]:
                            beauty = face["attributes"]["beauty"]
                            female_beauty_score = beauty['female_score']
                            male_beauty_score = beauty['male_score']
                            is_beautiful_result = is_beautiful(female_beauty_score, threshold)
                            print(f"{image_name}: {'Belle' if is_beautiful_result else 'Pas Belle'} (Female Score: {female_beauty_score}, Male Score: {male_beauty_score})")
                    else:
                        print(f"No face data in analyze result for {image_name}.")
                else:
                    print(f"No face detected in {image_name}.")
            else:
                print(f"Image not found: {image_name}")

if __name__ == "__main__":
    main()
