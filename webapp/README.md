# Türkçe Finansal PDF'ten Sentetik Veri Üretimi Web Uygulaması

## Uygulamanın Amacı
Bu uygulama, Türkçe finansal PDF dosyalarından sentetik soru-cevap (instruction) veri seti üretmek için geliştirilmiştir. Amaç, finansal okuryazarlık alanında eğitim ve yapay zeka uygulamaları için otomatik, kaliteli ve bağlama uygun veri üretmektir.

## Temel Özellikler
- PDF dosyasından metin çıkarımı ve parçalara ayırma
- LangChain ile vektör tabanlı doküman arama (retrieval)
- Ollama (ör: gemma3n:e4b) ile LLM tabanlı soru ve cevap üretimi
- Kullanıcıdan özel prompt (soru/cevap şablonu) alma imkanı
- Sonuçları ekranda görme ve JSON olarak indirme
- Streamlit tabanlı modern ve kolay arayüz

## Yapılan Başlıca İşler
- FastAPI ile PDF işleme ve LLM entegrasyonu
- Streamlit ile kullanıcı dostu frontend
- HuggingFace sentence-transformers ile embedding işlemleri
- Docker ile kolay dağıtım ve çalıştırma
- Backend hazır olmadan frontend'in başlamasını engelleyen script
- GPU desteği (Ollama ve embedding modelleri için uygun ortamda otomatik)
- Kullanıcıdan özel prompt ve soru adedi alma
- PDF işlenirken ilerleme çubuğu
- Gereksiz yorum ve açıklama satırlarının temizlenmesi

## Gereksinimler
- Docker (ve tercihen NVIDIA GPU ile CUDA sürücüleri)
- Host makinede Ollama kurulu ve model (ör: gemma3n:e4b) indirilmiş olmalı

## Docker ile Çalıştırma
1. **Hostta Ollama'yı başlat:**
   ```bash
   ollama serve
   # veya
   ollama run gemma3n:e4b
   ```
2. **Docker imajını build et:**
   ```bash
   docker build -t tr-pdftosyntheticdata-webapp:latest .
   ```
3. **Container'ı başlat:**
   ```bash
   docker run --gpus all -p 8501:8501 -p 8000:8000 tr-pdftosyntheticdata-webapp:latest
   ```
   > Eğer GPU'nuz yoksa `--gpus all` kısmını çıkarabilirsiniz.

4. **Uygulamaya eriş:**
   - [http://localhost:8501](http://localhost:8501) (Streamlit arayüzü)
   - [http://localhost:8000/docs](http://localhost:8000/docs) (FastAPI dokümantasyon)

## Kullanım
- PDF dosyanızı yükleyin.
- Kaç ve nasıl soru üretileceğini yazın (ör: "bana 50 tane mantıklı soru üret").
- İsterseniz özel promptlarınızı girin veya varsayılanları kullanın. (varsayılan prompt finansal veri üretmek icin oluşturulmuştur)
- Sonuçları ekranda görebilir ve JSON olarak indirebilirsiniz.

## Notlar
- Ollama ve embedding işlemleri için GPU desteği varsa otomatik kullanılır.
- Dockerfile ve scriptler backend hazır olmadan frontend'i başlatmaz.
- Uygulama, finansal okuryazarlık alanında eğitim ve veri üretimi için optimize edilmiştir. 