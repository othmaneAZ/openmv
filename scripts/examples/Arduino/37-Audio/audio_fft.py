import image, audio, time, array, math, ulab as np
from ulab import extras, numerical

SIZE = 512//4
pcm_buf = None
fb = image.Image(SIZE+50, SIZE, image.RGB565, copy_to_fb=True)
audio.init(channels=2, frequency=16000, gain=24, highpass=0.9883)

def audio_callback(buf):
    global pcm_buf
    if (pcm_buf == None):
        pcm_buf = np.array(array.array('h', buf))

# Start audio streaming
audio.start_streaming(audio_callback)

def draw_fft(img, fft_buf):
    fft_buf = (fft_buf / max(fft_buf)) * SIZE
    fft_buf = np.vector.log10(fft_buf + 1) * 20
    color = (0xFF, 0x0F, 0x00)
    for i in range(0, SIZE):
        img.draw_line(i, SIZE, i, SIZE-int(fft_buf[i]), color, 1)

def draw_audio_bar(img, level, offset):
    blk_size = SIZE//10
    color = (0xFF, 0x00, 0xF0)
    blk_space = (blk_size//4)
    for i in range(0, int(round(level/10))):
        fb.draw_rectangle(SIZE+offset, SIZE - ((i+1)*blk_size) + blk_space, 20, blk_size - blk_space, color, 1, True)

while (True):
    if (pcm_buf != None):
        fb.clear()
        fft_buf = extras.spectrogram(pcm_buf[0::2])
        l_lvl = int((numerical.mean(abs(pcm_buf[1::2])) / 32768)*100)
        r_lvl = int((numerical.mean(abs(pcm_buf[0::2])) / 32768)*100)
        pcm_buf = None
        draw_fft(fb, fft_buf)
        draw_audio_bar(fb, l_lvl, 0)
        draw_audio_bar(fb, r_lvl, 25)
        fb.flush()

# Stop streaming
audio.stop_streaming()
