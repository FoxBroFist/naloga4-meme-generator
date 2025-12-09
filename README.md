# Meme Generator

Preprosta Flask aplikacija za generiranje memov.  
Uporabnik naloži sliko, vnese zgornji in spodnji tekst, aplikacija pa vrne nov meme.

## Uporabljene tehnologije

- Jezik: Python
- Okvir: Flask
- Knjižnica za slike: Pillow
- Kontejnerizacija: Docker

## Kako zagnati aplikacijo z Dockerjem

### 1. Build Docker image

```bash
docker build -t meme-generator .