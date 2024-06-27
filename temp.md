wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id={FILEID}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id={FILEID}" -O {FILENAME} && rm -rf ~/cookies.txt

만약 링크가 아래와 같다고 한다면, 
https://drive.google.com/file/d/1xoM26eXQz-0qcXf1XpudL2se8GkQ9PJd/view?usp=sharing
{FILEID}를 1xoM26eXQz-0qcXf1XpudL2se8GkQ9PJd 로 바꾸고,
{FILENAME}을 g.png 로 바꾼다.
---------------------------------------------------------------------
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xoM26eXQz-0qcXf1XpudL2se8GkQ9PJd' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1xoM26eXQz-0qcXf1XpudL2se8GkQ9PJd" -O g.png && rm -rf ~/cookies.txt

출처: https://sofar-sogood.tistory.com/entry/wget-wget으로-구글-드라이브-다운 [작심삼일:티스토리]


https://drive.google.com/file/d/11AeDJXZrClcfV5bD6PcEfrRbv7sTJYOq/view?usp=drive_link
https://drive.google.com/file/d/1MKlTIVvJGWgbAKQVhGaEwHSOPgHHhiKh/view?usp=drive_link
