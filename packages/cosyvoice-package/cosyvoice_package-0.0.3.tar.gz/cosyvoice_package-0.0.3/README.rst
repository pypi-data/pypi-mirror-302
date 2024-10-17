!!!!! Warning: Provided unofficially and for author use only !!!!!   

before pip install:
conda install -y -c conda-forge pynini==2.1.5

after pip install:
conda install pytorch torchvision torchaudio pillow==9.0.0 pytorch-cuda=12.4 -c pytorch -c nvidia
conda install pytorch==2.0.1 torchvision==0.15.2 pillow==9.0.0 torchaudio==2.0.2 pytorch-cuda=11.7 -c pytorch -c nvidia

mkdir pretrained_models
git clone https://www.modelscope.cn/iic/CosyVoice-300M.git pretrained_models/CosyVoice-300M
git clone https://www.modelscope.cn/iic/CosyVoice-300M-SFT.git pretrained_models/CosyVoice-300M-SFT