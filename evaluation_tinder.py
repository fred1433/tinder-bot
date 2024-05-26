#evaluation_tinder.py

import requests
import time
import logging

# Configurer le logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='evaluation_tinder.log', filemode='w')
logger = logging.getLogger()

def detect_faces(api_key, api_secret, image_path):
    detect_url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    detect_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "return_attributes": "facequality"
    }

    with open(image_path, "rb") as image_file:
        files = {
            "image_file": image_file
        }
        response = requests.post(detect_url, data=detect_data, files=files)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()

def analyze_faces(api_key, api_secret, face_tokens):
    analyze_url = "https://api-us.faceplusplus.com/facepp/v3/face/analyze"
    analyze_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "face_tokens": ','.join(face_tokens),
        "return_attributes": "gender,age,beauty"
    }

    time.sleep(2)
    response = requests.post(analyze_url, data=analyze_data)
    response.raise_for_status()  # Raise an error for bad HTTP status codes
    return response.json()

def is_beautiful(beauty_score, threshold=65):
    return beauty_score >= threshold

def evaluate_image(api_key, api_secret, image_path, threshold=58):
    logger.info(f"Evaluating image at: {image_path}")
    try:
        detect_result = detect_faces(api_key, api_secret, image_path)
        logger.info(f"Detection result: {detect_result}")
        if "faces" in detect_result and detect_result["faces"]:
            face_tokens = [face["face_token"] for face in detect_result["faces"]]
            analyze_result = analyze_faces(api_key, api_secret, face_tokens)
            logger.info(f"Analyze result: {analyze_result}")

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
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return {"beautiful": False, "female_score": 0, "male_score": 0}

def main():
    api_key = "D-0FxSRjadOI6gja3opbnwjtxaLWlqKy"
    api_secret = "JceEOYbLxQQnhn1MRgRw7UEu12dS18Uf"
    
    profile_count = 0
    image_paths = ["/Users/frederic/tinder-bot/profile_image_tinder.jpg"]  # Liste des chemins d'image à évaluer

    for image_path in image_paths:
        result = evaluate_image(api_key, api_secret, image_path)
        if result["beautiful"]:
            profile_count += 1
        logger.info(f"Image: {'Belle' if result['beautiful'] else 'Pas Belle'} (Female Score: {result['female_score']}, Male Score: {result['male_score']})")
    
    logger.info(f"Total profiles swiped: {profile_count}")

if __name__ == "__main__":
    main()