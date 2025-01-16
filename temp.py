from psd_tools import PSDImage

def analyze_layer(layer, depth=0):
    indent = "  " * depth  # 계층 구조를 시각적으로 표현하기 위한 들여쓰기
    
    # 그룹 레이어인 경우
    if hasattr(layer, 'layers') and layer.layers:
        print(f"{indent}그룹 레이어: {layer.name}")
        # 그룹 내의 각 레이어를 재귀적으로 분석
        for child in layer.layers:
            analyze_layer(child, depth + 1)
    
    # 텍스트 레이어인 경우
    elif layer.kind == 'type':
        print(f"{indent}텍스트 레이어: {layer.name}")
        print(f"{indent}텍스트 내용: {layer.text}")
        print(f"{indent}폰트: {layer.font}")
    
    # 기타 일반 레이어
    else:
        print(f"{indent}일반 레이어: {layer.name}")
    
    print(f"{indent}크기: {layer.width} x {layer.height}")
    print(f"{indent}---")

# PSD 파일 열기
psd = PSDImage.open('example.psd')

# 최상위 레이어부터 분석 시작
for layer in psd:
    analyze_layer(layer)
