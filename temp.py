import xml.etree.ElementTree as ET

# Function to parse the XML file and extract bounding box information
def parse_xml_and_save(xml_file_path, output_file_path):
    # Load and parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract bounding box information
    bbox_data = []
    for obj in root.findall('.//object'):
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text
        bbox_data.append(f"{xmin} {ymin} {xmax} {ymax}\n")

    # Save the bounding box information to a text file
    with open(output_file_path, 'w') as file:
        file.writelines(bbox_data)

# Example usage
xml_file_path = 'path_to_your_xml_file.xml'  # Change this to the path of your XML file
output_file_path = 'bounding_boxes.txt'  # The text file where you want to save the data

parse_xml_and_save(xml_file_path, output_file_path)
