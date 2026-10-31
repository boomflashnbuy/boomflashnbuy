"""Pagine di nicchia (settore per settore) in 6 lingue, collegate con hreflang.
Uso: python3 tools/seo_niches.py https://boomflashnbuy.netlify.app
Rigenera prima tutto il resto (seo_build + seo_i18n), poi aggiunge le nicchie."""
import sys, os, json, html, urllib.parse, glob
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import seo_i18n as I  # rigenera guide IT + lingue + sitemap
S = I.S; BASE, ROOT, TODAY = S.BASE, S.ROOT, S.TODAY
LANGS = ['it', 'en', 'es', 'fr', 'de', 'pt']
LOC = {'it': 'it_IT'} | I.LOC
CF = I.render('en', 'shop')[I.render('en', 'shop').find("<script defer src='https://static.cloudflareinsights"):].split('</script>')[0] + '</script>'
ROBOTS = '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'

UI = {
 'it': dict(scan='📷 Apri lo scanner', app='Apri l’app', faq='Domande frequenti', more='Nello stesso settore', try_='Tocca una ricerca: l’app trova le offerte su Amazon.', foot='BoomFlashnBuy è gratis e funziona dal browser, senza registrazione.', upd='Aggiornato il', all='Tutte le guide', allu='/guide/', legal=S.LEGAL),
 'en': dict(scan='📷 Open the scanner', app='Open the app', faq='FAQ', more='In the same section', try_='Tap a search: the app finds the offers on Amazon.', foot=I.T['en']['foot'], upd='Updated', all='All guides', allu='/en/', legal=I.T['en']['legal']),
 'es': dict(scan='📷 Abrir el escáner', app='Abrir la app', faq='Preguntas frecuentes', more='En la misma sección', try_='Toca una búsqueda: la app encuentra las ofertas en Amazon.', foot=I.T['es']['foot'], upd='Actualizado el', all='Todas las guías', allu='/es/', legal=I.T['es']['legal']),
 'fr': dict(scan='📷 Ouvrir le scanner', app='Ouvrir l’appli', faq='Questions fréquentes', more='Dans la même rubrique', try_='Touche une recherche : l’appli trouve les offres Amazon.', foot=I.T['fr']['foot'], upd='Mis à jour le', all='Tous les guides', allu='/fr/', legal=I.T['fr']['legal']),
 'de': dict(scan='📷 Scanner öffnen', app='App öffnen', faq='Häufige Fragen', more='Im selben Bereich', try_='Tippe auf eine Suche: Die App findet die Angebote bei Amazon.', foot=I.T['de']['foot'], upd='Aktualisiert am', all='Alle Ratgeber', allu='/de/', legal=I.T['de']['legal']),
 'pt': dict(scan='📷 Abrir o leitor', app='Abrir a app', faq='Perguntas frequentes', more='Na mesma secção', try_='Toca numa pesquisa: a app encontra as ofertas na Amazon.', foot=I.T['pt']['foot'], upd='Atualizado a', all='Todos os guias', allu='/pt/', legal=I.T['pt']['legal']),
}

