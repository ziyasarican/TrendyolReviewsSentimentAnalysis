# TrendyolReviewsSentimentAnalysis

Trendyol ürün yorumlarının duygusal analizi projesi.

Data-set Adımları:
-Öncelikle Selenium kütüphanesi ile web-scraping işlemi yapılıp bir ürüne ait yorumlar comments.csv dosyasına yazılmıştır. Bu üründe 111 adet yorum vardır. Uygulanan modellerin başarısının kıyaslanması için az yorum sayısına ait bir ürün seçilmiştir. En yüksek başarıya sahip model daha sonra 1479 adet yoruma sahip başka bir ürüne uygulanmıştır.
-Ürüne verilen yıldız sayıları da web-scraping işlemi ile 'STARS' sütununa yazılmıştır.
-

Model Adımları:
- Türkçe halihazırda NLP adımlarının zor olduğu bir dildir. Üstüne kullanıcıların yorum yazarken günlük dilde yazıp çok fazla yazım yanlışı yapması NLP adımlarını hayli zorlaştırmaktadır. 
- Bu sebeple Türkçe yorumları İngilizce'ye çevirerek analize devam etme yoluna gidilmiştir.
- 2 farklı Translator kütüphanesi kullanılıp elde edilen İngilizce yorumlar 'Englsih Comments' ve 'English Comments 2' sütunları olarak csv dosyasına eklenmiştir.
- from deep_translator import GoogleTranslator kütüphanesi ile çevrilen yorumların daha başarılı olduğu hem manuel kontrol ile hem modeller uygulandıktan sonraki başarı oranının kontrolü ile tespit edilmiştir.
- Daha sonra İngilizce yorumlara 'Vader' ve 'Bert' modeller uygulanmıştır. Uygulanırken hazır modeller kullanılmıştır.
- Vader Model -1(negatif),1(pozitif) arasında değer döndürmektedir.
- - Model sonucunda dönen değerler 0'dan büyükse pozitif, 0'dan küçükse negatif, 0'a eşitse nötr etiketi atanmıştır.
- - Atanan etiketler ile ürüne verilen yıldız sayıları karşılaştırılmış ve 'Vader Model Status' sütununa yazılmıştır.
- ![Vader Result](https://user-images.githubusercontent.com/87414202/212744256-ca1ff373-e7dc-4183-9506-13041a030853.png)

- - 
- Bert Model ise 3 değer döndürüp bunlar negatif-nötr-pozitif kutpu ifade etmektedir.
- Basit bir ayrıştırma da olsa ürünlere verilen yıldızlar ile model sonuçları
![Roberta Result](https://user-images.githubusercontent.com/87414202/212740834-95676d7a-0d2f-4e18-a735-a8d87b4c9e1a.png)
