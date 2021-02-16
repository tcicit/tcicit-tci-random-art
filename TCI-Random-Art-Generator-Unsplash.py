#!/usr/bin/env python3
"""
TCI Art Generator

The program uses imagemagick for generation of random art images.
The program is inspired by the net.art generator by Panos Galanis.
http://net.art-generator.com/
http://net.art-generator.com/nags.html

Unsplash is used as the source for the images. 
You need an API key from unsplash, which you can get for free.

Autor: Thomas Cigolla, 16.02.2021
Version: 1.0

Mögliche Erweiterungen:

- Setzen von EXIF Daten 
- Lesen von Bildern aus einem lokal Verzeichnis
---------------------------------------------------------------
Requirements: 

Directoryes for Output Files und oginal Files

imageMagick min. 7.0.xxx
https://imagemagick.org/

python Wand min. 0.65 
https://docs.wand-py.org/

python 3.8.xxx

"""
import os
import random
import requests
import json
from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing

# unsplash URL 
url = "https://api.unsplash.com/photos/random/?client_id=G7o91KD0qroulewCBGB5NRvyoKW-L_TOaiikOgoS7S8"

# set directorys, put source images in input dir
# input_dir = ("input/")
output_dir = ("output/")
org_dir = ("org/")

# set how many image to generate
number_images = 1

# imagemagik operator / filters 
operators = ( 'plus',
              'difference',
              'displace',
              'multiply',
              'bumpmap',
              'copy_magenta'
              'copy_red',
              'copy_yellow',
              'copy_cyan',
              'copy_green',
              'copy_blue',
              'displace',
              'modulate',
              'luminize',
              'vivid_light',
              'threshold' )

### Functions ###
def draw_img(operators, background_img, overlay_img):

    oper = random.choice(operators)  
#    print ("Operator: ",  oper)
    
    bg_img = background_img.clone()
    ov_img = overlay_img.clone()
    
#    print ("Backgroundsize: ", bg_img.width, bg_img.height )
#    print ("Overlay Size: ", ov_img.width, ov_img.height )

    left_offset = random.randrange(0, bg_img.width - ov_img.width)
#    print("Offset left:", left_offset, left_offset + ov_img.width)
    
    top_offset = random.randrange(0, bg_img.height - ov_img.height)
#    print("Offset height:",top_offset, top_offset + ov_img.height)

    with Drawing() as draw:
        draw.composite(operator=oper, left=left_offset, top=top_offset, width=ov_img.width, height=ov_img.height, image=ov_img)
        draw(bg_img)

    return (bg_img, oper)
    
def linkFetch(url, photo_metadata):
   
    # url = "https://api.unsplash.com/photos/random/?client_id=G7o91KD0qroulewCBGB5NRvyoKW-L_TOaiikOgoS7S8"
    response = requests.get(url)
    raw_url  = response.json()["urls"]["raw"] # URL for raw image on unsplash
    
    photo_id = response.json()["id"]

    photo_metadata[photo_id] = {}
    photo_metadata[photo_id]["user_id"]    = response.json()["user"]["id"] 
    photo_metadata[photo_id]["user_name"]  = response.json()["user"]["name"] 
    photo_metadata[photo_id]["link_html"]  = response.json()["links"]["html"] 
    photo_metadata[photo_id]["created_at"] = response.json()["created_at"]
    
    return (raw_url, photo_metadata, photo_id)

def getImage(raw_url, org_dir, photo_id):
    response = requests.get(raw_url)
    img = Image(blob=response.content)
    
    img.save(filename=org_dir + photo_id + ".jpg") # Save oginal image
   
    return img
    
def make_filename(photo_metadata):
    i = 0
    for key in photo_metadata.keys():
        if (i == 0 ):
            f_name = key
            i += 1
        else:
            f_name = f_name + "-" + key
    return f_name
        
    
### Main ###
for i in range(number_images): 
    photo_metadata = {}
    
    # read random image for processing
    print ("Reding background image")
    raw_url, photo_metadata, bg_id  = linkFetch(url, photo_metadata)
    background_img = getImage(raw_url, org_dir, bg_id)

    print ("Reding first image")
    raw_url, photo_metadata, first_id  = linkFetch(url, photo_metadata)
    first_img = getImage(raw_url, org_dir, first_id)
    
    print ("Reding second image")
    raw_url, photo_metadata, second_id  = linkFetch(url, photo_metadata)
    second_img = getImage(raw_url, org_dir, second_id)
 
    # scale overlay images and preserve aspect ratio
    # scale height to 100px and preserve aspect ratio "img.transform(resize='x100')"
    trans =   str(background_img.width // 5 * 4) + 'x'  # overlay image with 80%
    first_img.transform(resize=trans)
    second_img.transform(resize=trans)
    
    # Test is overlay image smaler as background image
    if (first_img.width > background_img.width):
        print ("First image width to big!")
        continue
    elif (first_img.height > background_img.height):
        print ("First image height to big!")
        continue
    elif (second_img.width > background_img.width):
        print ("Second image width to big!")
        continue
    elif (second_img.height > background_img.height):
        print ("Second image height to big!")
        continue
    else:
        # Create image 
        new_img1, oper = draw_img(operators, background_img, first_img)
        photo_metadata[bg_id]["operator"] = oper

        new_img2, oper = draw_img(operators, new_img1, second_img)
        photo_metadata[first_id]["operator"] = oper
        
        # Make filename
        f_name = make_filename(photo_metadata)
        new_img2.save(filename = output_dir + f_name + ".jpg")
        
        # Save metadata to filsystem
        with open(output_dir + f_name + ".json", "w") as out_file:
            out_file = json.dump(photo_metadata, out_file)
            print ("Filename:",output_dir + f_name + ".jpg")

            
    


#############################################################################
'''
   wand.image.COMPOSITE_OPERATORS = 
  ('undefined', 
  'alpha', 
  'atop', 
  'blend', 
  'blur', 
  'bumpmap', 
  'change_mask', 
  'clear', 
  'color_dodge', 
  'colorize', 
  'copy_black',
  'copy_blue', 
  'copy', 
  'copy_cyan', 
  'copy_green', 
  'copy_magenta', 
  'copy_alpha', 
  'copy_red',  
  'copy_yellow', 
  'darken', 
  'darken_intensity', 
  'difference',
  'displace', 
  'dissolve', 
  'distort', 
  'divide_dst', 
  'divide_src', 
  'dst_atop', 
  'dst', 
  'dst_in', 
  'dst_out', 
  'dst_over', 
  'exclusion', 
  'hard_light', 
  'hard_mix', 
  'hue', 
  'in', 
  'intensity', 
  'lighten', 
  'lighten_intensity', 
  'linear_burn', 
  'linear_dodge', 
  'linear_light', 
  'luminize', 
  'mathematics', 
  'minus_dst', 
  'minus_src', 
  'modulate', 
  'modulus_add',
  'modulus_subtract', 
  'multiply', 
  'no', 
  'out', 
  'over', 
  'overlay', 
  'pegtop_light', 
  'pin_light', 
  'plus', 
  'replace', 
  'saturate', 
  'screen', 
  'soft_light', 
  'src_atop', 
  'src', 
  'src_in', 
  'src_out', 
  'src_over', 
  'threshold',
  'vivid_light', 
  'xor', 
  'stereo')
'''
 
 
 
