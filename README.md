# いじぇぴっぴGPSロガー

## なにこれ

PimoroniのGPSモジュールを使用してGPSロガーを雑に作るプロジェクト

## 必要なモジュール

* [PA1010D GPS Breakout](https://shop.pimoroni.com/products/pa1010d-gps-breakout)
* [0.96" SPI Colour LCD (160x80) Breakout](https://shop.pimoroni.com/products/0-96-spi-colour-lcd-160x80-breakout)
* [Breakout Garden Mini (I2C + SPI)](https://shop.pimoroni.com/products/breakout-garden-mini-i2c-spi)

PA1010D GPS Breakout以外はなくてもいいですが、なくてもいいような考慮はまだコードに含まれていません。

## インストール

なんか抜けてるかも

```
pi@raspberrypi:~ $ sudo apt update ; sudo apt install python3-pip python3-pil python3-spidev python3-smbus2 fonts-dejavu-core
pi@raspberrypi:~ $ sudo pip3 install ST7735 pa1010d
pi@raspberrypi:~ $ git clone https://gitlab.com/Akkiesoft/ejegpslogger
pi@raspberrypi:~ $ sudo cp ejegpslogger/ejegpslogger.service /etc/systemd/system/
pi@raspberrypi:~ $ sudo systemctl enable ejegpslogger.service
pi@raspberrypi:~ $ sudo systemctl start ejegpslogger.service
```

## 使い方

* http://raspberrypi.local (もしくはインストールしたマシンのホスト名)にアクセス
* 記録
    * Startボタンを押すと記録開始
    * Stopボタンを押すと記録終了
* マップ
    * 初期地点は青葉台駅です
    * GPSで現在位置が取得できるとその場所が表示されます
    * 10秒ごとに現在地点をピンで打ちます
    * いまのところリロードすると消えます
* MAPリンク
    * 現在位置のGoogle Mapsリンクです

## 記録データ

* CSVデータです
* /home/pi/ejegpsloggerに蓄積されます

## License

MIT Lisence
Copyright 2020 Akira Ouchi <akkiesoft@marokun.net>
