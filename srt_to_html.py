from pathlib import Path
import srt
import json

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>

<head>
  <title>Normconf: {talk_title} Transcript</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description"
    content="Transcript of {talk_title} from Normconf" />
  <meta property="og:title" content="Normconf: {talk_title} Transcript" />
  <meta property="og:url" content="https://normconf.com" />
  <meta name="og:description"
    content="Transcript of {talk_title} from Normconf" />
  <meta property="og:image" content="https://normconf.com/images/normconf_banner_metadata_1000x500.png" />
  <meta property="og:type" content="website" />
  <meta name="twitter:image" content="https://normconf.com/images/normconf_banner_metadata_1000x500.png" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:site" content="normconf.com" />
  <meta name="twitter:creator" content="@normconf" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
  <link href="fontawesome/css/all.min.css" rel="stylesheet">
  <link rel="icon" type="image/x-icon" href="images/favicon.ico">
  <style>
    body {{
      background-image: url('images/background_placeholder.png');
    }}

    .hero {{
      background-color: None;
      color: #797979;
      font-family: sans-serif;
    }}

    .center {{
      display: block;
      margin-left: auto;
      margin-right: auto;
      width: 50%;
    }}

    a:link {{
      color: #4200be;
    }}

    a:visited {{
      color: #4200be;
    }}

    a:active {{
      color: #ef028c;
    }}

    a:hover {{
      color: #ef028c;
    }}

    a.light_link:link {{
      color: #ef028c;
    }}

    a.light_link:visited {{
      color: #4200be;
    }}

    a.dark_link:link {{
      color: #ef028c;
    }}

    a.dark_link:visited {{
      color: #ef028c;
    }}

    a.dark_link:active {{
      color: #5fffcf;
    }}

    a.dark_link:hover {{
      color: #5fffcf;
    }}

    a.on_pink:link {{
      color: #5fffcf;
    }}

    a.on_pink:active {{
      color: #6017af;
    }}

    a.on_pink:hover {{
      color: #4200be;
    }}

    .navbar.is-dark .navbar-end>a.navbar-item:hover {{
      background-color: #ef028c;
    }}

    .navbar.is-dark .navbar-item {{
      white-space: normal;
    }}

    .navbar.is-dark .navbar-item.has-dropdown:hover .navbar-link {{
      background-color: #ef028c;
    }}

    .navbar.is-dark .navbar-brand>a.navbar-item:hover {{
      background-color: #6017af;
    }}

    .button.is-danger {{
      background-color: #ef028c;
    }}

    .button.is-primary {{
      background-color: #5fffcf;
      color: #4200be;
    }}

    table.speakers1 {{
      font-weight: bold;
      color: #4200be;
      width: auto;
    }}

    table.speakers2 {{
      font-weight: bold;
      color: #6017af;
      width: auto;
    }}

    table.schedule {{
      font-weight: bold;
      /* width: auto; */
    }}

    table.schedule td {{
      text-align: center;
      padding: 0.5em;
      max-width: 30em;
      /* word-wrap: break-word; */
    }}

    table.schedule tr:nth-child(odd) {{
      color: #4200be;
      background-color: #00000017;
    }}

    table.schedule tr:nth-child(even) {{
      color: #6017af;
    }}

    .message.is-primary .message-header {{
      background-color: #5fffcf;
      color: #4200be;
    }}
  </style>
  </head>
  <body>
  <section class="section" style="background-color: #6017af;">
    <div class="container">
    <div class="box">
      <h1 class="title">
        {talk_title}
      </h1>
      <p class="subtitle">
        Transcript generated with <a href='https://github.com/openai/whisper'>OpenAI Whisper</a> <code>large-v2</code>.
      </p>
      </div>
      <div class="box">
        {stuff}
      </p>
    </div>
  </section>
  </body>
</html>"""

paths = Path("data/").glob("**/*.srt")

YT_TEMPLATE = '<a href="https://www.youtube.com/watch?v={id}&t={seconds}">{content} </a>'
for p in paths:
    data = srt.parse(p.read_text())
    info = json.loads(Path(p.parent / "info.json").read_text())
    link = info['id']
    talk_title = info['title']
    print(link, talk_title)
    html = ""
    for sub in data:
        html += YT_TEMPLATE.format(id=link, seconds=sub.start.seconds, content=sub.content)
    (p.parent / "transcript.html").write_text(BASE_TEMPLATE.format(stuff=html, talk_title=talk_title))