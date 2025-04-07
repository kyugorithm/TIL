# Python 예시 코드
def find_moov_atom(mp4_file):
    with open(mp4_file, 'rb') as f:
        pos = 0
        while True:
            # 아톰 크기 읽기
            size_data = f.read(4)
            if not size_data or len(size_data) < 4:
                break
                
            size = int.from_bytes(size_data, byteorder='big')
            
            # 아톰 타입 읽기
            atom_type = f.read(4)
            
            if atom_type == b'moov':
                return f"'moov' 아톰이 위치 {pos}에서 발견됨 (크기: {size} 바이트)"
                
            # 다음 아톰으로 이동
            if size > 8:
                f.seek(size - 8, 1)
            
            pos += size
    
    return "'moov' 아톰을 찾을 수 없음"
