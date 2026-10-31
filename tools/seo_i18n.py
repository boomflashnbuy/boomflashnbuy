"""Guide per Google in EN/ES/FR/DE/PT + collegamenti hreflang con le guide italiane.
Uso: python3 tools/seo_i18n.py https://boomflashnbuy.netlify.app   (dopo tools/seo_build.py)"""
import sys, os, json, html, re, datetime
sys.argv = sys.argv[:2]
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import seo_build as S  # rigenera anche le pagine italiane e la sitemap

BASE, ROOT, TODAY = S.BASE, S.ROOT, S.TODAY
KEYS = ['shop', 'scan', 'bf']
IT_SLUG = {'shop': '/guide/negozio-o-amazon/', 'scan': '/guide/app-scanner-codice-a-barre/', 'bf': '/guide/black-friday-prezzi/'}
LOC = {'en': 'en_US', 'es': 'es_ES', 'fr': 'fr_FR', 'de': 'de_DE', 'pt': 'pt_PT'}

T = {
'en': dict(
  slug={'shop': '/en/store-or-amazon/', 'scan': '/en/barcode-scanner-app/', 'bf': '/en/black-friday-prices/'},
  idx=('/en/', 'BoomFlashnBuy guides: in-store price vs Amazon', 'Free guides: scan a barcode in the store and check the Amazon price in seconds.', 'Store price <em>vs Amazon</em>'),
  open_scan='📷 Open the scanner', open_app='Open the app', faq='FAQ', more='More guides', foot='BoomFlashnBuy is free and runs in your browser, no sign-up.', upd='Updated',
  legal='It costs you nothing: Amazon pays me. As an Amazon Associate I earn from qualifying purchases.',
  steps=['Open <a href="/?lang=en">BoomFlashnBuy</a> on your phone (or say <b>“Hey Siri, boom!”</b> on iPhone).', 'Point the camera at the <b>barcode</b>: at the beep the app recognises it.', 'If you like, type the <b>price you see in the store</b>.', 'Tap <b>“Found! Go to prices”</b>: Amazon opens with all the offers for that product.'],
  pages={
   'shop': ('Store or Amazon? How to find out which is cheaper in 5 seconds', 'In a store and wondering if Amazon is cheaper? Scan the barcode and compare the price in seconds, for free.', 'Store or Amazon: <em>which is cheaper?</em>',
     '<p class="lead">You are in front of the shelf, the price looks fine, but you wonder: what if it costs less online? Checking by hand means typing the right name and size and scrolling through results. With the barcode it takes a moment.</p>[[VIDEO]]<h2>Compare the price in 4 steps</h2>[[STEPS]]<div class="box"><b>The trick:</b> the barcode (EAN/UPC) identifies the exact product, size included. So you compare the same thing, not something similar.</div><h2>When the store wins</h2><ul><li>You need it <b>now</b> and don\'t want to wait for delivery.</li><li>The store has a <b>deal</b> or the same price as online.</li><li>You want to see it, try it or get advice.</li></ul><h2>When Amazon wins</h2><ul><li>The price is <b>lower</b> and you can wait for delivery.</li><li>You find <b>sizes</b> or multipacks that are better value.</li><li>You want to compare sellers and read reviews.</li></ul><p>BoomFlashnBuy also keeps count: type the store price and what you paid on Amazon, and see how much you have saved in total.</p>',
     [('Do I need to install anything?', 'No. BoomFlashnBuy runs in your phone browser. If you like, add it to your Home Screen like an app.'), ('Is it free?', 'Yes, free and with no sign-up. The app gets a small commission from Amazon on qualifying purchases, at no cost to you.'), ('What if the product has no barcode?', 'Use “Read the label”: the app reads brand and model from the text. Or type or say what you are looking for.')]),
   'scan': ('Free barcode scanner app to compare prices with Amazon', 'Free barcode scanner that runs in your browser: scan the code in the store and compare the price with Amazon. No sign-up.', 'Free <em>barcode scanner</em>',
     '<p class="lead">BoomFlashnBuy is a barcode scanner built for one thing: telling you in a flash whether the price in the store is a good one.</p>[[VIDEO]]<h2>What it does</h2><ul><li>Reads <b>EAN-13, EAN-8, UPC</b> and other common formats, even tilted or far away.</li><li>Recognises the product and prepares the Amazon search in the <b>right department</b>.</li><li>No barcode? After 5 seconds it offers to <b>read the label</b>.</li><li>Works in <b>6 languages</b> and uses your country\'s Amazon store.</li></ul><h2>How to use it</h2>[[STEPS]]<h2>Privacy</h2><p>The camera is used only to read the code, inside the app. Searches and spending stay on your phone: no account needed.</p>',
     [('Does it work on iPhone and Android?', 'Yes. On iPhone open it in Safari (and with “Hey Siri, boom!”), on Android in Chrome, where you can also install it with one tap.'), ('Why isn\'t the code being read?', 'Move closer, avoid reflections and turn on the torch with the 🔦 icon. If it still fails, use “Read the label”.')]),
   'bf': ('Black Friday 2026: is the in-store deal really cheaper than Amazon?', 'Black Friday 2026 is Friday 27 November. Before buying in store, scan the barcode and compare the price with Amazon in seconds.', 'Black Friday: <em>is it really a deal?</em>',
     '<p class="lead">Black Friday 2026 falls on <b>Friday 27 November</b>, and Cyber Monday on Monday 30 November. “Sale” signs are everywhere: the fastest way to know if a price is really good is to compare it with Amazon on the spot, product by product.</p>[[VIDEO]]<h2>In the store, in 4 steps</h2>[[STEPS]]<h2>3 quick tips</h2><ol><li><b>Compare the same product</b>: the barcode avoids mixing up similar models and sizes.</li><li><b>Look at the final price</b>, not the discount percentage.</li><li><b>Keep count</b>: type the store price and see how much you save overall.</li></ol>',
     [('When is Black Friday 2026?', 'Friday 27 November 2026. Cyber Monday is Monday 30 November 2026.'), ('Does the app show the Amazon price directly?', 'It opens Amazon with the search ready for that product, where you see all the offers and sellers.')]),
  }),
'es': dict(
  slug={'shop': '/es/tienda-o-amazon/', 'scan': '/es/app-escaner-codigo-de-barras/', 'bf': '/es/black-friday-precios/'},
  idx=('/es/', 'Guías BoomFlashnBuy: precio en tienda vs Amazon', 'Guías gratis: escanea el código de barras en la tienda y mira el precio en Amazon en segundos.', 'Precio en tienda <em>vs Amazon</em>'),
  open_scan='📷 Abrir el escáner', open_app='Abrir la app', faq='Preguntas frecuentes', more='Más guías', foot='BoomFlashnBuy es gratis y funciona desde el navegador, sin registro.', upd='Actualizado el',
  legal='A ti no te cuesta nada: me paga Amazon. Como Afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables.',
  steps=['Abre <a href="/?lang=es">BoomFlashnBuy</a> en el móvil (o di <b>“Oye Siri, boom”</b> en iPhone).', 'Enfoca el <b>código de barras</b>: con el pitido la app lo reconoce.', 'Si quieres, escribe el <b>precio que ves en la tienda</b>.', 'Toca <b>“¡Encontrado! Ver precios”</b>: se abre Amazon con todas las ofertas de ese producto.'],
  pages={
   'shop': ('¿Tienda o Amazon? Cómo saber dónde es más barato en 5 segundos', '¿Estás en una tienda y no sabes si en Amazon cuesta menos? Escanea el código de barras y compara el precio en segundos, gratis.', 'Tienda o Amazon: <em>¿dónde sale más barato?</em>',
     '<p class="lead">Estás delante de la estantería, el precio parece bueno, pero te surge la duda: ¿y si online cuesta menos? Comprobarlo a mano significa escribir el nombre y el formato correctos y mirar resultados. Con el código de barras es un momento.</p>[[VIDEO]]<h2>Compara el precio en 4 pasos</h2>[[STEPS]]<div class="box"><b>El truco:</b> el código de barras (EAN) identifica el producto exacto, incluido el formato. Así comparas lo mismo, no algo parecido.</div><h2>Cuándo conviene la tienda</h2><ul><li>Lo necesitas <b>ya</b> y no quieres esperar el envío.</li><li>La tienda tiene una <b>oferta</b> o el mismo precio que online.</li><li>Quieres verlo, probarlo o que te aconsejen.</li></ul><h2>Cuándo conviene Amazon</h2><ul><li>El precio es <b>más bajo</b> y puedes esperar el envío.</li><li>Encuentras <b>formatos</b> o packs más baratos.</li><li>Quieres comparar vendedores y leer opiniones.</li></ul><p>BoomFlashnBuy también lleva la cuenta: escribe el precio de la tienda y lo que pagaste en Amazon, y verás cuánto has ahorrado en total.</p>',
     [('¿Hay que instalar algo?', 'No. BoomFlashnBuy funciona desde el navegador del móvil. Si quieres, añádela a la pantalla de inicio como una app.'), ('¿Es gratis?', 'Sí, gratis y sin registro. La app recibe una pequeña comisión de Amazon por las compras que cumplen los requisitos, sin coste para ti.'), ('¿Y si el producto no tiene código de barras?', 'Usa “Leer la etiqueta”: la app lee marca y modelo del texto. O escribe o di lo que buscas.')]),
   'scan': ('App gratis para escanear códigos de barras y comparar precios con Amazon', 'Escáner de códigos de barras gratis que funciona desde el navegador: escanea en la tienda y compara el precio con Amazon. Sin registro.', 'Escáner de <em>códigos de barras</em> gratis',
     '<p class="lead">BoomFlashnBuy es un escáner de códigos de barras pensado para una sola cosa: saber en un instante si el precio de la tienda es bueno.</p>[[VIDEO]]<h2>Qué hace</h2><ul><li>Lee códigos <b>EAN-13, EAN-8, UPC</b> y otros formatos comunes, aunque estén torcidos o lejos.</li><li>Reconoce el producto y prepara la búsqueda en Amazon en la <b>categoría correcta</b>.</li><li>¿Sin código? A los 5 segundos te propone <b>leer la etiqueta</b>.</li><li>Funciona en <b>6 idiomas</b> y usa el Amazon de tu país.</li></ul><h2>Cómo se usa</h2>[[STEPS]]<h2>Privacidad</h2><p>La cámara se usa solo para leer el código, dentro de la app. Búsquedas y gastos se quedan en tu móvil: no hace falta cuenta.</p>',
     [('¿Funciona en iPhone y Android?', 'Sí. En iPhone se abre desde Safari (y con “Oye Siri, boom”), en Android desde Chrome, donde también puedes instalarla con un toque.'), ('¿Por qué no lee el código?', 'Acércate, evita reflejos y enciende la linterna con el icono 🔦. Si aun así no va, usa “Leer la etiqueta”.')]),
   'bf': ('Black Friday 2026: ¿la oferta de la tienda es de verdad más barata que Amazon?', 'El Black Friday 2026 es el viernes 27 de noviembre. Antes de comprar en tienda, escanea el código de barras y compara el precio con Amazon.', 'Black Friday: <em>¿es de verdad una oferta?</em>',
     '<p class="lead">El Black Friday 2026 cae el <b>viernes 27 de noviembre</b>, y el Cyber Monday el lunes 30. Los carteles de “descuento” están por todas partes: la forma más rápida de saber si un precio es bueno es compararlo con Amazon al momento, producto a producto.</p>[[VIDEO]]<h2>En la tienda, en 4 pasos</h2>[[STEPS]]<h2>3 consejos rápidos</h2><ol><li><b>Compara el mismo producto</b>: el código de barras evita confundir modelos y formatos parecidos.</li><li><b>Mira el precio final</b>, no el porcentaje de descuento.</li><li><b>Lleva la cuenta</b>: escribe el precio de la tienda y mira cuánto ahorras en total.</li></ol>',
     [('¿Cuándo es el Black Friday 2026?', 'El viernes 27 de noviembre de 2026. El Cyber Monday es el lunes 30 de noviembre de 2026.'), ('¿La app muestra directamente el precio de Amazon?', 'Abre Amazon con la búsqueda lista para ese producto, donde ves todas las ofertas y vendedores.')]),
  }),
'fr': dict(
  slug={'shop': '/fr/magasin-ou-amazon/', 'scan': '/fr/appli-scanner-code-barre/', 'bf': '/fr/black-friday-prix/'},
  idx=('/fr/', 'Guides BoomFlashnBuy : prix en magasin vs Amazon', 'Guides gratuits : scanne le code-barres en magasin et vois le prix Amazon en quelques secondes.', 'Prix en magasin <em>vs Amazon</em>'),
  open_scan='📷 Ouvrir le scanner', open_app='Ouvrir l’appli', faq='Questions fréquentes', more='Autres guides', foot='BoomFlashnBuy est gratuit et fonctionne dans le navigateur, sans inscription.', upd='Mis à jour le',
  legal='Ça ne te coûte rien : c’est Amazon qui me paie. En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.',
  steps=['Ouvre <a href="/?lang=fr">BoomFlashnBuy</a> sur ton téléphone (ou dis <b>« Dis Siri, boom »</b> sur iPhone).', 'Vise le <b>code-barres</b> : au bip, l’appli le reconnaît.', 'Si tu veux, tape le <b>prix affiché en magasin</b>.', 'Touche <b>« Trouvé ! Voir les prix »</b> : Amazon s’ouvre avec toutes les offres pour ce produit.'],
  pages={
   'shop': ('Magasin ou Amazon ? Savoir où c’est moins cher en 5 secondes', 'En magasin et tu te demandes si c’est moins cher sur Amazon ? Scanne le code-barres et compare le prix en quelques secondes, gratuitement.', 'Magasin ou Amazon : <em>où est-ce moins cher ?</em>',
     '<p class="lead">Tu es devant le rayon, le prix semble correct, mais un doute arrive : et si c’était moins cher en ligne ? Vérifier à la main, c’est taper le bon nom et le bon format, puis faire défiler. Avec le code-barres, c’est immédiat.</p>[[VIDEO]]<h2>Comparer le prix en 4 étapes</h2>[[STEPS]]<div class="box"><b>L’astuce :</b> le code-barres (EAN) identifie le produit exact, format compris. Tu compares la même chose, pas un produit similaire.</div><h2>Quand le magasin gagne</h2><ul><li>Tu en as besoin <b>tout de suite</b>.</li><li>Le magasin a une <b>promo</b> ou le même prix qu’en ligne.</li><li>Tu veux voir, essayer ou te faire conseiller.</li></ul><h2>Quand Amazon gagne</h2><ul><li>Le prix est <b>plus bas</b> et tu peux attendre la livraison.</li><li>Tu trouves des <b>formats</b> ou des lots plus avantageux.</li><li>Tu veux comparer les vendeurs et lire les avis.</li></ul><p>BoomFlashnBuy fait aussi les comptes : tape le prix du magasin et ce que tu as payé sur Amazon, et vois combien tu as économisé au total.</p>',
     [('Faut-il installer quelque chose ?', 'Non. BoomFlashnBuy fonctionne dans le navigateur du téléphone. Tu peux l’ajouter à l’écran d’accueil comme une appli.'), ('C’est gratuit ?', 'Oui, gratuit et sans inscription. L’appli reçoit une petite commission d’Amazon sur les achats éligibles, sans frais pour toi.'), ('Et si le produit n’a pas de code-barres ?', 'Utilise « Lire l’étiquette » : l’appli lit la marque et le modèle. Ou écris ou dis ce que tu cherches.')]),
   'scan': ('Appli gratuite pour scanner un code-barres et comparer les prix avec Amazon', 'Scanner de code-barres gratuit qui fonctionne dans le navigateur : scanne en magasin et compare le prix avec Amazon. Sans inscription.', 'Scanner de <em>code-barres</em> gratuit',
     '<p class="lead">BoomFlashnBuy est un scanner de code-barres conçu pour une seule chose : savoir en un éclair si le prix du magasin est bon.</p>[[VIDEO]]<h2>Ce qu’il fait</h2><ul><li>Lit les codes <b>EAN-13, EAN-8, UPC</b> et d’autres formats courants, même de travers ou de loin.</li><li>Reconnaît le produit et prépare la recherche Amazon dans le <b>bon rayon</b>.</li><li>Pas de code ? Après 5 secondes, il propose de <b>lire l’étiquette</b>.</li><li>Fonctionne en <b>6 langues</b> et utilise l’Amazon de ton pays.</li></ul><h2>Comment l’utiliser</h2>[[STEPS]]<h2>Confidentialité</h2><p>La caméra sert seulement à lire le code, dans l’appli. Recherches et dépenses restent sur ton téléphone : pas besoin de compte.</p>',
     [('Ça marche sur iPhone et Android ?', 'Oui. Sur iPhone, ouvre-la dans Safari (et avec « Dis Siri, boom »), sur Android dans Chrome, où tu peux aussi l’installer en un geste.'), ('Pourquoi le code n’est pas lu ?', 'Rapproche-toi, évite les reflets et allume la lampe avec l’icône 🔦. Sinon, utilise « Lire l’étiquette ».')]),
   'bf': ('Black Friday 2026 : la promo en magasin est-elle vraiment moins chère qu’Amazon ?', 'Le Black Friday 2026 tombe le vendredi 27 novembre. Avant d’acheter en magasin, scanne le code-barres et compare le prix avec Amazon.', 'Black Friday : <em>vraie bonne affaire ?</em>',
     '<p class="lead">Le Black Friday 2026 tombe le <b>vendredi 27 novembre</b>, et le Cyber Monday le lundi 30. Les affiches « promo » sont partout : le moyen le plus rapide de savoir si un prix est vraiment bon, c’est de le comparer avec Amazon sur place, produit par produit.</p>[[VIDEO]]<h2>En magasin, en 4 étapes</h2>[[STEPS]]<h2>3 conseils rapides</h2><ol><li><b>Compare le même produit</b> : le code-barres évite de confondre des modèles et formats proches.</li><li><b>Regarde le prix final</b>, pas le pourcentage de remise.</li><li><b>Fais les comptes</b> : tape le prix du magasin et vois combien tu économises au total.</li></ol>',
     [('Quand est le Black Friday 2026 ?', 'Le vendredi 27 novembre 2026. Le Cyber Monday est le lundi 30 novembre 2026.'), ('L’appli affiche-t-elle directement le prix Amazon ?', 'Elle ouvre Amazon avec la recherche prête pour ce produit, où tu vois toutes les offres et les vendeurs.')]),
  }),
'de': dict(
  slug={'shop': '/de/laden-oder-amazon/', 'scan': '/de/barcode-scanner-app/', 'bf': '/de/black-friday-preise/'},
  idx=('/de/', 'BoomFlashnBuy Ratgeber: Ladenpreis vs. Amazon', 'Kostenlose Ratgeber: Barcode im Laden scannen und den Amazon-Preis in Sekunden sehen.', 'Ladenpreis <em>vs. Amazon</em>'),
  open_scan='📷 Scanner öffnen', open_app='App öffnen', faq='Häufige Fragen', more='Weitere Ratgeber', foot='BoomFlashnBuy ist kostenlos und läuft im Browser, ohne Anmeldung.', upd='Aktualisiert am',
  legal='Dich kostet es nichts: Amazon bezahlt mich. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.',
  steps=['Öffne <a href="/?lang=de">BoomFlashnBuy</a> auf dem Handy (oder sag <b>„Hey Siri, boom“</b> auf dem iPhone).', 'Halte die Kamera auf den <b>Barcode</b>: beim Piepton erkennt die App ihn.', 'Wenn du willst, tippe den <b>Preis im Laden</b> ein.', 'Tippe auf <b>„Gefunden! Zu den Preisen“</b>: Amazon öffnet sich mit allen Angeboten für dieses Produkt.'],
  pages={
   'shop': ('Laden oder Amazon? In 5 Sekunden herausfinden, wo es günstiger ist', 'Im Laden und unsicher, ob es bei Amazon billiger ist? Barcode scannen und den Preis in Sekunden vergleichen – kostenlos.', 'Laden oder Amazon: <em>wo ist es günstiger?</em>',
     '<p class="lead">Du stehst vor dem Regal, der Preis wirkt okay, aber du fragst dich: Ist es online billiger? Von Hand heißt das: richtigen Namen und Größe eintippen und durch Ergebnisse scrollen. Mit dem Barcode geht es sofort.</p>[[VIDEO]]<h2>Preis vergleichen in 4 Schritten</h2>[[STEPS]]<div class="box"><b>Der Trick:</b> Der Barcode (EAN) bestimmt das genaue Produkt inklusive Größe. So vergleichst du dasselbe, nicht etwas Ähnliches.</div><h2>Wann der Laden gewinnt</h2><ul><li>Du brauchst es <b>sofort</b>.</li><li>Der Laden hat ein <b>Angebot</b> oder denselben Preis wie online.</li><li>Du willst es sehen, ausprobieren oder beraten werden.</li></ul><h2>Wann Amazon gewinnt</h2><ul><li>Der Preis ist <b>niedriger</b> und du kannst auf die Lieferung warten.</li><li>Es gibt günstigere <b>Größen</b> oder Mehrfachpackungen.</li><li>Du willst Verkäufer vergleichen und Bewertungen lesen.</li></ul><p>BoomFlashnBuy rechnet auch mit: Ladenpreis und Amazon-Preis eintippen und sehen, wie viel du insgesamt gespart hast.</p>',
     [('Muss ich etwas installieren?', 'Nein. BoomFlashnBuy läuft im Handy-Browser. Du kannst es wie eine App zum Home-Bildschirm hinzufügen.'), ('Ist es kostenlos?', 'Ja, kostenlos und ohne Anmeldung. Die App erhält von Amazon eine kleine Provision auf qualifizierte Käufe – ohne Kosten für dich.'), ('Und wenn das Produkt keinen Barcode hat?', 'Nutze „Etikett lesen“: Die App liest Marke und Modell aus dem Text. Oder schreib oder sag, was du suchst.')]),
   'scan': ('Kostenlose Barcode-Scanner-App zum Preisvergleich mit Amazon', 'Kostenloser Barcode-Scanner im Browser: Code im Laden scannen und den Preis mit Amazon vergleichen. Ohne Anmeldung.', 'Kostenloser <em>Barcode-Scanner</em>',
     '<p class="lead">BoomFlashnBuy ist ein Barcode-Scanner für genau eine Sache: blitzschnell zu wissen, ob der Ladenpreis gut ist.</p>[[VIDEO]]<h2>Was er kann</h2><ul><li>Liest <b>EAN-13, EAN-8, UPC</b> und andere gängige Formate, auch schräg oder aus der Ferne.</li><li>Erkennt das Produkt und bereitet die Amazon-Suche in der <b>richtigen Kategorie</b> vor.</li><li>Kein Barcode? Nach 5 Sekunden bietet er an, das <b>Etikett zu lesen</b>.</li><li>Funktioniert in <b>6 Sprachen</b> und nutzt das Amazon deines Landes.</li></ul><h2>So geht’s</h2>[[STEPS]]<h2>Datenschutz</h2><p>Die Kamera wird nur zum Lesen des Codes in der App genutzt. Suchen und Ausgaben bleiben auf deinem Handy: kein Konto nötig.</p>',
     [('Funktioniert es auf iPhone und Android?', 'Ja. Auf dem iPhone in Safari öffnen (und mit „Hey Siri, boom“), auf Android in Chrome, wo du es auch mit einem Tipp installieren kannst.'), ('Warum wird der Code nicht gelesen?', 'Näher rangehen, Spiegelungen vermeiden und die Taschenlampe mit 🔦 einschalten. Sonst „Etikett lesen“ nutzen.')]),
   'bf': ('Black Friday 2026: Ist das Angebot im Laden wirklich günstiger als Amazon?', 'Black Friday 2026 ist am Freitag, 27. November. Vor dem Kauf im Laden Barcode scannen und den Preis mit Amazon vergleichen.', 'Black Friday: <em>wirklich ein Schnäppchen?</em>',
     '<p class="lead">Black Friday 2026 ist am <b>Freitag, 27. November</b>, Cyber Monday am Montag, 30. November. „Rabatt“-Schilder hängen überall: Am schnellsten erkennst du einen guten Preis, wenn du ihn direkt vor Ort mit Amazon vergleichst – Produkt für Produkt.</p>[[VIDEO]]<h2>Im Laden, in 4 Schritten</h2>[[STEPS]]<h2>3 schnelle Tipps</h2><ol><li><b>Dasselbe Produkt vergleichen</b>: Der Barcode verhindert Verwechslungen bei ähnlichen Modellen und Größen.</li><li><b>Auf den Endpreis achten</b>, nicht auf den Rabatt in Prozent.</li><li><b>Mitrechnen</b>: Ladenpreis eintippen und sehen, wie viel du insgesamt sparst.</li></ol>',
     [('Wann ist Black Friday 2026?', 'Am Freitag, 27. November 2026. Cyber Monday ist am Montag, 30. November 2026.'), ('Zeigt die App den Amazon-Preis direkt an?', 'Sie öffnet Amazon mit der fertigen Suche für dieses Produkt, wo du alle Angebote und Verkäufer siehst.')]),
  }),
'pt': dict(
  slug={'shop': '/pt/loja-ou-amazon/', 'scan': '/pt/app-leitor-codigo-de-barras/', 'bf': '/pt/black-friday-precos/'},
  idx=('/pt/', 'Guias BoomFlashnBuy: preço na loja vs Amazon', 'Guias grátis: lê o código de barras na loja e vê o preço na Amazon em segundos.', 'Preço na loja <em>vs Amazon</em>'),
  open_scan='📷 Abrir o leitor', open_app='Abrir a app', faq='Perguntas frequentes', more='Mais guias', foot='BoomFlashnBuy é grátis e funciona no navegador, sem registo.', upd='Atualizado a',
  legal='A ti não custa nada: paga-me a Amazon. Como Associado da Amazon, ganho com compras qualificadas.',
  steps=['Abre <a href="/?lang=pt">BoomFlashnBuy</a> no telemóvel (ou diz <b>“E aí Siri, boom”</b> no iPhone).', 'Aponta para o <b>código de barras</b>: com o bip a app reconhece-o.', 'Se quiseres, escreve o <b>preço que vês na loja</b>.', 'Toca em <b>“Encontrado! Ver preços”</b>: abre-se a Amazon com todas as ofertas desse produto.'],
  pages={
   'shop': ('Loja ou Amazon? Como saber onde é mais barato em 5 segundos', 'Estás numa loja e não sabes se na Amazon é mais barato? Lê o código de barras e compara o preço em segundos, grátis.', 'Loja ou Amazon: <em>onde compensa?</em>',
     '<p class="lead">Estás em frente à prateleira, o preço parece bom, mas surge a dúvida: e se online for mais barato? Verificar à mão é escrever o nome e o formato certos e percorrer resultados. Com o código de barras é num instante.</p>[[VIDEO]]<h2>Comparar o preço em 4 passos</h2>[[STEPS]]<div class="box"><b>O truque:</b> o código de barras (EAN) identifica o produto exato, incluindo o formato. Assim comparas a mesma coisa, não algo parecido.</div><h2>Quando compensa a loja</h2><ul><li>Precisas <b>já</b> e não queres esperar pela entrega.</li><li>A loja tem uma <b>promoção</b> ou o mesmo preço que online.</li><li>Queres ver, experimentar ou pedir conselho.</li></ul><h2>Quando compensa a Amazon</h2><ul><li>O preço é <b>mais baixo</b> e podes esperar pela entrega.</li><li>Encontras <b>formatos</b> ou packs mais vantajosos.</li><li>Queres comparar vendedores e ler opiniões.</li></ul><p>A BoomFlashnBuy também faz as contas: escreve o preço da loja e o que pagaste na Amazon, e vê quanto poupaste no total.</p>',
     [('É preciso instalar alguma coisa?', 'Não. A BoomFlashnBuy funciona no navegador do telemóvel. Se quiseres, adiciona-a ao ecrã principal como uma app.'), ('É grátis?', 'Sim, grátis e sem registo. A app recebe uma pequena comissão da Amazon pelas compras qualificadas, sem custo para ti.'), ('E se o produto não tiver código de barras?', 'Usa “Ler a etiqueta”: a app lê a marca e o modelo. Ou escreve ou diz o que procuras.')]),
   'scan': ('App grátis para ler códigos de barras e comparar preços com a Amazon', 'Leitor de códigos de barras grátis que funciona no navegador: lê o código na loja e compara o preço com a Amazon. Sem registo.', 'Leitor de <em>códigos de barras</em> grátis',
     '<p class="lead">A BoomFlashnBuy é um leitor de códigos de barras feito para uma coisa só: saber num instante se o preço da loja é bom.</p>[[VIDEO]]<h2>O que faz</h2><ul><li>Lê códigos <b>EAN-13, EAN-8, UPC</b> e outros formatos comuns, mesmo tortos ou ao longe.</li><li>Reconhece o produto e prepara a pesquisa na Amazon na <b>categoria certa</b>.</li><li>Sem código? Após 5 segundos propõe <b>ler a etiqueta</b>.</li><li>Funciona em <b>6 línguas</b> e usa a Amazon do teu país.</li></ul><h2>Como se usa</h2>[[STEPS]]<h2>Privacidade</h2><p>A câmara é usada só para ler o código, dentro da app. Pesquisas e gastos ficam no teu telemóvel: não é preciso conta.</p>',
     [('Funciona no iPhone e no Android?', 'Sim. No iPhone abre-se no Safari (e com “E aí Siri, boom”), no Android no Chrome, onde também a podes instalar com um toque.'), ('Porque é que o código não é lido?', 'Aproxima-te, evita reflexos e liga a lanterna no ícone 🔦. Se mesmo assim não der, usa “Ler a etiqueta”.')]),
   'bf': ('Black Friday 2026: a promoção na loja é mesmo mais barata que a Amazon?', 'A Black Friday 2026 é na sexta-feira, 27 de novembro. Antes de comprar na loja, lê o código de barras e compara o preço com a Amazon.', 'Black Friday: <em>é mesmo promoção?</em>',
     '<p class="lead">A Black Friday 2026 calha na <b>sexta-feira, 27 de novembro</b>, e a Cyber Monday na segunda, 30. Há cartazes de “desconto” por todo o lado: a forma mais rápida de saber se um preço é bom é compará-lo com a Amazon na hora, produto a produto.</p>[[VIDEO]]<h2>Na loja, em 4 passos</h2>[[STEPS]]<h2>3 dicas rápidas</h2><ol><li><b>Compara o mesmo produto</b>: o código de barras evita confundir modelos e formatos parecidos.</li><li><b>Olha para o preço final</b>, não para a percentagem de desconto.</li><li><b>Faz as contas</b>: escreve o preço da loja e vê quanto poupas no total.</li></ol>',
     [('Quando é a Black Friday 2026?', 'Sexta-feira, 27 de novembro de 2026. A Cyber Monday é segunda-feira, 30 de novembro de 2026.'), ('A app mostra diretamente o preço da Amazon?', 'Abre a Amazon com a pesquisa pronta para esse produto, onde vês todas as ofertas e vendedores.')]),
  }),
}

