import os
import shutil
from tkinter import Tk
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass
from tkinter.filedialog import askopenfilename
from pydub import AudioSegment
import numpy as np
from scipy.signal import correlate
import time

# ファイル選択ダイアログの作成
def select_file(title):
    Tk().withdraw()  # Tkinterウィンドウを非表示にする
    filename = askopenfilename(title=title, filetypes=[("Audio files", "*.flac;*.mp3;*.wav;*.ogg;*.aac")])
    return filename

def align_audio_with_phase_cancellation_optimized():
    # オリジナルとオフボーカルファイルを選択
    print("オリジナル音源ファイルを選択してください")
    original_file = select_file("オリジナル音源ファイルの選択")
    if not original_file:
        print("オリジナル音源ファイルが選択されませんでした。処理を終了します。")
        time.sleep(3)
        return

    print("オフボーカル音源ファイルを選択してください")
    off_vocal_file = select_file("オフボーカル音源ファイルの選択")
    if not off_vocal_file:
        print("オフボーカル音源ファイルが選択されませんでした。処理を終了します。")
        time.sleep(3)
        return

    # 出力先フォルダを同じ場所にoutputフォルダを作成
    output_dir = os.path.join(os.path.dirname(original_file), 'output')
    
    # ファイル読み込み処理、エラーチェック
    try:
        original = AudioSegment.from_file(original_file)
        off_vocal = AudioSegment.from_file(off_vocal_file)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("ファイルの読み込みに失敗しました。処理を終了します。")
        time.sleep(3)
        return

    # 出力フォルダ作成 (エラーなしで読み込んだ場合にのみ)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # サンプリングレートやチャネルの取得
    sample_rate = original.frame_rate
    channels = original.channels

    # ステレオ波形を分離
    original_np = np.array(original.get_array_of_samples()).reshape((-1, channels))
    off_vocal_np = np.array(off_vocal.get_array_of_samples()).reshape((-1, channels))
    
    # モノラル化（左右平均）
    original_mono = original_np.mean(axis=1)
    off_vocal_mono = off_vocal_np.mean(axis=1)
    
    # クロスコリレーションで初期ラグ計算
    correlation = correlate(original_mono, off_vocal_mono, mode="full")
    correlation_lag_index = np.argmax(correlation)  # ピーク位置
    correlation_lag = correlation_lag_index - len(off_vocal_mono) + 1
    
    print(f"クロスコリレーションで計算したラグ: {correlation_lag} samples")
    
    aligned_original = original

    # オフボーカルを調整
    if correlation_lag >= 0:
        adjusted_off_vocal_np = np.concatenate((
            np.zeros((correlation_lag, channels)),  # 無音挿入
            off_vocal_np[:len(off_vocal_np) - correlation_lag]
        ))
    else:
        adjusted_off_vocal_np = np.concatenate((
            off_vocal_np[-correlation_lag:],  # 無音で末尾を埋める
            np.zeros((-correlation_lag, channels))
        ))
    
    # 整数型に戻して出力
    adjusted_off_vocal = AudioSegment(
        adjusted_off_vocal_np.flatten().astype(np.int16).tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=channels
    )

    # ファイル名の設定（元のファイル名にoutputフォルダを指定）
    original_filename = os.path.basename(original_file)
    off_vocal_filename = os.path.basename(off_vocal_file)
    
    # 出力ファイルパスを設定
    output_original_file = os.path.join(output_dir, f"aligned_{original_filename}")
    output_off_vocal_file = os.path.join(output_dir, f"aligned_{off_vocal_filename}")
    
    # ステレオでファイル書き出し
    aligned_original.export(output_original_file, format="flac")
    adjusted_off_vocal.export(output_off_vocal_file, format="flac")

    print(f"次のファイルを保存しました {output_original_file}, {output_off_vocal_file}")
    time.sleep(3)

align_audio_with_phase_cancellation_optimized()