# ---------------- NICCHIA: MODA (6% di commissione su amazon.it) ----------------
# ogni pagina: slug, title, desc, h1, body (html, [[VIDEO]] [[CHIPS]]), chips (testi di ricerca), faq
N = {}
N['moda'] = {
 'it': dict(slug='/moda/', title='Scarpe e vestiti: prezzo in negozio o su Amazon? Controlla in 5 secondi',
   desc='Sneakers, giubbotti, jeans, borse: scansiona il codice sul cartellino o sulla scatola e confronta subito il prezzo con Amazon. Gratis.',
   h1='Scarpe e vestiti: <em>negozio o Amazon?</em>',
   body='''<p class="lead">Nella moda la stessa scarpa o lo stesso giubbotto può costare molto meno online, soprattutto a fine stagione. Prima di andare in cassa basta un'occhiata.</p>[[VIDEO]]
<h2>Dove trovare il codice</h2><ul><li><b>Scarpe:</b> il codice a barre è sull'etichetta della <b>scatola</b>, di lato. Dentro la linguetta c'è anche il <b>codice modello</b> (per esempio Nike CW2288-111, Adidas B75806): l'app lo legge con “Leggi l'etichetta”.</li><li><b>Vestiti e giubbotti:</b> il codice a barre è sul <b>cartellino del prezzo</b> appeso al capo.</li><li><b>Borse e accessori:</b> cartellino o etichetta interna.</li></ul>
<h2>Cerca subito</h2><p>[[TRY]]</p>[[CHIPS]]
<div class="box"><b>Taglie:</b> prima di comprare online prova il capo in negozio e annota la taglia del marchio, poi confronta il prezzo. Molti articoli moda su Amazon hanno il reso gratuito: controlla la scritta nella pagina del prodotto.</div>''',
   chips=['sneakers uomo', 'sneakers donna', 'giubbotto invernale uomo', 'piumino donna', "jeans Levi's 501", 'scarpe running', 'stivali donna', 'borsa donna', 'orologio uomo'],
   faq=[('Funziona con tutte le marche?', 'Sì: se il prodotto ha un codice a barre o un codice modello, l’app prepara la ricerca su Amazon per quel prodotto esatto.'), ('Conviene sempre Amazon?', 'No. A volte il negozio ha un’offerta migliore o ti serve subito: l’app ti fa solo vedere il confronto, decidi tu.')]),
 'en': dict(slug='/en/fashion/', title='Shoes and clothes: store price or Amazon? Check in 5 seconds',
   desc='Sneakers, jackets, jeans, bags: scan the code on the tag or the box and compare the price with Amazon right away. Free.',
   h1='Shoes and clothes: <em>store or Amazon?</em>',
   body='''<p class="lead">In fashion the same shoe or jacket can cost much less online, especially at the end of a season. Check before you queue at the till.</p>[[VIDEO]]
<h2>Where to find the code</h2><ul><li><b>Shoes:</b> the barcode is on the label on the side of the <b>box</b>. Inside the tongue there is also the <b>style code</b> (e.g. Nike CW2288-111, Adidas B75806): the app reads it with “Read the label”.</li><li><b>Clothes and jackets:</b> the barcode is on the <b>price tag</b> attached to the item.</li><li><b>Bags and accessories:</b> price tag or inside label.</li></ul>
<h2>Search now</h2><p>[[TRY]]</p>[[CHIPS]]
<div class="box"><b>Sizes:</b> try the item on in the store and note the brand size, then compare the price. Many fashion items on Amazon have free returns: check the product page.</div>''',
   chips=['mens sneakers', 'womens sneakers', 'mens winter jacket', 'womens puffer jacket', "Levi's 501 jeans", 'running shoes', 'womens boots', 'womens handbag', 'mens watch'],
   faq=[('Does it work with every brand?', 'Yes: if the product has a barcode or a style code, the app prepares the Amazon search for that exact product.'), ('Is Amazon always cheaper?', 'No. Sometimes the store has a better deal or you need it now: the app just shows you the comparison, you decide.')]),
 'es': dict(slug='/es/moda/', title='Zapatillas y ropa: ¿precio en tienda o en Amazon? Compruébalo en 5 segundos',
   desc='Zapatillas, chaquetas, vaqueros, bolsos: escanea el código de la etiqueta o de la caja y compara el precio con Amazon al momento. Gratis.',
   h1='Zapatillas y ropa: <em>¿tienda o Amazon?</em>',
   body='''<p class="lead">En moda, la misma zapatilla o chaqueta puede costar mucho menos online, sobre todo a final de temporada. Compruébalo antes de pasar por caja.</p>[[VIDEO]]
<h2>Dónde está el código</h2><ul><li><b>Zapatillas:</b> el código de barras está en la etiqueta del lateral de la <b>caja</b>. Dentro de la lengüeta está el <b>código de modelo</b> (p. ej. Nike CW2288-111, Adidas B75806): la app lo lee con “Leer la etiqueta”.</li><li><b>Ropa y chaquetas:</b> el código de barras está en la <b>etiqueta del precio</b> colgada de la prenda.</li><li><b>Bolsos y accesorios:</b> etiqueta del precio o etiqueta interior.</li></ul>
<h2>Busca ya</h2><p>[[TRY]]</p>[[CHIPS]]
<div class="box"><b>Tallas:</b> pruébate la prenda en la tienda y apunta la talla de la marca; luego compara el precio. Muchos artículos de moda en Amazon tienen devolución gratuita: míralo en la página del producto.</div>''',
   chips=['zapatillas hombre', 'zapatillas mujer', 'chaqueta invierno hombre', 'plumífero mujer', "vaqueros Levi's 501", 'zapatillas running', 'botas mujer', 'bolso mujer', 'reloj hombre'],
   faq=[('¿Funciona con todas las marcas?', 'Sí: si el producto tiene código de barras o código de modelo, la app prepara la búsqueda en Amazon de ese producto exacto.'), ('¿Amazon siempre es más barato?', 'No. A veces la tienda tiene mejor oferta o lo necesitas ya: la app solo te enseña la comparación, decides tú.')]),
 'fr': dict(slug='/fr/mode/', title='Chaussures et vêtements : prix en magasin ou sur Amazon ? Vérifie en 5 secondes',
   desc='Baskets, doudounes, jeans, sacs : scanne le code de l’étiquette ou de la boîte et compare tout de suite le prix avec Amazon. Gratuit.',
   h1='Chaussures et vêtements : <em>magasin ou Amazon ?</em>',
   body='''<p class="lead">En mode, la même basket ou la même veste peut coûter bien moins cher en ligne, surtout en fin de saison. Vérifie avant de passer en caisse.</p>[[VIDEO]]
<h2>Où trouver le code</h2><ul><li><b>Chaussures :</b> le code-barres est sur l’étiquette sur le côté de la <b>boîte</b>. Dans la languette, il y a aussi la <b>référence du modèle</b> (ex. Nike CW2288-111, Adidas B75806) : l’appli la lit avec « Lire l’étiquette ».</li><li><b>Vêtements et vestes :</b> le code-barres est sur l’<b>étiquette de prix</b> accrochée au vêtement.</li><li><b>Sacs et accessoires :</b> étiquette de prix ou étiquette intérieure.</li></ul>
<h2>Cherche maintenant</h2><p>[[TRY]]</p>[[CHIPS]]
<div class="box"><b>Tailles :</b> essaie le vêtement en magasin et note la taille de la marque, puis compare le prix. Beaucoup d’articles de mode sur Amazon ont le retour gratuit : vérifie sur la page du produit.</div>''',
   chips=['baskets homme', 'baskets femme', 'veste hiver homme', 'doudoune femme', "jean Levi's 501", 'chaussures running', 'bottes femme', 'sac à main femme', 'montre homme'],
   faq=[('Ça marche avec toutes les marques ?', 'Oui : si le produit a un code-barres ou une référence, l’appli prépare la recherche Amazon pour ce produit exact.'), ('Amazon est-il toujours moins cher ?', 'Non. Parfois le magasin a une meilleure offre ou tu en as besoin tout de suite : l’appli montre la comparaison, tu décides.')]),
 'de': dict(slug='/de/mode/', title='Schuhe und Kleidung: Ladenpreis oder Amazon? In 5 Sekunden prüfen',
   desc='Sneaker, Jacken, Jeans, Taschen: Code auf dem Etikett oder Karton scannen und den Preis sofort mit Amazon vergleichen. Kostenlos.',
   h1='Schuhe und Kleidung: <em>Laden oder Amazon?</em>',
   body='''<p class="lead">Bei Mode kann derselbe Schuh oder dieselbe Jacke online deutlich weniger kosten, vor allem am Saisonende. Prüf es, bevor du zur Kasse gehst.</p>[[VIDEO]]
<h2>Wo der Code steht</h2><ul><li><b>Schuhe:</b> Der Barcode klebt seitlich auf dem <b>Karton</b>. In der Zunge steht außerdem die <b>Artikelnummer</b> (z. B. Nike CW2288-111, Adidas B75806): Die App liest sie mit „Etikett lesen“.</li><li><b>Kleidung und Jacken:</b> Der Barcode ist auf dem <b>Preisschild</b> am Kleidungsstück.</li><li><b>Taschen und Accessoires:</b> Preisschild oder Innenetikett.</li></ul>
<h2>Jetzt suchen</h2><p>[[TRY]]</p>[[CHIPS]]
<div class="box"><b>Größen:</b> Probier das Teil im Laden an und merk dir die Größe der Marke, dann vergleich den Preis. Viele Modeartikel auf Amazon haben kostenlose Rücksendung: Das steht auf der Produktseite.</div>''',
   chips=['Sneaker Herren', 'Sneaker Damen', 'Winterjacke Herren', 'Daunenjacke Damen', "Levi's 501 Jeans", 'Laufschuhe', 'Stiefel Damen', 'Handtasche Damen', 'Herrenuhr'],
   faq=[('Funktioniert das mit allen Marken?', 'Ja: Hat das Produkt einen Barcode oder eine Artikelnummer, bereitet die App die Amazon-Suche für genau dieses Produkt vor.'), ('Ist Amazon immer günstiger?', 'Nein. Manchmal hat der Laden das bessere Angebot oder du brauchst es sofort: Die App zeigt nur den Vergleich, du entscheidest.')]),
 'pt': dict(slug='/pt/moda/', title='Sapatilhas e roupa: preço na loja ou na Amazon? Confirma em 5 segundos',
   desc='Sapatilhas, casacos, calças de ganga, malas: lê o código da etiqueta ou da caixa e compara já o preço com a Amazon. Grátis.',
   h1='Sapatilhas e roupa: <em>loja ou Amazon?</em>',
   body='''<p class="lead">Na moda, a mesma sapatilha ou o mesmo casaco pode custar muito menos online, sobretudo no fim da estação. Confirma antes de ir à caixa.</p>[[VIDEO]]
<h2>Onde está o código</h2><ul><li><b>Sapatos:</b> o código de barras está na etiqueta lateral da <b>caixa</b>. Dentro da lingueta está também o <b>código do modelo</b> (ex. Nike CW2288-111, Adidas B75806): a app lê-o com “Ler a etiqueta”.</li><li><b>Roupa e casacos:</b> o código de barras está na <b>etiqueta do preço</b> presa à peça.</li><li><b>Malas e acessórios:</b> etiqueta do preço ou etiqueta interior.</li></ul>
<h2>Pesquisa já</h2><p>[[TRY]]</p>[[CHIPS]]
<div class="box"><b>Tamanhos:</b> experimenta a peça na loja e aponta o tamanho da marca; depois compara o preço. Muitos artigos de moda na Amazon têm devolução grátis: vê na página do produto.</div>''',
   chips=['sapatilhas homem', 'sapatilhas mulher', 'casaco inverno homem', 'casaco acolchoado mulher', "calças Levi's 501", 'sapatilhas running', 'botas mulher', 'mala mulher', 'relógio homem'],
   faq=[('Funciona com todas as marcas?', 'Sim: se o produto tiver código de barras ou código de modelo, a app prepara a pesquisa na Amazon desse produto exato.'), ('A Amazon é sempre mais barata?', 'Não. Às vezes a loja tem melhor oferta ou precisas já: a app só mostra a comparação, decides tu.')]),
}
SNK = ['Nike Air Force 1', 'Adidas Samba', 'New Balance 530', 'Nike Dunk Low', 'Converse Chuck Taylor', 'Asics Gel-Kayano', 'Vans Old Skool', 'Puma Suede', 'Veja Campo']
N['sneakers'] = {
 'it': dict(slug='/moda/sneakers/', title='Sneakers: prezzo in negozio o su Amazon? Nike, Adidas, New Balance e altre',
   desc='Prima di comprare sneakers in negozio, scansiona la scatola o leggi il codice nella linguetta e confronta il prezzo su Amazon. Gratis.',
   h1='Sneakers: <em>il prezzo giusto in un lampo</em>',
   body='''<p class="lead">Le sneakers sono tra gli acquisti dove la differenza di prezzo tra negozi e online si sente di più. Con il codice giusto confronti esattamente lo stesso modello e lo stesso colore.</p>[[VIDEO]]
<h2>Il codice giusto per le sneakers</h2><ol><li><b>Scatola:</b> inquadra il codice a barre sull'etichetta laterale.</li><li><b>Senza scatola:</b> apri la linguetta, c'è un'etichetta con il <b>codice modello</b> (es. Nike CW2288-111). Usa “Leggi l'etichetta”.</li><li><b>Colore:</b> le ultime cifre del codice indicano il colore, così non confronti un'altra versione.</li></ol>
<h2>Modelli più cercati</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=SNK, faq=[('Il codice nella linguetta basta?', 'Sì, il codice modello identifica modello e colore. La taglia la scegli poi su Amazon.'), ('E se trovo il modello a meno in negozio?', 'Allora compralo lì: l’app serve a farti scegliere sapendo il prezzo.')]),
 'en': dict(slug='/en/fashion/sneakers/', title='Sneakers: store price or Amazon? Nike, Adidas, New Balance and more',
   desc='Before buying sneakers in a store, scan the box or read the code inside the tongue and compare the price on Amazon. Free.',
   h1='Sneakers: <em>the right price in a flash</em>',
   body='''<p class="lead">Sneakers are one of the purchases where the gap between store and online prices shows the most. With the right code you compare exactly the same model and colourway.</p>[[VIDEO]]
<h2>The right code for sneakers</h2><ol><li><b>Box:</b> scan the barcode on the side label.</li><li><b>No box:</b> open the tongue, there is a label with the <b>style code</b> (e.g. Nike CW2288-111). Use “Read the label”.</li><li><b>Colour:</b> the last digits of the code are the colourway, so you don't compare a different version.</li></ol>
<h2>Most searched models</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=SNK, faq=[('Is the code inside the tongue enough?', 'Yes, the style code identifies model and colourway. You pick the size on Amazon.'), ('What if the store is cheaper?', 'Then buy it there: the app is there so you choose knowing the price.')]),
 'es': dict(slug='/es/moda/zapatillas/', title='Zapatillas: ¿precio en tienda o en Amazon? Nike, Adidas, New Balance y más',
   desc='Antes de comprar zapatillas en tienda, escanea la caja o lee el código de la lengüeta y compara el precio en Amazon. Gratis.',
   h1='Zapatillas: <em>el precio justo al instante</em>',
   body='''<p class="lead">Las zapatillas son de las compras donde más se nota la diferencia entre tienda y online. Con el código correcto comparas exactamente el mismo modelo y color.</p>[[VIDEO]]
<h2>El código correcto</h2><ol><li><b>Caja:</b> enfoca el código de barras de la etiqueta lateral.</li><li><b>Sin caja:</b> abre la lengüeta, hay una etiqueta con el <b>código de modelo</b> (p. ej. Nike CW2288-111). Usa “Leer la etiqueta”.</li><li><b>Color:</b> las últimas cifras indican el color, así no comparas otra versión.</li></ol>
<h2>Modelos más buscados</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=SNK, faq=[('¿Basta con el código de la lengüeta?', 'Sí, el código de modelo identifica modelo y color. La talla la eliges en Amazon.'), ('¿Y si en la tienda es más barato?', 'Entonces cómpralo allí: la app sirve para decidir sabiendo el precio.')]),
 'fr': dict(slug='/fr/mode/baskets/', title='Baskets : prix en magasin ou sur Amazon ? Nike, Adidas, New Balance et autres',
   desc='Avant d’acheter des baskets en magasin, scanne la boîte ou lis la référence dans la languette et compare le prix sur Amazon. Gratuit.',
   h1='Baskets : <em>le bon prix en un éclair</em>',
   body='''<p class="lead">Les baskets font partie des achats où l’écart entre magasin et en ligne se voit le plus. Avec la bonne référence, tu compares exactement le même modèle et le même coloris.</p>[[VIDEO]]
<h2>La bonne référence</h2><ol><li><b>Boîte :</b> vise le code-barres de l’étiquette latérale.</li><li><b>Sans boîte :</b> ouvre la languette, une étiquette porte la <b>référence du modèle</b> (ex. Nike CW2288-111). Utilise « Lire l’étiquette ».</li><li><b>Coloris :</b> les derniers chiffres indiquent le coloris, pour ne pas comparer une autre version.</li></ol>
<h2>Modèles les plus recherchés</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=SNK, faq=[('La référence de la languette suffit ?', 'Oui, elle identifie modèle et coloris. La pointure se choisit sur Amazon.'), ('Et si le magasin est moins cher ?', 'Alors achète là : l’appli sert à choisir en connaissant le prix.')]),
 'de': dict(slug='/de/mode/sneaker/', title='Sneaker: Ladenpreis oder Amazon? Nike, Adidas, New Balance und mehr',
   desc='Bevor du Sneaker im Laden kaufst: Karton scannen oder Artikelnummer in der Zunge lesen und den Preis bei Amazon vergleichen. Kostenlos.',
   h1='Sneaker: <em>der richtige Preis im Nu</em>',
   body='''<p class="lead">Bei Sneakern ist der Preisunterschied zwischen Laden und online oft besonders groß. Mit der richtigen Nummer vergleichst du genau dasselbe Modell in derselben Farbe.</p>[[VIDEO]]
<h2>Die richtige Nummer</h2><ol><li><b>Karton:</b> Barcode auf dem seitlichen Etikett scannen.</li><li><b>Ohne Karton:</b> In der Zunge steht die <b>Artikelnummer</b> (z. B. Nike CW2288-111). „Etikett lesen“ nutzen.</li><li><b>Farbe:</b> Die letzten Ziffern stehen für die Farbe, so vergleichst du keine andere Version.</li></ol>
<h2>Meistgesuchte Modelle</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=SNK, faq=[('Reicht die Nummer in der Zunge?', 'Ja, die Artikelnummer bestimmt Modell und Farbe. Die Größe wählst du bei Amazon.'), ('Und wenn der Laden günstiger ist?', 'Dann kauf dort: Die App hilft dir, mit dem Preis im Kopf zu entscheiden.')]),
 'pt': dict(slug='/pt/moda/sapatilhas/', title='Sapatilhas: preço na loja ou na Amazon? Nike, Adidas, New Balance e mais',
   desc='Antes de comprar sapatilhas na loja, lê a caixa ou o código na lingueta e compara o preço na Amazon. Grátis.',
   h1='Sapatilhas: <em>o preço certo num instante</em>',
   body='''<p class="lead">As sapatilhas são das compras onde mais se nota a diferença entre loja e online. Com o código certo comparas exatamente o mesmo modelo e a mesma cor.</p>[[VIDEO]]
<h2>O código certo</h2><ol><li><b>Caixa:</b> aponta para o código de barras da etiqueta lateral.</li><li><b>Sem caixa:</b> abre a lingueta, há uma etiqueta com o <b>código do modelo</b> (ex. Nike CW2288-111). Usa “Ler a etiqueta”.</li><li><b>Cor:</b> os últimos dígitos indicam a cor, assim não comparas outra versão.</li></ol>
<h2>Modelos mais procurados</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=SNK, faq=[('O código da lingueta chega?', 'Sim, identifica modelo e cor. O tamanho escolhes na Amazon.'), ('E se na loja for mais barato?', 'Então compra lá: a app serve para decidires sabendo o preço.')]),
}
JK = ['The North Face Nuptse', 'Columbia', 'Napapijri', 'Helly Hansen', 'Geox', 'Superdry', 'Jack & Jones', 'Tommy Hilfiger', 'Carhartt']
N['giubbotti'] = {
 'it': dict(slug='/moda/giubbotti/', title='Giubbotti e piumini: conviene il negozio o Amazon? Confronta in 5 secondi',
   desc='Giubbotti invernali e piumini: scansiona il cartellino in negozio e confronta il prezzo con Amazon prima di comprare. Gratis.',
   h1='Giubbotti e piumini: <em>negozio o Amazon?</em>',
   body='''<p class="lead">Un giubbotto invernale è una spesa importante: confrontare il prezzo prima di comprarlo vale qualche secondo, soprattutto tra novembre e i saldi di gennaio.</p>[[VIDEO]]
<h2>Come confrontare</h2><ol><li>Inquadra il codice a barre sul <b>cartellino del prezzo</b>.</li><li>Nessun cartellino? Usa “Leggi l'etichetta” sull'etichetta interna con marca e modello.</li><li>Scrivi il prezzo del negozio: l'app tiene il conto di quanto risparmi.</li></ol>
<h2>Marche più cercate</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=JK, faq=[('Quando costano meno i giubbotti?', 'Spesso con il Black Friday (27 novembre 2026) e con i saldi di gennaio: confronta prima di comprare.'), ('Posso cercare solo per marca?', 'Sì, tocca una marca qui sopra: l’app apre le offerte su Amazon.')]),
 'en': dict(slug='/en/fashion/jackets/', title='Winter jackets and puffers: store or Amazon? Compare in 5 seconds',
   desc='Winter jackets and puffer coats: scan the price tag in the store and compare the price with Amazon before you buy. Free.',
   h1='Winter jackets: <em>store or Amazon?</em>',
   body='''<p class="lead">A winter jacket is a big purchase: comparing the price first is worth a few seconds, especially between November and the January sales.</p>[[VIDEO]]
<h2>How to compare</h2><ol><li>Scan the barcode on the <b>price tag</b>.</li><li>No tag? Use “Read the label” on the inside label with brand and model.</li><li>Type the store price: the app keeps count of what you save.</li></ol>
<h2>Most searched brands</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=JK, faq=[('When are jackets cheapest?', 'Often around Black Friday (27 November 2026) and the January sales: compare before you buy.'), ('Can I search by brand only?', 'Yes, tap a brand above: the app opens the offers on Amazon.')]),
 'es': dict(slug='/es/moda/chaquetas/', title='Chaquetas y plumíferos: ¿tienda o Amazon? Compara en 5 segundos',
   desc='Chaquetas de invierno y plumíferos: escanea la etiqueta en la tienda y compara el precio con Amazon antes de comprar. Gratis.',
   h1='Chaquetas de invierno: <em>¿tienda o Amazon?</em>',
   body='''<p class="lead">Una chaqueta de invierno es un gasto importante: comparar el precio antes vale unos segundos, sobre todo entre noviembre y las rebajas de enero.</p>[[VIDEO]]
<h2>Cómo comparar</h2><ol><li>Enfoca el código de barras de la <b>etiqueta del precio</b>.</li><li>¿Sin etiqueta? Usa “Leer la etiqueta” en la etiqueta interior con marca y modelo.</li><li>Escribe el precio de la tienda: la app lleva la cuenta de lo que ahorras.</li></ol>
<h2>Marcas más buscadas</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=JK, faq=[('¿Cuándo cuestan menos las chaquetas?', 'A menudo en Black Friday (27 de noviembre de 2026) y en las rebajas de enero: compara antes de comprar.'), ('¿Puedo buscar solo por marca?', 'Sí, toca una marca arriba: la app abre las ofertas en Amazon.')]),
 'fr': dict(slug='/fr/mode/doudounes/', title='Doudounes et vestes d’hiver : magasin ou Amazon ? Compare en 5 secondes',
   desc='Vestes d’hiver et doudounes : scanne l’étiquette en magasin et compare le prix avec Amazon avant d’acheter. Gratuit.',
   h1='Vestes d’hiver : <em>magasin ou Amazon ?</em>',
   body='''<p class="lead">Une veste d’hiver est un gros achat : comparer le prix avant vaut quelques secondes, surtout entre novembre et les soldes de janvier.</p>[[VIDEO]]
<h2>Comment comparer</h2><ol><li>Vise le code-barres de l’<b>étiquette de prix</b>.</li><li>Pas d’étiquette ? Utilise « Lire l’étiquette » sur l’étiquette intérieure avec marque et modèle.</li><li>Tape le prix du magasin : l’appli compte ce que tu économises.</li></ol>
<h2>Marques les plus recherchées</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=JK, faq=[('Quand les vestes coûtent-elles moins ?', 'Souvent au Black Friday (27 novembre 2026) et aux soldes de janvier : compare avant d’acheter.'), ('Je peux chercher par marque ?', 'Oui, touche une marque ci-dessus : l’appli ouvre les offres Amazon.')]),
 'de': dict(slug='/de/mode/winterjacken/', title='Winterjacken und Daunenjacken: Laden oder Amazon? In 5 Sekunden vergleichen',
   desc='Winterjacken und Daunenjacken: Preisschild im Laden scannen und den Preis vor dem Kauf mit Amazon vergleichen. Kostenlos.',
   h1='Winterjacken: <em>Laden oder Amazon?</em>',
   body='''<p class="lead">Eine Winterjacke ist eine größere Ausgabe: Der Preisvergleich vorher lohnt die paar Sekunden, besonders zwischen November und dem Winterschlussverkauf.</p>[[VIDEO]]
<h2>So vergleichst du</h2><ol><li>Barcode auf dem <b>Preisschild</b> scannen.</li><li>Kein Preisschild? „Etikett lesen“ auf dem Innenetikett mit Marke und Modell nutzen.</li><li>Ladenpreis eintippen: Die App zählt mit, wie viel du sparst.</li></ol>
<h2>Meistgesuchte Marken</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=JK, faq=[('Wann sind Jacken am günstigsten?', 'Oft rund um Black Friday (27. November 2026) und im Winterschlussverkauf: vor dem Kauf vergleichen.'), ('Kann ich nur nach Marke suchen?', 'Ja, tippe oben auf eine Marke: Die App öffnet die Angebote bei Amazon.')]),
 'pt': dict(slug='/pt/moda/casacos/', title='Casacos de inverno e kispos: loja ou Amazon? Compara em 5 segundos',
   desc='Casacos de inverno e acolchoados: lê a etiqueta na loja e compara o preço com a Amazon antes de comprar. Grátis.',
   h1='Casacos de inverno: <em>loja ou Amazon?</em>',
   body='''<p class="lead">Um casaco de inverno é uma compra importante: comparar o preço antes vale uns segundos, sobretudo entre novembro e os saldos de janeiro.</p>[[VIDEO]]
<h2>Como comparar</h2><ol><li>Aponta para o código de barras da <b>etiqueta do preço</b>.</li><li>Sem etiqueta? Usa “Ler a etiqueta” na etiqueta interior com marca e modelo.</li><li>Escreve o preço da loja: a app faz a conta do que poupas.</li></ol>
<h2>Marcas mais procuradas</h2><p>[[TRY]]</p>[[CHIPS]]''',
   chips=JK, faq=[('Quando são mais baratos os casacos?', 'Muitas vezes na Black Friday (27 de novembro de 2026) e nos saldos de janeiro: compara antes de comprar.'), ('Posso pesquisar só pela marca?', 'Sim, toca numa marca acima: a app abre as ofertas na Amazon.')]),
}
HUB = 'moda'
ORDER = ['moda', 'sneakers', 'giubbotti']

CHIP_CSS = '.chips{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}.chips a{display:inline-block;border:1.5px solid #2B2F27;background:#171914;color:#fff;text-decoration:none;border-radius:99px;padding:9px 14px;font-weight:700;font-size:15px}.chips a:hover{border-color:#D4FF4A}'

def alts(key):
    m = {lg: N[key][lg]['slug'] for lg in LANGS}
    return ''.join(f'<link rel="alternate" hreflang="{lg}" href="{BASE}{u}">' for lg, u in m.items()) + f'<link rel="alternate" hreflang="x-default" href="{BASE}{m["en"]}">', m

def render(key, lg):
    D, U = N[key][lg], UI[lg]; a, m = alts(key)
    vfile = f'/media/BoomFlashnBuy-{lg}-orizzontale.mp4'
    vid = f'<video class="bfb" controls playsinline preload="metadata" poster="{S.POSTER}"><source src="{vfile}" type="video/mp4"></video>' + I.VIDEO_JS
    chips = '<div class="chips">' + ''.join(f'<a href="/?q={urllib.parse.quote(c)}&amp;lang={lg}">{html.escape(c)}</a>' for c in D['chips']) + '</div>'
    body = D['body'].replace('[[VIDEO]]', vid).replace('[[CHIPS]]', chips).replace('[[TRY]]', U['try_'])
    vld = dict(S.VIDEO_LD, name=D['title'], description=D['desc'], contentUrl=BASE + vfile, embedUrl=BASE + D['slug'], inLanguage=lg)
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "BoomFlashnBuy", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": html.unescape(N[HUB][lg]['h1'].split('<em>')[0].strip(' :')), "item": BASE + N[HUB][lg]['slug']}]
        + ([{"@type": "ListItem", "position": 3, "name": D['title'].split(':')[0], "item": BASE + D['slug']}] if key != HUB else [])}
    lds = [dict(S.APP_LD, url=f'{BASE}/?lang={lg}'), vld, S.faq_ld(D['faq']), crumbs]
    fq = ''.join(f'<details><summary>{q}</summary><p>{x}</p></details>' for q, x in D['faq'])
    more = ''.join(f'<a href="{N[k][lg]["slug"]}">{N[k][lg]["title"]} →</a>' for k in ORDER if k != key) + f'<a href="{U["allu"]}">{U["all"]} →</a>'
    return f'''<!doctype html><html lang="{lg}"><head><meta charset="utf-8">{ROBOTS}<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(D['title'])}</title><meta name="description" content="{html.escape(D['desc'])}"><link rel="canonical" href="{BASE}{D['slug']}">{a}
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(D['title'])}"><meta property="og:description" content="{html.escape(D['desc'])}"><meta property="og:url" content="{BASE}{D['slug']}"><meta property="og:image" content="{BASE}{S.OG}"><meta property="og:locale" content="{LOC[lg]}">
<meta property="og:video" content="{BASE}{vfile}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icons/favicon-48.png"><link rel="apple-touch-icon" href="/icons/apple-touch-icon.png"><meta name="theme-color" content="#0B0C0A">
<style>{S.CSS}{CHIP_CSS}</style>{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}</head>
<body><div class="w"><header><img src="/icons/icon-192.png" alt="" width="44" height="44"><a href="/?lang={lg}">Boom<em>Flash</em>nBuy</a></header>
<main>{I.langbar(m, lg)}<h1>{D['h1']}</h1>{body}
<div class="cta"><a class="btn" href="/?boom=1&amp;lang={lg}">{U['scan']}</a><a class="btn g" href="/?lang={lg}">{U['app']}</a></div>
<h2>{U['faq']}</h2>{fq}
<h2>{U['more']}</h2><nav class="more">{more}</nav></main>
<footer>{U['foot']} {U['legal']}<br>{U['upd']} {TODAY}.</footer></div>{CF}</body></html>'''

urls = []
for key in ORDER:
    for lg in LANGS:
        S.write(N[key][lg]['slug'].strip('/') + '/index.html', render(key, lg)); urls.append((key, lg))

# link al settore Moda dalle pagine indice di ogni lingua
IDX = {'it': '/guide/', 'en': '/en/', 'es': '/es/', 'fr': '/fr/', 'de': '/de/', 'pt': '/pt/'}
for lg, u in IDX.items():
    p = os.path.join(ROOT, u.strip('/'), 'index.html'); s = open(p, encoding='utf-8').read()
    link = f'<a href="{N[HUB][lg]["slug"]}">{N[HUB][lg]["title"]} →</a>'
    if N[HUB][lg]['slug'] not in s and '<nav class="more">' in s:
        s = s.replace('<nav class="more">', '<nav class="more">' + link, 1); open(p, 'w', encoding='utf-8').write(s)

# sitemap
sp = os.path.join(ROOT, 'sitemap.xml'); sm = open(sp, encoding='utf-8').read()
def vt(key, lg):
    D = N[key][lg]
    return (f'<video:video><video:thumbnail_loc>{BASE}{S.POSTER}</video:thumbnail_loc><video:title>{html.escape(D["title"])}</video:title>'
            f'<video:description>{html.escape(D["desc"])}</video:description><video:content_loc>{BASE}/media/BoomFlashnBuy-{lg}-orizzontale.mp4</video:content_loc><video:duration>64</video:duration></video:video>')
add = ''.join(f'<url><loc>{BASE}{N[k][lg]["slug"]}</loc><lastmod>{TODAY}</lastmod>{vt(k, lg)}</url>\n' for k, lg in urls if f'{BASE}{N[k][lg]["slug"]}<' not in sm)
open(sp, 'w', encoding='utf-8').write(sm.replace('</urlset>', add + '</urlset>'))
print('nicchie:', len(urls), 'pagine')