def alt_links(key):
    """<link hreflang> per una guida (key) o per l'indice (key=None)."""
    if key is None:
        m = {'it': '/guide/'} | {lg: T[lg]['idx'][0] for lg in T}
    else:
        m = {'it': IT_SLUG[key]} | {lg: T[lg]['slug'][key] for lg in T}
    s = ''.join(f'<link rel="alternate" hreflang="{lg}" href="{BASE}{u}">' for lg, u in m.items())
    return s + f'<link rel="alternate" hreflang="x-default" href="{BASE}{m["en"]}">', m

def langbar(m, cur):
    names = {'it': 'IT', 'en': 'EN', 'es': 'ES', 'fr': 'FR', 'de': 'DE', 'pt': 'PT'}
    return '<p style="font-size:14px;margin:0 0 6px">' + ' · '.join(
        f'<b>{names[l]}</b>' if l == cur else f'<a href="{u}">{names[l]}</a>' for l, u in m.items()) + '</p>'

VIDEO_JS = ("<script>(function(){var L=['it','en','es','fr','de','pt'],g=document.documentElement.lang;if(L.indexOf(g)<0)g='en';"
  "var o=matchMedia('(orientation:portrait)').matches?'verticale':'orizzontale';"
  "document.querySelectorAll('video.bfb').forEach(function(v){var u='/media/BoomFlashnBuy-'+g+'-'+o+'.mp4';"
  "if(v.currentSrc.indexOf(u)<0){v.querySelector('source').src=u;v.load()}})})()</script>")

