# Bash-For-Windows.V2 (GUİ)

Bash for Windows, kullanıcıların komut satırı benzeri bir etkileşimli terminal deneyimi yaşamalarını sağlayan basit bir GUI uygulamasıdır.

**Not:** CMD'de veya başka bir terminalde bu projeyi çalıştırmak isteyenler **bash.py** dosyasını çalıştırabilirler.


![image](https://github.com/ugurcomptech/Bash-For-Windows/assets/133202238/c65c6c61-48ae-48b2-a896-a3eb1c04b344)


## Gereksinimler

Bu betiği çalıştırmak için aşağıdaki gereksinimlere ihtiyacınız vardır:

- Python 3.x
- tkinter (genellikle Python ile birlikte gelir)
- colorama kütüphanesi
- prompt_toolkit kütüphanesi

Gereksinimleri yüklemek için terminale aşağıdaki komutları kullanabilirsiniz:

```python
pip install -r requirements.txt
```

# Kullanım

- Bu repo'yu bilgisayarınıza klonlayın veya ZIP dosyasını indirin.

- Terminal veya komut istemcisini açın ve betiğin bulunduğu klasöre gidin.
    ```python
    cd C:\users\username\downloads\Bash-For-Windows-V2-GUI
    ```

- Betiği çalıştırmak için aşağıdaki komutu kullanın:
  ```python
  python gui_bash.py
  ```
- Kabuk betiği başlatıldığında, aşağıdaki komutları kullanabilirsiniz:

    - **cd <directory>:** Mevcut dizini değiştirin.
    - **ls:** Mevcut dizindeki dosyaları listele.
    - **exit:** Kabuk betimden çıkın.
    - **move <source> <destination>:** Dosya veya dizini taşıyın.
    - **copy <source> <destination>:** Dosya veya dizini kopyalayın.
    - **delete <file>:** Bir dosyayı silin.
    - **create <file>:** Yeni bir dosya oluşturun.
    - **search <keyword>:** Bir anahtar kelime içeren dosyaları arayın.
    - **edit:** Dosyaların içeriğini düzenler.
    - **up:** Üst dizine gidin.
    - **back:** Alt dizine gidin.
    - **show <directory>:** Bir dizinin içeriğini gösterin.
    - **help:** Yardım mesajını gösterin.



## Lisans

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Bu projeyi [MIT Lisansı](https://opensource.org/licenses/MIT) altında lisansladık. Lisansın tam açıklamasını burada bulabilirsiniz.
