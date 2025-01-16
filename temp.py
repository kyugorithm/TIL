from psd_tools import PSDImage

def analyze_layer(layer, depth=0):
    indent = "  " * depth
    
    # is_group() 메서드로 그룹 체크
    if layer.is_group():
        print(f"{indent}그룹 레이어: {layer.name}")
        # descendants() 메서드를 사용하여 모든 하위 레이어에 접근
        for child in layer.descendants():
            analyze_layer(child, depth + 1)
    
    # 텍스트 레이어인 경우
    elif layer.kind == 'type':
        print(f"{indent}텍스트 레이어: {layer.name}")
        print(f"{indent}텍스트 내용: {layer.text}")
        if hasattr(layer, 'font'):
            print(f"{indent}폰트: {layer.font}")
    
    # 기타 일반 레이어
    else:
        print(f"{indent}일반 레이어: {layer.name}")
        
    print(f"{indent}위치: x={layer.left}, y={layer.top}")
    print(f"{indent}크기: {layer.width} x {layer.height}")
    print(f"{indent}---")

# PSD 파일 열기
psd = PSDImage.open('example.psd')

# 최상위 레이어부터 분석 시작
for layer in psd:
    analyze_layer(layer)
