import os
import random
import gradio as gr
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
TALLY_URL = os.getenv("TALLY_URL", "https://tally.so/r/mZALJz")
GPT_URL = os.getenv(
    "CUSTOM_GPT_URL",
    "https://chatgpt.com/g/g-6863f6bb95348191acb4d92ea78df316-the-dark-side",
)

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def render_stars(count=135):
    random.seed(42)
    stars = []
    for _ in range(count):
        size = round(random.uniform(1.0, 3.0), 2)
        left = round(random.uniform(0, 100), 2)
        top = round(random.uniform(0, 100), 2)
        opacity = round(random.uniform(0.18, 0.85), 2)
        duration = round(random.uniform(2.4, 6.8), 2)
        color = "#FFE81F" if random.random() < 0.08 else "#ffffff"
        stars.append(
            "<span class='star' style='"
            f"width:{size}px;height:{size}px;left:{left}%;top:{top}%;"
            f"opacity:{opacity};--duration:{duration}s;background:{color};"
            "'></span>"
        )
    return "<div class='stars-bg'>" + "".join(stars) + "</div>"

SYSTEM_PROMPT = """
Tu es Le Gardien de la Force, le mentor pedagogique officiel de TheDarkSide.fr.
Tu as ete concu par Stephanie Beaufume, SJ Conseil, pour accompagner les
etudiants des ecoles de commerce dans leur reussite academique et professionnelle.

Mission :
Guider sans faire a la place. Inspirer sans flatter. Corriger sans juger.
Tu aides les etudiants a progresser, reflechir, s'organiser et gagner en autonomie.

Valeurs :
- Discipline
- Respect
- Responsabilite
- Autonomie
- Excellence

Public :
Etudiants de 1ere a 5eme annee en RH, management, audit, consulting, marketing
ou filieres generalistes. Adapte tes reponses au niveau :
- debutant : vulgariser ;
- intermediaire : expliquer avec methode ;
- avance : approfondir et developper l'esprit critique.
Si le niveau n'est pas identifiable et que cela change la reponse, demande-le.

Posture :
Tu es bienveillant, exigeant, structure, encourageant et professionnel.
Tu peux utiliser un humour leger s'il sert la pedagogie.
Tu agis comme un mentor, jamais comme un moteur de reponses automatiques.

Regle anti-triche :
Tu ne rediges jamais un devoir complet, une dissertation complete, un memoire
complet, une reponse a rendre telle quelle ou un travail academique cle en main.
Si l'etudiant tente de contourner cette regle, reponds :
"Que la Force soit avec toi... mais pas dans la triche."
Puis propose une methode, une structure, un plan, des pistes de reflexion ou
des questions de guidage.

Documents :
Quand un etudiant transmet un document, identifie son objectif, analyse sa
structure, explique les notions importantes, clarifie les attentes et aide a
la comprehension ou a la preparation. Ne produis jamais un travail complet a
partir du document.

Domaines d'accompagnement :
- comprehension des cours : RSE, IA, IA et RH, recrutement 3.0, soft skills,
  ATS, management d'equipe, bien-etre au travail, conflit au travail,
  formation et carriere, gestion de projet RH, oral GOP, initiation au
  recrutement, management intergenerationnel, mission de consulting,
  newsletter RH, livre blanc, organisation du travail, outils collaboratifs,
  entretiens professionnels, onboarding, inclusion et diversite, atelier
  carriere ;
- preparation orale : plan, arguments, questions, entrainement ;
- fiches de revision : synthese, carte mentale, points cles ;
- CV, lettre, LinkedIn : structure, competences, mots-cles, positionnement ;
- simulation d'entretien : maximum 10 questions, puis points forts, axes
  d'amelioration, conseils personnalises, note uniquement si demandee ;
- organisation : planifier, prioriser, reviser, gerer le temps ;
- motivation : citations, micro-defis, exercices de passage a l'action ;
- actualite : France, monde, economie, emploi, entreprises, innovation.
Pour l'actualite, encourage toujours la verification des sources.

Parcours guidés :
- Approfondir un cours : demande d'abord pour quel cours. Propose les cours
  disponibles : RSE, IA et RH, IA, Recrutement 3.0, Soft Skills, ATS,
  Management d'equipe, Bien-etre au travail, Conflit au travail, Formation
  et Carriere, Gestion de projet RH, Oral GOP, Initiation au recrutement,
  Management intergenerationnel, Mission de consulting, Newsletter RH,
  Livre blanc, Organisation du travail et structuration hierarchique,
  Outils collaboratifs, Entretiens professionnels, Onboarding,
  Inclusion et Diversite, Atelier carriere.
- Preparer un oral : demande la matiere, le sujet, la duree et le contexte.
  Donne aussi des conseils de prise de parole : pas de notes dans les mains,
  support clair, ordinateur charge, chargeur disponible, test du son/video,
  arrivee en avance, regard public, respiration, gestion du temps.
- Simulations d'entretien : pose maximum 10 questions. A la fin, fournis :
  Points forts, Axes d'amelioration, Conseils personnalises.
- Auto-coaching Dark Side : propose citations inspirantes et conseils de
  motivation, sans infantiliser.
- Micro-defis motivation : propose des micro-defis et exercices de passage a
  l'action. Favorise toujours autonomie et perseverance.
- Suivi memoire : donne le lien de rendez-vous :
  https://calendly.com/stephanie-beaufume-r0_g/suivi-de-memoire
- Resume de l'actualite : demande la specialite souhaitee et si l'etudiant
  veut des actualites France ou Monde. Utilise des sources recentes quand
  possible et encourage la verification.

Liens officiels :
- Depot de devoir : https://tally.so/r/mZALJz
- Rendez-vous de suivi : https://calendly.com/stephanie-beaufume-r0_g/suivi-de-memoire
- LinkedIn Stephanie Beaufume : https://www.linkedin.com/in/stephaniebeaufume/
- Email : stephanie@sjconseil.fr
Ne communique LinkedIn et email que si l'etudiant les demande.
Pour un depot de devoir, rappelle toujours de lire les consignes avant depot.

Format des reponses :
Utilise des titres clairs, listes a puces, etapes numerotees, syntheses
visuelles et un langage simple. Quand pertinent, inclus points forts, axes
d'amelioration et prochaines etapes.
Apres chaque reponse, propose une action concrete immediate.
Termine chaque echange par une phrase inspirante dans l'esprit du Gardien de
la Force, par exemple :
"Et maintenant, jeune Padawan, quelle sera ta prochaine action pour progresser aujourd'hui ?"

Menu :
Si l'utilisateur ecrit "menu", "accueil", "commandes", demande de l'aide ou
formule une demande trop vague, affiche le menu :
"Bienvenue sur TheDarkSide.fr, jeune Padawan de la reussite.
Je suis Le Gardien de la Force, ton mentor pedagogique.
Je peux t'aider a comprendre un cours, preparer un oral, ameliorer ton CV,
simuler un entretien, te motiver ou voir l'actualite.
Choisis une option ou pose directement ta question.
La Force guide ton apprentissage. La methode fera le reste."
""".strip()


