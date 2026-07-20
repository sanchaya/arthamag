# ಅರ್ಥ - ಆರ್ಥಿಕತೆಯ ಕನ್ನಡ ಮಾಸಪತ್ರಿಕೆ

Digital archive of Artha (ಅರ್ಥ) — a Kannada magazine on economics published by Lokayatha.

**Website:** https://artha.sanchaya.net

## How to add a new issue

1. Upload the PDF to Internet Archive (archive.org)
2. Add a new entry to `issues.json` with the following fields:
   ```json
   {
     "identifier": "lokayatha.artha.<month>.<year>",
     "title": "ಅರ್ಥ <Kannada month> <year>",
     "author": "ಟಿ ಎಸ್ ವೆಂಕಟಗೋಪಾಲ್",
     "publisher": "ಲೋಕಾಯತ",
     "info": "Description in Kannada",
     "tags": "ಅರ್ಥ ಮಾಸಪತ್ರಿಕೆ, ಮಾಸಪತ್ರಿಕೆ, ಪತ್ರಿಕೆ, ಕನ್ನಡ ಸಾಹಿತ್ಯ, ಆರ್ಥಿಕತೆ",
     "level": <year>,
     "authorUrl": "https://archive.org/search?query=creator%3A%22T+S+Venugopal%22",
     "url": "https://archive.org/details/<identifier>",
     "cover": "https://archive.org/services/img/<identifier>"
   }
   ```
3. Commit and push to deploy

## Deploy

```sh
./push.sh
```

## License

Content is CC BY 4.0 unless otherwise noted. Code is MIT.
# arthamag
