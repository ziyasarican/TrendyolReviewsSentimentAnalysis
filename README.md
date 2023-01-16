# TrendyolReviewsSentimentAnalysis

Trendyol ürün yorumlarının duygusal analizi projesi.

Dataset Adımları:
- Öncelikle Selenium kütüphanesi ile web-scraping işlemi yapılıp bir ürüne ait yorumlar comments.csv dosyasına yazılmıştır. Bu üründe 111 adet yorum vardır. Uygulanan modellerin başarısının kıyaslanması için az yorum sayısına ait bir ürün seçilmiştir. En yüksek başarıya sahip model daha sonra 1479 adet yoruma sahip başka bir ürüne uygulanmıştır.
- Web-scraping, translate ve modelin çalışması hayli zaman aldığı için bir önceki dataset küçük seçilip en başarılı sonuç daha büyük bir dataset ile denenmiştir.
- Ürüne verilen yıldız sayıları da web-scraping işlemi ile 'STARS' sütununa yazılmıştır.
- Denemeler sırasında büyük-küçük harf durumunun model başarısını etkilediği görülüp bütün yorumlar küçük harfe çevrilmiştir.

Test Model Adımları(temp.py):
- Türkçe halihazırda NLP adımlarının zor olduğu bir dildir. Üstüne kullanıcıların yorum yazarken günlük dilde yazıp çok fazla yazım yanlışı yapması NLP adımlarını hayli zorlaştırmaktadır. 
- Bu sebeple Türkçe yorumları İngilizce'ye çevirerek analize devam etme yoluna gidilmiştir.
- 2 farklı Translator kütüphanesi kullanılıp elde edilen İngilizce yorumlar 'Englsih Comments' ve 'English Comments 2' sütunları olarak csv dosyasına eklenmiştir.
- from deep_translator import GoogleTranslator kütüphanesi ile çevrilen yorumların daha başarılı olduğu hem manuel kontrol ile hem modeller uygulandıktan sonraki başarı oranının kontrolü ile tespit edilmiştir.
- Daha sonra İngilizce yorumlara 'Vader' ve 'Bert' modeller uygulanmıştır. Uygulanırken hazır modeller kullanılmıştır.
- Vader Model -1(negatif),1(pozitif) arasında değer döndürmektedir.
- - Model sonucunda dönen değerler 0'dan büyükse pozitif, 0'dan küçükse negatif, 0'a eşitse nötr etiketi atanmıştır.
- - Atanan etiketler ile ürüne verilen yıldız sayıları karşılaştırılmış ve 'Vader Model Status' sütununa yazılmıştır.
- - from googletrans import Translator kütüphanesi ile çevrilmiş yorumların sonuçları: 

![Vader Result](https://user-images.githubusercontent.com/87414202/212744256-ca1ff373-e7dc-4183-9506-13041a030853.png)
- - from deep_translator import GoogleTranslator kütüphanesi ile çevrilmiş yorumların sonuçları:

![Vader Result 2](https://user-images.githubusercontent.com/87414202/212744347-74607607-1202-4071-a7c7-c0885f7a1fda.png)

- Bert Model ise 3 değer döndürüp bunlar negatif-nötr-pozitif kutpu ifade etmektedir. Bu kutuplar 'Polarity' sütununa eklenmiştir.
- Pozitif-nötr-negatif kutup değerlerinden hangisi en büyükse ona kendi ismi etiket olarak atanıp yeni sütuna eklenmiştir.
- Daha sonra bu etiketler ile ürüne verilen yıldız sayıları karşılaştırılıp 'Roberta Model Status' sütunun olarak eklemiştir.
- - from googletrans import Translator kütüphanesi ile çevrilmiş yorumların sonuçları: 

![Roberta Result](https://user-images.githubusercontent.com/87414202/212745483-5ab3afce-2ed0-4b3a-9ae0-a0d0cf8c0093.png)
- - from deep_translator import GoogleTranslator Translator kütüphanesi ile çevrilmiş yorumların sonuçları: 

![Roberta Result 2 ](https://user-images.githubusercontent.com/87414202/212745631-7e7b3806-d529-4297-a3a4-279216d227ab.png)

Test Model Sonuçları:
- from deep_translator import GoogleTranslator kütüphanesi ile daha başarılı çeviriler yapılmıştır ve modelin doğruluk oranı artmıştır.
- Bert Model'in başarısı Vader Model'e göre daha fazladır. 

Uygulama Model Adımları(sentimentAnalysisWithRoberta.py):
- 1479 yoruma sahip ürün web-scraping işlemi ile çekilip comments2.csv dosyasına yazılıp bir test modeldeki from deep_translator import GoogleTranslator kütüphanesi ile yorumlar İngilizce'ye çevrilmiştir.
- Daha sonra Bert Model kullanılmış ve kutup polarity'leri yeni sütuna yazılmıştır.
- Bir önceki datasetteki karşılaştırma geliştirilmiştir ve Bert Model'de dönen negatif-nötr-pozitif değerleri farklı şekilde karşılaştırılmıştır.
- - Eğer dönen değerlerden bir tanesi 0.8 yani %80 ve üzeriyse kendi ismi etiketlenmiştir. Örneğin [0.8835449  0.09714787 0.01930723] durumunda veriye 'Negative' etiketi verilmiştir. Bunun sebebi %80'den fazla olasılıkla o kutpa yakın olmasıdır.
- - Eğer dönen değerler 0.2'den küçükse yani %20 ve altında olasılıkla o değer değilse 'non' etiketi kullanılmıştır. Örneğin [0.47839725 0.4838082  0.03779453] durumunda veriye 'Non Positive' etiketi atanmıştır.
- - Bu optimizasyonlar ile modelin başarısı artmıştır.
- Daha sonra bu etiketler ile ürüne verilen yıldız sayıları karşılaştırılmıştır.

![Bert Result](https://user-images.githubusercontent.com/87414202/212747589-50dc06c7-14f5-40ff-9b50-bd0c261071e4.png)


