"""
inject_css.py — Collège Bobée
==============================
Injecte dans TOUS les fichiers .html :
  - Lien vers custom.css (design modernisé)
  - JS sticky nav + scroll reveal

Usage (dans le dossier du repo) :
  python inject_css.py
  git add -A
  git commit -m "Injection custom.css sur toutes les pages"
  git push
"""

import os, re

CSS_LINK = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="/custom.css">"""

JS_SNIPPET = """<script>
(function(){
  var h = document.getElementById('header');
  if(h) window.addEventListener('scroll', function(){
    h.classList.toggle('scrolled', window.scrollY > 8);
  }, {passive:true});
  var els = document.querySelectorAll('.views-row, .block-views, #block-coordonnees');
  if('IntersectionObserver' in window){
    els.forEach(function(el){ el.classList.add('cpb-reveal'); });
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('visible'); obs.unobserve(e.target); }
      });
    },{threshold:0.1, rootMargin:'0px 0px -30px 0px'});
    els.forEach(function(el){ obs.observe(el); });
  }
})();
</script>"""

MARKER = "custom.css"

def inject(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    if MARKER in content:
        return False
    # CSS dans <head>
    new_content, n = re.subn(r"(</head>)", CSS_LINK + "\n\1", content, count=1, flags=re.IGNORECASE)
    if n == 0:
        new_content = CSS_LINK + "\n" + content
    # JS avant </body>
    new_content = re.sub(r"(</body>)", JS_SNIPPET + "\n\1", new_content, count=1, flags=re.IGNORECASE)
    with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
        f.write(new_content)
    return True

modified = skipped = errors = 0
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".vercel"}]
    for filename in files:
        if not filename.lower().endswith((".html", ".htm")):
            continue
        path = os.path.join(root, filename)
        try:
            if inject(path):
                modified += 1
                if modified % 100 == 0:
                    print(f"  {modified} fichiers traités...")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"❌  {path} → {e}")

print(f"\n{'─'*40}")
print(f"✅ Modifiés  : {modified}")
print(f"⏭  Déjà OK  : {skipped}")
print(f"❌ Erreurs   : {errors}")
print(f"{'─'*40}")
print("\nMaintenant lance :")
print("  git add -A")
print("  git commit -m \"Injection custom.css sur toutes les pages\"")
print("  git push")
