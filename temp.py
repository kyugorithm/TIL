def rgba_to_rgb(img):
    """
    4채널 RGBA 이미지를 3채널 RGB 이미지로 변환하면서 투명도를 유지합니다.
    CMYK 이미지도 처리할 수 있도록 수정됨
    """
    if img.shape[2] == 4:  # RGBA
        alpha = img[:, :, 3] / 255.0
        img_rgb = img[:, :, :3] * alpha[:, :, None]
        return img_rgb.astype(np.uint8)
    elif hasattr(img, 'mode') and img.mode == 'CMYK':  # CMYK 체크
        # CMYK를 RGB로 변환
        from PIL import Image
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img)
        # CMYK에서 RGB로 변환
        img_rgb = img.convert('RGB')
        return np.array(img_rgb)
    return img

class PSDProcessor:
    def __init__(self):
        self.ocr_en = PaddleOCR(use_angle_cls=False, use_gpu=True, show_log=False, lang="en")
        self.ocr_ko = PaddleOCR(use_angle_cls=False, use_gpu=True, show_log=False, lang="korean")

    def composite_without_text(self, psd_path):
        psd = PSDImage.open(psd_path)
        working_psd = deepcopy(psd)

        def remove_text_layers(layers):
            for i in range(len(layers) - 1, -1, -1):
                layer = layers[i]
                if hasattr(layer, 'layers'):
                    remove_text_layers(layer.layers)
                elif layer.kind == 'type':
                    layer_image = layer.composite()
                    img_np = np.array(layer_image)
                    
                    # CMYK 이미지 처리
                    if hasattr(layer_image, 'mode') and layer_image.mode == 'CMYK':
                        img_np = np.array(layer_image.convert('RGB'))
                    
                    img_np_rgb = rgba_to_rgb(img_np)
                    ratio = 100 * np.sum(img_np_rgb) / (math.prod(img_np_rgb.shape))
                    
                    rst = []
                    rst1 = self.ocr_en.ocr(img_np_rgb, cls=False)[0]
                    rst2 = self.ocr_ko.ocr(img_np_rgb, cls=False)[0]
                    if rst1:
                        rst.extend(rst1)
                    if rst2:
                        rst.extend(rst2)
                    
                    if len(rst) > 0 and ratio > 50:
                        del layers[i]

        remove_text_layers(working_psd.layers)
        
        # CMYK 이미지인 경우 RGB로 변환하여 저장
        result = working_psd.composite()
        if hasattr(result, 'mode') and result.mode == 'CMYK':
            result = result.convert('RGB')
        
        return result

    def process_psd_without_text(self, input_path, output_path):
        try:
            result = self.composite_without_text(input_path)
            # CMYK 처리를 고려한 저장
            if hasattr(result, 'mode') and result.mode == 'CMYK':
                result = result.convert('RGB')
            result.save(output_path)
            print(f"Successfully saved to {output_path}")
        except Exception as e:
            print(f"Error processing PSD: {str(e)}")
