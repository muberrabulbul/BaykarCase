# BaykarCase
Bu proje Baykar tarafından verilen bir Vaka çalışması için geliştirilmiştir. Amacı, Django web çerçevesini kullanarak bir IHA kiralama platformu oluşturmaktır. **Proje için hazırladığım dökümantasyon `docs` klasörü altında yer almaktadır.**

## Teknolojiler
* Python 3.9
* Django 4.11
* Django Rest Framework
* PostgreSQL
* Docker

## Kurulum

### Yerel Makineye Kurulum
Bu proje, Python 3.9 sürümünü gerektirir. Bağımlılıklar Docker aracılığıyla yönetilir.

Gereksinimleri Kurma
Projeyi çalıştırmak için gereksinimleri kurmak için aşağıdaki adımları izleyin:

` docker install `

Projenin image dosyasını edinmek için aşağıdaki komutu çalıştırın:

` docker pull muberrabulbul/baykar-case:baykarcase `


PostgreSQL ve Uygulamayı Yapılandırma
Projeyi çalıştırmak için PostgreSQL ve uygulamayı yapılandırmanız gerekir. Docker ve docker-compose kullanarak kolayca yapılandırabilirsiniz:

` docker compose up -d `

Sunucuyu Çalıştırma
Şimdi, sunucuyu başlatma zamanı geldi. İlk adımlarımızı atalım:

` docker compose up baykarcase `



Yerel makinenizde bu projeyi çalıştırmak için gereken adımları tamamladınız. 🚀 

Proje bir demo projesi olduğu için özel bir sunucu kiralanmadı. Bu sebeple varsayılan adres `http://0.0.0.0`'dır. Eğer projeyi Docker Compose ile ayağa kaldırıp test etmek istiyorsanız, proje ayağa kalktıktan sonra tarayıcınızda başlangıç noktası olarak şu adresi kullanabilirsiniz: 

`http://localhost:8000/register/`

Bu adresle uygulamaya erişebilirsiniz. 🚀