def render(lg, key):
    D = T[lg]; title, desc, h1, body, faq = D['pages'][key]; slug = D['slug'][key]
    alts, m = alt_links(key)
    vfile = f'/media/BoomFlashnBuy-{lg}-orizzontale.mp4'
    vid = f'<video class="bfb" controls playsinline preload="metadata" poster="{S.POSTER}"><source src="{vfile}" type="video/mp4"></video>' + VIDEO_JS
    steps = '<ol>' + ''.join(f'<li>{x}</li>' for x in D['steps']) + '</ol>'
    body = body.replace('[[VIDEO]]', vid).replace('[[STEPS]]', steps)
    app_ld = dict(S.APP_LD, url=f'{BASE}/?lang={lg}')
    vld = dict(S.VIDEO_LD, name=title, description=desc, contentUrl=BASE + vfile, embedUrl=BASE + slug, inLanguage=lg)
    lds = [app_ld, vld, S.faq_ld(faq)]
    fq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    more = ''.join(f'<a href="{D["slug"][k]}">{D["pages"][k][0]} →</a>' for k in KEYS if k != key)
    return f'''<!doctype html><html lang="{lg}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{BASE}{slug}">{alts}
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{BASE}{slug}"><meta property="og:image" content="{BASE}{S.OG}"><meta property="og:locale" content="{LOC[lg]}">
<meta property="og:video" content="{BASE}{vfile}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icons/favicon-48.png"><link rel="apple-touch-icon" href="/icons/apple-touch-icon.png"><meta name="theme-color" content="#0B0C0A">
<style>{S.CSS}</style>{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}</head>
<body><div class="w"><header><img src="/icons/icon-192.png" alt="" width="44" height="44"><a href="/?lang={lg}">Boom<em>Flash</em>nBuy</a></header>
<main>{langbar(m, lg)}<h1>{h1}</h1>{body}
<div class="cta"><a class="btn" href="/?boom=1&amp;lang={lg}">{D['open_scan']}</a><a class="btn g" href="/?lang={lg}">{D['open_app']}</a></div>
<h2>{D['faq']}</h2>{fq}
<h2>{D['more']}</h2><nav class="more">{more}<a href="{D['idx'][0]}">{D['idx'][1]} →</a></nav></main>
<footer>{D['foot']} {D['legal']}<br>{D['upd']} {TODAY}.</footer></div></body></html>'''

