import re
import logging


def regex_description(product, data):
    if not data:
        return dict()
    first_word = product.split()[0]
    
    url = data['url']

    start_point    = "<p><strong>İçindekiler</strong><br>"
    end_point      = "</p><p><strong>"
    pattern        = "{}(.+?){}".format(start_point, end_point)
    ingredients_re = re.findall(pattern, data['description'])
    ingredients    = ingredients_re[0] if ingredients_re else None

    start_point  = "<p><strong>Alerjen Uyarısı</strong><br>"
    end_point    = "</p><p><strong>"
    pattern      = "{}(.+?){}".format(start_point, end_point)
    allergens_re = re.findall(pattern, data['description'])
    allergens    = allergens_re[0] if allergens_re else None
    
    try:
        image_link = data['mainEntity']['offers']['itemOffered'][0]['offers']['image']
    except:
        image_link = None
        logging.error("Couldn't find any image: {}".format)

    data = {
        "Product"     : first_word,
        "url"         : url,
        "image_link"  : image_link,
        "Ingredients" : ingredients,
        "Allergens"   : allergens
    }
    logging.info("I found the infos. Here they are:\n{}".format(data))
    return data


