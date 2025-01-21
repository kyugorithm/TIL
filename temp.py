from psd_tools import PSDImage
from copy import deepcopy

def composite_without_text(psd_path):
    # 원본 PSD 파일을 열기
    psd = PSDImage.open(psd_path)
    
    # PSD 파일의 복사본을 만들어서 작업
    # 이렇게 하면 원본 파일은 변경되지 않습니다
    working_psd = deepcopy(psd)
    
    def remove_text_layers(layers):
        """
        재귀적으로 모든 레이어를 순회하면서 텍스트 레이어를 찾아 제거합니다.
        그룹 레이어 내부의 텍스트도 처리할 수 있습니다.
        """
        # 리스트를 뒤에서부터 순회합니다
        # 레이어를 삭제할 때 인덱스가 변경되는 것을 방지하기 위함입니다
        for i in range(len(layers) - 1, -1, -1):
            layer = layers[i]
            
            # 그룹 레이어인 경우 재귀적으로 처리
            if hasattr(layer, 'layers'):
                remove_text_layers(layer.layers)
                
                # 그룹 내의 모든 레이어가 제거된 경우 그룹도 제거
                if len(layer.layers) == 0:
                    del layers[i]
            
            # 텍스트 레이어인 경우 제거
            elif layer.kind == 'type':
                del layers[i]
    
    # 텍스트 레이어 제거 실행
    remove_text_layers(working_psd.layers)
    
    # 수정된 PSD 파일 합성
    # 이때 원본 PSD의 블렌딩 모드와 투명도가 유지됩니다
    result = working_psd.composite()
    
    return result

# 사용 예시
def process_psd_without_text(input_path, output_path):
    """
    PSD 파일에서 텍스트를 제외한 모든 레이어를 합성하여 저장합니다.
    
    Args:
        input_path (str): 입력 PSD 파일 경로
        output_path (str): 출력 이미지 파일 경로 (보통 PNG로 저장)
    """
    try:
        result = composite_without_text(input_path)
        result.save(output_path)
        print(f"Successfully saved to {output_path}")
    except Exception as e:
        print(f"Error processing PSD: {str(e)}")

# 실제 사용
# process_psd_without_text('your_file.psd', 'output.png')
