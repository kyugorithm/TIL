import xml.etree.ElementTree as ET

def extract_bndbox_details(file_path):
    # XML 파일 파싱
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # bndbox 요소 찾기
    bndbox = root.find('.//bndbox')
    
    # xmin, ymin, xmax, ymax 값 추출
    xmin = int(bndbox.find('xmin').text)
    ymin = int(bndbox.find('ymin').text)
    xmax = int(bndbox.find('xmax').text)
    ymax = int(bndbox.find('ymax').text)
    
    # 너비와 높이 계산
    w = xmax - xmin
    h = ymax - ymin
    
    # 중심점 계산
    xc = xmin + w / 2
    yc = ymin + h / 2
    
    return xc, yc, w, h

# 사용 예시
file_path = 'path/to/your/xmlfile.xml'
xc, yc, w, h = extract_bndbox_details(file_path)
print(f'xc: {xc}, yc: {yc}, w: {w}, h: {h}')