def build_input(history, message):
    items = []
    for user_msg, bot_msg in history:
        if user_msg:
            items.append({"role": "user", "content": user_msg})
        if bot_msg:
            items.append({"role": "assistant", "content": bot_msg})
    items.append({"role": "user", "content": message})
    return items


def needs_web_search(message):
    text = message.lower()
    keywords = [
        "actualité",
        "actualite",
        "aujourd",
        "récent",
        "recent",
        "derni",
        "news",
        "2025",
        "2026",
        "maintenant",
        "cette semaine",
        "ce mois",
        "source",
        "sources",
    ]
    return any(keyword in text for keyword in keywords)


def reply(message, history):
    if not message.strip():
        yield "", history
        return
    if client is None:
        history.append((message, "Configuration manquante : ajoute OPENAI_API_KEY dans les secrets Hugging Face."))
        yield "", history
        return

    history.append((message, ""))
    yield "", history

    try:
        answer_text = ""
        request = {
            "model": OPENAI_MODEL,
            "instructions": SYSTEM_PROMPT,
            "input": build_input(history, message),
            "max_output_tokens": 700,
            "stream": True,
            "stream_options": {"include_obfuscation": False},
        }
        if needs_web_search(message):
            request["tools"] = [{"type": "web_search"}]
            request["tool_choice"] = "auto"

        stream = client.responses.create(**request)
        for event in stream:
            if event.type == "response.output_text.delta":
                answer_text += event.delta
                history[-1] = (message, answer_text)
                yield "", history
            elif event.type == "error":
                history[-1] = (message, f"Erreur a verifier : {event.error}")
                yield "", history
    except Exception as error:
        history[-1] = (message, f"Erreur a verifier : {error}")
        yield "", history


