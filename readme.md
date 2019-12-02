## tgs19  
tgs19の実験です。みんなで見られるように、このへんに置いときます。  
    
## Requirements  
pip install -r requirements.txt  
  
# running  
python3 tgs.py  
  
## Realsenseを使う  
realsense受信機/realsenseOSC.exeを立ち上げておく。  
buildSettings.py で、 CONTROLLER_MODE=1 に設定されていることを確認。
両方揃ってれば、勝手に通信して動く。  

## マウスを使う  
buildSettings.py で CONTROLLER_MODE=0 にする。  
あとは、普通に動かせばマウスになる。  
マウス移動でスプレーを移動、左クリックで発射。もしかすると、右クリックでスプレー位置をリセットできるかもしれない（デバッグ用に作ったやつなので、残してるか消したか忘れた）  