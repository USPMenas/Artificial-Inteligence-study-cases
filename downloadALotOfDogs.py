import os
import requests

def download_images_from_api(api_url, save_path, num_images=200):
    images_got = 0
    while(images_got < num_images):
        response = requests.get(api_url)
        data = response.json()

        print(data)

        if 'message' in data and isinstance(data['message'], list):
            image_urls = data['message'][:num_images]
            for i, img_url in enumerate(image_urls):
                img_data = requests.get(img_url).content
                with open(os.path.join(save_path, f'dog_image_{i + 1 + images_got}.jpg'), 'wb') as f:
                    f.write(img_data)
        else:
            print("Error: Unable to extract image URLs from the API response.")
        images_got =  images_got + 50
        print("\n\n\n You have downloaded {} images. \n\n\n".format(images_got))

# Example usage
api_url = 'https://dog.ceo/api/breeds/image/random/50'
save_path = 'dataset/validation/dogs'
download_images_from_api(api_url, save_path)
