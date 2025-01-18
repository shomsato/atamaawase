# atamaawase
CDのオリジナル音源とoff vocal音源の再生位置を合わせるためのプログラムです。ほぼChatGPTで作りました。
![example](https://github.com/user-attachments/assets/fa97b8cd-35dc-4c8a-9ee9-e421235109a9)
オリジナルとoff vocal(画像上2つ)を入力すると、画像下2つで示したように名前変えただけのオリジナルと、オリジナルの再生位置に合わせたoff vocalが出力されます。入力はflac, mp3, wav, ogg, aacに対応、出力は僕がflacが好きだからという理由でflac一択です。

# ダウンロード
pydubという音声処理のライブラリを動作させるのにFFmpegが必要なため、実行するには予めインストールしてください。 https://ffmpeg.org/

## ソースコード
https://github.com/shomsato/atamaawase/blob/main/atamaawase.py
## 実行ファイル版
https://github.com/shomsato/atamaawase/releases/download/v1.0.0/atamaawase.exe
