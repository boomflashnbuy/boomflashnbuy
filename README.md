# BoomFlashnBuy · kit video (ramo video-kit, NON pubblicato da Netlify)
Pipeline usata per i video promo approvati il 31/10/2026.
- rv/stage5.html: scene animate (testi TX in 6 lingue), rv/end.html: schede finali Siri/Android
- rv/render5.py / still5.py: render dei fotogrammi con Playwright; rv/shots_ap.py: screenshot dell'app
- build_vo4.py: mix voce+musica (MUS=0.72 THR=0.04 RAT=4 REL=600 INTRO=2.0), loudnorm -14 LUFS; args: lang fmt out voicedir
- rv/base_eq.wav: base musicale approvata
- kok/gen2.py: voci Kokoro (EN am_michael, ES em_alex, PT pm_alex, FR ff_siwis; brand in IPA "bˈuːm flˈæʃ ænd bˈaɪ").
  Modello: kokoro-v1.0.onnx + voices-v1.0.bin (scaricare da github.com/thewh1teagle/kokoro-onnx releases).
- IT: voce Alfeo (TTSMaker, id 149001, speed 1.05) – serve Stefano per i captcha. DE: voce Mac "Anna (Premium)".
Regole: pronuncia "Boom Flash and Buy"; musica sotto la voce, 2 s di intro; niente prezzi Amazon inventati.