def render_idx(lg):
    D = T[lg]; slug, title, desc, h1 = D['idx']
    alts, m = alt_links(None)
    items = ''.join(f'<a href="{D["slug"][k]}">{D["pages"][k][0]} →</a>' for k in KEYS)
    return f'''<!doctype html><html lang="{lg}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{BASE}{slug}">{alts}
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{BASE}{S.OG}"><meta property="og:locale" content="{LOC[lg]}">
<link rel="icon" href="/icons/favicon-48.png"><meta name="theme-color" content="#0B0C0A"><style>{S.CSS}</style></head>
<body><div class="w"><header><img src="/icons/icon-192.png" alt="" width="44" height="44"><a href="/?lang={lg}">Boom<em>Flash</em>nBuy</a></header>
<main>{langbar(m, lg)}<h1>{h1}</h1><p class="lead">{html.escape(desc)}</p>
<div class="cta"><a class="btn" href="/?boom=1&amp;lang={lg}">{D['open_scan']}</a><a class="btn g" href="/?lang={lg}">{D['open_app']}</a></div>
<nav class="more">{items}</nav></main><footer>{D['foot']} {D['legal']}</footer></div></body></html>'''

new_urls = []
for lg in T:
    for k in KEYS:
        S.write(T[lg]['slug'][k].strip('/') + '/index.html', render(lg, k)); new_urls.append(T[lg]['slug'][k])
    S.write(T[lg]['idx'][0].strip('/') + '/index.html', render_idx(lg)); new_urls.append(T[lg]['idx'][0])

# hreflang + barra lingue nelle pagine italiane
for key in KEYS + [None]:
    rel = (IT_SLUG[key] if key else '/guide/').strip('/') + '/index.html'
    p = os.path.join(ROOT, rel); s = open(p, encoding='utf-8').read()
    alts, m = alt_links(key)
    s = s.replace("c=[q].concat(", "c=[q,'it'].concat(")  # guida italiana: video in italiano
    if 'hreflang' not in s:
        s = s.replace('<meta property="og:type"', alts + '\n<meta property="og:type"', 1) if '<meta property="og:type"' in s else s.replace('</head>', alts + '</head>', 1)
        s = s.replace('<main>', '<main>' + langbar(m, 'it'), 1)
    open(p, 'w', encoding='utf-8').write(s)

# sitemap: aggiungi le nuove pagine
sp = os.path.join(ROOT, 'sitemap.xml'); sm = open(sp, encoding='utf-8').read()
add = ''.join(f'<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in new_urls if f'{BASE}{u}<' not in sm)
sm = sm.replace('</urlset>', add + '</urlset>'); open(sp, 'w', encoding='utf-8').write(sm)
print('pagine nuove:', len(new_urls))
