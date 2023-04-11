TalkLip

기존 방법론은 오디오와 입모양의 sync와 이미지 품질에 집중해왔으나 가독성은 중요하지 않았다.  
그러나 McGurk effect에 따르면 잘못된 음성과 시각 정보를 혼합하는 경우 관찰자는 잘못된 phoneme으로 이해할 수 있는 문제가 있기 때문에 해결이 필요한 문제이다.  
아래 방법론을 통해 문제를 해결해 나간다.  

1. Lip reading : enhance intelligibility of spoken words
2. Audio-Visual self-supervised training: compensate data scarcity
3. Contrastive learning: Enhance audio sync with video(while considering global temporal dependency of audio)

Audio encoder
: G에서 사용할 (입 모양과 입술의 움직임 정보)를 Phoneme 단위로 넘겨주는 역할
: local(cnn-based : 0.2s input) & global(transformer-based) 두가지 encoder가 존재
