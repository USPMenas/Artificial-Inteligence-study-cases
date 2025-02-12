import os
import requests

def download_images_from_api(api_url, save_path, num_images=200):
    images_got = 0
    while(images_got < num_images):
        response = requests.get(api_url)
        data = response.json()

        print(data)

        if isinstance(data, list):
                image_urls = [entry['url'] for entry in data][:num_images]
                for i, img_url in enumerate(image_urls):
                    img_data = requests.get(img_url).content
                    with open(os.path.join(save_path, f'cat_image_{i + 1 + images_got}.jpg'), 'wb') as f:
                        f.write(img_data)
        else:
            print("Error: Unable to extract image URLs from the API response.")
        images_got =  images_got + 10
        print("\n\n\n You have downloaded {} images. \n\n\n".format(images_got))

# Example usage
api_url = 'https://api.thecatapi.com/v1/images/search?limit=10'
save_path = 'dataset/validation/cats'
download_images_from_api(api_url, save_path)
