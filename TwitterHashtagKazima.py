# Gerekli Kütüphanelerin import edilmesi #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Klavye komutlarını verebilmek için.
from selenium.webdriver.support.ui import WebDriverWait #time.sleep yerine, belirli bir elemanın görünür hale gelmesiyle işlem yapmasını sağlamak için.
from selenium.webdriver.support import expected_conditions as EC #time.sleep yerine, belirli bir elemanın görünür hale gelmesiyle işlem yapmasını sağlamak için.
import time
import random
from instabilgi import KullaniciAdi, Sifre, GuvenlikKodu # Localimde instabilgi.py oluşturdum ve burdan çektim.
# Basic Xpath: //TAG[@ATTRIBUTE="VALUE"]
def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Çeşitli hatalar sonucunda, yapılması gereken options ayarları #
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_experimental_option("detach", True)
prefs = {"profile.default_content_setting_values.notifications" : 2} # Site Bildirimini kapatma. Chrome üzerinden.
chrome_options.add_experimental_option("prefs",prefs) # Site Bildirimini kapatma. Chrome üzerinden.

# Selenium Bağlantısı #
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://x.com/"
driver.get(url)
driver.maximize_window()

wait = WebDriverWait(driver, 4) # Otomatik Bekleme Süreleri İçin. 10 burada maksimum bekleme süresini ifade eder. Eğer 10 saniye ve üstü sürerse TimeoutException hatası döner.

GirisYap = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a/div'))) # GirisYap'daki element gözüktüğü zaman işlem yapacak. Manuel time.sleep belirlemeyeceğim. Otomatik çalışacak.
GirisYap.click()
# random_sleep(1, 3) # random 1 veya 3 saniye sleep atacak. Wait.Until ile çok hızlı oldu.

time.sleep(2)

Giris = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')))
Giris.send_keys(KullaniciAdi)
Giris.send_keys(Keys.ENTER)

time.sleep(2)

try:
    # İlk olarak Şifre alanını kontrol et
    Sif = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
    Sif.send_keys(Sifre)
    Sif.send_keys(Keys.ENTER)
except:
    try:
        # Eğer Şifre alanı bulunamazsa, Telefon alanını kontrol et
        Telefon = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')))
        Telefon.send_keys(GuvenlikKodu)
        Telefon.send_keys(Keys.ENTER)
        time.sleep(1)

        # Telefon numarası ile işlem yaptıktan sonra Şifre alanını bekle ve işlem yap
        Sif = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
        Sif.send_keys(Sifre)
        Sif.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Elementler bulunamadı: {e}")

time.sleep(2)

Aranan = "Cinsel Eşitlik Bakanlığı"
Arama = f"https://x.com/search?q={Aranan}&src=typed_query"
driver.get(Arama)

time.sleep(3)

Bilgi = []

# wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu"))) yaptım ancak belirttiğim süre az kalıyor. Sanırım tüm elementsleri beklediği için ve scroll yapmadığımda da tüm elementler gelemediği için alamıyor.
Profil = driver.find_elements(By.XPATH, './/div[@class="css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]')# Class ismini koydum. Elements çünkü birden çok var. Elements de for döngüsü genellikle.
for i in Profil:
    Bilgi.append(i.text)

#Hashtag yapısında, sürekli binlerce tweet geldiği için, kaç tane bilgi istiyorsam ona göre döngü yapacağım. Sınırım o olmalı.
TweetSayisi = 3

#Scrollbar ile hareket ederken ki yeni gelen verilerin çekilmesi.
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") #scrollbar her hareket ettiğinde, tekrar profil2den xpath al.
    time.sleep(3)
    Profil2 = driver.find_elements(By.XPATH, './/div[@class="css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]')
    for j in Profil2:
        x = j.text
        if x not in Bilgi:
            Bilgi.append(x)
    if len(Bilgi) >= TweetSayisi: # Divler 50'yi görmeden 50 üstünede çıkabilir. Ondan >= yapmak durumundayız.
        break
    wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class="css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]')))
    # Tüm Bilgileri, Bilgi'ye atadık.
# Her \n bir liste indeksi olacak gibi düşünebiliriz.
print(Bilgi)

# Her tweet, Bilgi içerisinde indeksle saklanıyor. İndekslerin içerisine girerek parçalama yapmam lazım.
sayac = 0

# Tweet bilgilerini ayrıştır ve yazdır
for k in range(0, TweetSayisi):
    try:
        lines = Bilgi[k].split("\n")
        Account = lines[1]  # Kullanıcı Hesabı
        When = lines[3]  # Ne zaman tweet atıldı
        Tweet = lines[4]  # Tweet
        if lines[5] == " adlı kişiye yanıt olarak":
            Tweet = lines[6]

        # Görüntülenme
        try:
            Visualization = lines[-1].split(" ")
            if len(Visualization) > 1:
                if Visualization[1] == "B":
                    Visualization = int(Visualization[0] + "000")
                elif Visualization[1] == "Mn":
                    Visualization = int(Visualization[0] + "000000")
                else:
                    Visualization = int(Visualization[0])
            else:
                Visualization = int(Visualization[0])
        except IndexError as e:
            print(f"IndexError: {e}")
            Visualization = 0
        except ValueError as e:
            print(f"ValueError: {e}")
            Visualization = 0

        # Beğeni
        try:
            Like = lines[-2].split(" ")
            if len(Like) > 1:
                if Like[1] == "B":
                    Like = int(Like[0] + "000")
                elif Like[1] == "Mn":
                    Like = int(Like[0] + "000000")
                else:
                    Like = int(Like[0])
            else:
                Like = int(Like[0])
        except IndexError as e:
            print(f"IndexError: {e}")
            Like = 0
        except ValueError as e:
            print(f"ValueError: {e}")
            Like = 0

        # Retweet
        try:
            Retweet = lines[-3].split(" ")
            if len(Retweet) > 1:
                if Retweet[1] == "B":
                    Retweet = int(Retweet[0] + "000")
                elif Retweet[1] == "Mn":
                    Retweet = int(Retweet[0] + "000000")
                else:
                    Retweet = int(Retweet[0])
            else:
                Retweet = int(Retweet[0])
        except IndexError as e:
            print(f"IndexError: {e}")
            Retweet = 0
        except ValueError as e:
            print(f"ValueError: {e}")
            Retweet = 0

        # Yorum
        try:
            Comment = lines[-4].split(" ")
            if len(Comment) > 1:
                if Comment[1] == "B":
                    Comment = int(Comment[0] + "000")
                elif Comment[1] == "Mn":
                    Comment = int(Comment[0] + "000000")
                else:
                    Comment = int(Comment[0])
            else:
                Comment = int(Comment[0])
        except IndexError as e:
            print(f"IndexError: {e}")
            Comment = 0
        except ValueError as e:
            print(f"ValueError: {e}")
            Comment = 0

        sayac += 1
        print(f"{sayac} - {Account} - {When} / Görüntülenme: {Visualization} / Beğeni: {Like} / Retweet Sayısı: {Retweet} / Yorum Sayısı: {Comment} - Tweet: {Tweet}")
    except IndexError:
        # Eğer beklenen yapı bulunamazsa, hatayı görmezden gel
        pass


# IndexError: list index out of range 107. satır için. Try bloğuna al. Metin Dosyasında hata detayı var.

# Tweet Atanlar Kaç Defa Tweet Attı.
# Hashtag, Belirli Bir Hesabın Tweetleri Bu Çalışmaları Yapılacak.