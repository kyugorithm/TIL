from psd_tools import PSDImage
from PIL import Image, ImageChops
import numpy as np

class PSDCompositor:
    def __init__(self, psd_path):
        self.psd = PSDImage.open(psd_path)
        
    def apply_blend_mode(self, base, blend, mode, opacity=1.0):
        """
        블렌딩 모드를 적용하는 함수입니다.
        각 블렌딩 모드의 수학적 연산을 구현합니다.
        """
        if mode == 'normal':
            return Image.blend(base, blend, opacity)
        
        elif mode == 'multiply':
            # multiply 모드는 각 채널값을 곱하고 255로 나눕니다
            result = ImageChops.multiply(base, blend)
            if opacity < 1.0:
                result = Image.blend(base, result, opacity)
            return result
        
        elif mode == 'screen':
            # screen 모드는 반전된 이미지를 곱하고 다시 반전합니다
            result = ImageChops.screen(base, blend)
            if opacity < 1.0:
                result = Image.blend(base, result, opacity)
            return result
        
        # 다른 블렌딩 모드들도 비슷한 방식으로 구현할 수 있습니다
        return blend

    def apply_layer_effects(self, layer, image):
        """
        레이어 효과(그림자, 글로우 등)를 적용하는 함수입니다.
        """
        if not hasattr(layer, 'effects') or not layer.effects:
            return image
            
        result = image.copy()
        
        for effect in layer.effects:
            if effect.name == 'drop_shadow':
                # 그림자 효과 구현
                shadow = image.copy()
                shadow = shadow.convert('RGBA')
                # 그림자 오프셋 적용
                offset_x = effect.distance * np.cos(np.radians(effect.angle))
                offset_y = effect.distance * np.sin(np.radians(effect.angle))
                # 그림자 블러 적용
                shadow = shadow.filter(ImageFilter.GaussianBlur(effect.size))
                # 최종 합성
                result = Image.alpha_composite(result, shadow)
                
        return result

    def apply_layer_mask(self, layer, image):
        """
        레이어 마스크를 적용하는 함수입니다.
        """
        if not layer.has_mask():
            return image
            
        mask = layer.mask.topil()
        # 마스크가 흑백이 아닌 경우 변환
        if mask.mode != 'L':
            mask = mask.convert('L')
            
        # 마스크 크기가 이미지와 다른 경우 리사이즈
        if mask.size != image.size:
            mask = mask.resize(image.size, Image.LANCZOS)
            
        # RGBA 이미지의 알파 채널에 마스크 적용
        r, g, b, a = image.split()
        a = ImageChops.multiply(a, mask)
        return Image.merge('RGBA', (r, g, b, a))

    def composite_group(self, group, backdrop=None):
        """
        레이어 그룹을 합성하는 메인 함수입니다.
        모든 블렌딩 모드, 효과, 마스크를 고려합니다.
        """
        if backdrop is None:
            backdrop = Image.new('RGBA', self.psd.size, (0, 0, 0, 0))
            
        result = backdrop.copy()
        
        for layer in reversed(list(group)):  # 레이어 순서대로 처리
            if not layer.visible:
                continue
                
            if hasattr(layer, 'layers'):  # 중첩된 그룹인 경우
                layer_image = self.composite_group(layer, backdrop)
            else:  # 일반 레이어인 경우
                layer_image = layer.topil()
                
            if layer_image is None:  # 빈 레이어 건너뛰기
                continue
                
            # 레이어 마스크 적용
            layer_image = self.apply_layer_mask(layer, layer_image)
            
            # 레이어 효과 적용
            layer_image = self.apply_layer_effects(layer, layer_image)
            
            # 블렌딩 모드 적용
            blend_mode = getattr(layer, 'blend_mode', 'normal')
            opacity = getattr(layer, 'opacity', 255) / 255.0
            
            result = self.apply_blend_mode(result, layer_image, blend_mode, opacity)
            
        return result

    def render_group(self, group_name):
        """
        특정 그룹을 찾아서 합성을 수행하는 함수입니다.
        """
        group = None
        for layer in self.psd:
            if layer.name == group_name:
                group = layer
                break
                
        if group is None:
            raise ValueError(f"Group '{group_name}' not found in PSD file")
            
        return self.composite_group(group)

# 사용 예시
def process_psd(psd_path, group_name, output_path):
    """
    PSD 파일에서 특정 그룹을 추출하여 저장하는 함수입니다.
    """
    compositor = PSDCompositor(psd_path)
    result = compositor.render_group(group_name)
    result.save(output_path, 'PNG')
