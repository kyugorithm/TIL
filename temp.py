import xml.etree.ElementTree as ET

def extract_bndbox_details_to_file(file_path, output_path):
    # XML 파일 파싱
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # 결과를 저장할 문자열 리스트
    results = []
    
    # 모든 bndbox 요소 찾기
    for bndbox in root.findall('.//bndbox'):
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
        
        # 결과 문자열 포맷
        result_str = f'xc: {xc}, yc: {yc}, w: {w}, h: {h}'
        results.append(result_str)
    
    # 결과를 파일로 저장
    with open(output_path, 'w') as f:
        for result in results:
            f.write(result + '\n')

# 사용 예시
input_file_path = 'path/to/your/xmlfile.xml'
output_file_path = 'path/to/your/output.txt'
extract_bndbox_details_to_file(input_file_path, output_file_path)