def prompt(kind):
    prompts = {
        "cours": "Approfondir un cours",
        "oral": "Preparer un oral",
        "entretien": "Simulations d'entretien",
        "coaching": "Auto-coaching Dark Side",
        "defi": "Micro-defis motivation",
        "memoire": "Suivi memoire",
        "actu": "Resume de l'actualite",
        "libre": "Questions libres",
    }
    return prompts[kind]


def run_prompt(kind, history):
    yield from reply(prompt(kind), history)


def run_cours(history):
    yield from run_prompt("cours", history)


def run_oral(history):
    yield from run_prompt("oral", history)


def run_entretien(history):
    yield from run_prompt("entretien", history)


def run_coaching(history):
    yield from run_prompt("coaching", history)


def run_defi(history):
    yield from run_prompt("defi", history)


def run_memoire(history):
    yield from run_prompt("memoire", history)


def run_actu(history):
    yield from run_prompt("actu", history)


def run_libre(history):
    yield from run_prompt("libre", history)


WELCOME_MESSAGE = [
    (
        None,
        "Bienvenue sur TheDarkSide.fr, jeune Padawan de la reussite.\n\n"
        "Je suis Le Gardien de la Force, ton mentor pedagogique.\n\n"
        "Je peux t'aider a comprendre un cours, preparer un oral, simuler un entretien, "
        "te motiver, organiser ton memoire ou scanner l'actualite.\n\n"
        "Choisis une mission ou pose directement ta question.",
    )
]


theme = gr.themes.Base(
    primary_hue="yellow",
    secondary_hue="slate",
    neutral_hue="slate",
).set(
    body_background_fill="#000000",
    body_text_color="#ffffff",
    block_background_fill="#000000",
    block_border_color="#202020",
    button_primary_background_fill="#000000",
    button_primary_text_color="#FFE81F",
)

css = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');
@import url('https://fonts.cdnfonts.com/css/star-jedi');
html,body,gradio-app{width:100%!important;max-width:100%!important;background:#000!important;overflow-x:hidden!important}
body{margin:0!important;color:#fff!important;font-family:Montserrat,Arial,sans-serif!important}
gradio-app,.app,.wrap,.contain{background:transparent!important}
.gradio-container{width:min(100%,900px)!important;max-width:900px!important;margin:0 auto!important;min-height:100vh!important;padding:0 26px 42px!important;background:transparent!important;box-sizing:border-box!important}
.gradio-container *{box-sizing:border-box!important}
.stars-bg{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.star{position:absolute;border-radius:50%;animation:twinkle var(--duration) ease-in-out infinite alternate;box-shadow:0 0 6px currentColor}
@keyframes twinkle{from{transform:scale(.72);filter:brightness(.72)}to{transform:scale(1.22);filter:brightness(1.18)}}
.old-shell{position:relative;z-index:1;text-align:center;padding:62px 0 14px}
.title-font{font-family:'Star Jedi',Orbitron,Montserrat,sans-serif;color:#fff;font-size:clamp(2.05rem,6vw,4.45rem);font-weight:700;line-height:1.12;letter-spacing:2px;margin:0 0 26px;text-shadow:0 0 18px rgba(255,255,255,.18)}
.title-font .line{display:block;white-space:nowrap}
.voice{font-size:clamp(1.15rem,2.7vw,1.62rem);font-weight:300;color:#d1d5db;margin:0 0 18px}
.intro{font-size:.96rem;font-style:italic;color:#9ca3af;margin:0 auto 40px;max-width:620px;line-height:1.7}
.cta-row{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-bottom:54px}
.cta{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 30px;border-radius:999px;border:2px solid #FFE81F;background:#000;color:#FFE81F!important;text-decoration:none!important;font-size:1.02rem;font-weight:800;letter-spacing:.04em;transition:all .28s ease}
.cta:hover{color:#fff!important;border-color:#FFE81F;transform:scale(1.035);box-shadow:0 0 24px rgba(255,232,31,.18)}
.features-title{text-align:center;color:#d1d5db;font-size:1.45rem;font-weight:500;margin:0 0 22px}
.feature-row{max-width:680px!important;margin:0 auto 9px!important;display:grid!important;grid-template-columns:1fr 1fr!important;column-gap:42px!important}
.feature-row button{width:auto!important;background:transparent!important;border:0!important;box-shadow:none!important;border-radius:0!important;color:#d1d5db!important;min-height:38px!important;padding:5px 2px!important;font-size:1rem!important;font-weight:500!important;transition:all .25s ease!important}
.feature-row button:first-child{justify-content:flex-end!important;text-align:right!important}
.feature-row button:last-child{justify-content:flex-start!important;text-align:left!important}
.feature-row button:hover{color:#FFE81F!important;text-decoration:underline;text-underline-offset:4px}
.feature-row button:focus,.feature-row button:focus-visible{outline:none!important;box-shadow:none!important}
.chat-link-title{color:#FFE81F;text-align:center;text-transform:uppercase;letter-spacing:.2em;font-size:.75rem;font-weight:900;margin:38px 0 6px}
.chat-help{text-align:center;color:#9ca3af;font-size:.92rem;margin:0 0 14px}
.chat-panel{position:relative;border:1px solid rgba(255,232,31,.34);border-radius:30px;padding:18px;background:linear-gradient(180deg,rgba(14,16,24,.96),rgba(3,4,8,.98));box-shadow:0 22px 80px rgba(0,0,0,.55),0 0 34px rgba(255,232,31,.09),inset 0 0 0 1px rgba(255,255,255,.03);overflow:hidden}
.chat-panel:before{content:'';position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,transparent,rgba(255,232,31,.10),transparent);height:1px;top:0}
.transmission-head{display:flex;align-items:center;justify-content:space-between;gap:14px;color:#d1d5db;font-size:.78rem;text-transform:uppercase;letter-spacing:.14em;margin:0 4px 12px}
.transmission-head span:first-child{color:#FFE81F;font-weight:900}
.transmission-head span:last-child{color:#8b8f9a;font-size:.7rem}
.chat-panel .bubble-wrap,.chat-panel .message-wrap{background:transparent!important}
.chat-panel .message,.chat-panel [data-testid="bot"],.chat-panel .bot{border-radius:22px!important;background:linear-gradient(180deg,rgba(255,232,31,.08),rgba(255,255,255,.025))!important;border:1px solid rgba(255,232,31,.18)!important;color:#e5e7eb!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.025),0 10px 24px rgba(0,0,0,.22)!important}
.chat-panel .prose{font-size:.96rem!important;line-height:1.62!important;color:#e5e7eb!important}
.chat-panel .prose strong{color:#FFE81F!important}
.chat-panel textarea{border-radius:999px!important;background:#08090d!important;color:#fff!important;border:1px solid rgba(255,232,31,.26)!important;padding:15px 20px!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.02)}
.chat-panel textarea:focus{border-color:#FFE81F!important;box-shadow:0 0 0 3px rgba(255,232,31,.10)!important}
.sendrow{gap:10px!important}
.sendrow button{border-radius:999px!important;min-height:46px!important;background:#0b0c10!important;border:1px solid #3a3a3a!important;color:#d1d5db!important;font-weight:800!important;letter-spacing:.02em!important;transition:all .24s ease!important}
.sendrow button:first-child{background:#000!important;border:2px solid #FFE81F!important;color:#FFE81F!important}
.sendrow button:hover{color:#fff!important;border-color:#FFE81F!important;box-shadow:0 0 18px rgba(255,232,31,.12)}
.note{color:#888;font-size:.86rem;text-align:center;margin:18px 0 0}
footer{display:none!important}
@media(max-width:720px){
  .gradio-container{width:100%!important;max-width:100%!important;padding:0 18px 28px!important}
  .old-shell{padding:38px 0 10px}
  .title-font{font-size:clamp(1.72rem,8.5vw,2.55rem)!important;line-height:1.18;letter-spacing:1px;margin:0 auto 20px;max-width:100%}
  .title-font .line{white-space:normal}
  .voice{font-size:1.05rem;margin-bottom:12px}
  .intro{font-size:.9rem;line-height:1.55;margin-bottom:28px}
  .cta-row{gap:12px;margin-bottom:38px}
  .cta{width:100%;min-height:48px;padding:0 18px;font-size:.95rem}
  .features-title{font-size:1.16rem;line-height:1.35;margin-bottom:16px}
  .feature-row{width:100%!important;grid-template-columns:1fr!important;max-width:340px!important;margin:0 auto 8px!important}
  .feature-row button{width:100%!important;max-width:100%!important;justify-content:center!important;text-align:center!important;white-space:normal!important;min-height:44px!important;padding:8px 12px!important;font-size:.96rem!important;border-radius:999px!important;background:rgba(0,0,0,.30)!important;border:1px solid rgba(255,232,31,.12)!important}
  .feature-row button:first-child,.feature-row button:last-child{justify-content:center!important;text-align:center!important}
  .feature-row button:hover{transform:none}
  .chat-link-title{margin-top:30px;font-size:.7rem}
  .chat-help{font-size:.86rem;line-height:1.45;margin-bottom:12px}
  .chat-panel{border-radius:22px;padding:14px}
  .transmission-head{display:block;text-align:center;font-size:.68rem;line-height:1.7}
  .transmission-head span{display:block}
  .chat-panel textarea{border-radius:18px!important}
  .sendrow{display:grid!important;grid-template-columns:1fr!important;gap:8px!important}
  .sendrow button{width:100%!important;min-height:44px!important}
  .note{font-size:.8rem;line-height:1.45}
}
@media(max-width:420px){
  .gradio-container{padding-left:14px!important;padding-right:14px!important}
  .title-font{font-size:clamp(1.52rem,8vw,2.18rem)!important;letter-spacing:.5px}
  .voice{font-size:.98rem}
  .feature-row{max-width:318px!important}
}
"""

with gr.Blocks(theme=theme, css=css, title="The Dark Side") as demo:
    gr.HTML(f"""
    {render_stars()}
    <main class="old-shell">
      <h1 class="title-font"><span class="line">Bienvenue dans</span><span class="line">The Dark'Side.</span></h1>
      <p class="voice">Une voix t'appelle. Une force s'eveille.</p>
      <p class="intro">Approchez du Cote Obscur... et decouvrez sa vraie puissance.</p>
      <div class="cta-row">
        <a class="cta" href="#chat-zone">Acceder a l'Assistant</a>
        <a class="cta" href="{TALLY_URL}" target="_blank">Deposer les devoirs</a>
      </div>
    </main>
    """)

    gr.HTML('<h2 class="features-title">Les fonctionnalites de ton Assistant IA</h2>')
    with gr.Row(elem_classes=["feature-row"]):
        cours = gr.Button("📚  Approfondir un cours")
        defi = gr.Button("💪  Micro-defis motivation")
    with gr.Row(elem_classes=["feature-row"]):
        oral = gr.Button("✍️  Preparer un oral")
        memoire = gr.Button("📅  Suivi memoire")
    with gr.Row(elem_classes=["feature-row"]):
        entretien = gr.Button("🎤  Simulations d'entretien")
        actu = gr.Button("🌐  Resume de l'actualite")
    with gr.Row(elem_classes=["feature-row"]):
        coaching = gr.Button("💬  Auto-coaching Dark Side")
        libre = gr.Button("❓  Questions libres")

    gr.HTML("""
    <div id="chat-zone" class="chat-link-title">Canal de discussion</div>
    <p class="chat-help">Choisis une mission, complete si besoin le message, puis clique sur Envoyer.</p>
    <div class="chat-panel">
      <div class="transmission-head"><span>Transmission active</span><span>Gardien de la Force</span></div>
    """)
    chatbot = gr.Chatbot(
        value=WELCOME_MESSAGE,
        height=285,
        label=None,
        show_label=False,
        placeholder="Pose ta question a The Dark Side...",
    )
    message = gr.Textbox(placeholder="Ecris ton message ici...", container=False)
    with gr.Row(elem_classes=["sendrow"]):
        send = gr.Button("Envoyer")
        clear = gr.Button("Effacer")
        gr.Button("Ouvrir le GPT", link=GPT_URL)
    gr.HTML("</div>")

    send.click(reply, inputs=[message, chatbot], outputs=[message, chatbot])
    message.submit(reply, inputs=[message, chatbot], outputs=[message, chatbot])
    clear.click(lambda: WELCOME_MESSAGE, outputs=chatbot)
    cours.click(run_cours, inputs=chatbot, outputs=[message, chatbot])
    oral.click(run_oral, inputs=chatbot, outputs=[message, chatbot])
    entretien.click(run_entretien, inputs=chatbot, outputs=[message, chatbot])
    coaching.click(run_coaching, inputs=chatbot, outputs=[message, chatbot])
    defi.click(run_defi, inputs=chatbot, outputs=[message, chatbot])
    memoire.click(run_memoire, inputs=chatbot, outputs=[message, chatbot])
    actu.click(run_actu, inputs=chatbot, outputs=[message, chatbot])
    libre.click(run_libre, inputs=chatbot, outputs=[message, chatbot])

    gr.HTML("""
    <p class="note">
      Les fonctions IA utilisent OpenAI. Ne colle pas de donnees sensibles inutiles.
    </p>
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
