from jinja2 import Template
import os

def generate_report(articles, word_freq=None, metadata=None):

    html="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>El Pais Scraper Report</title>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: Arial, sans-serif; max-width: 960px; margin: 40px auto; background: #f0f2f5; color: #333; padding: 0 20px; }

            h1 { text-align: center; color: #1a1a2e; font-size: 1.8em; padding: 20px 0 10px; border-bottom: 3px solid #e94560; margin-bottom: 24px; }

            /* Metadata */
            .metadata { background: #1a1a2e; color: #ccc; border-radius: 8px; padding: 20px 24px; margin-bottom: 28px; }
            .metadata h2 { color: #e94560; font-size: 1em; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
            .meta-row { display: flex; justify-content: space-between; font-size: 0.88em; padding: 4px 0; border-bottom: 1px solid #2e2e4e; }
            .meta-row:last-child { border-bottom: none; }
            .meta-key { color: #aaa; }
            .meta-val { color: #fff; font-weight: bold; }

            /* Articles */
            .article { background: white; border-radius: 8px; padding: 24px; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.07); border-left: 4px solid #e94560; }
            .article-number { font-size: 0.75em; font-weight: bold; color: #e94560; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
            .label { font-size: 0.7em; font-weight: bold; text-transform: uppercase; color: #999; letter-spacing: 1px; margin: 10px 0 3px; }
            .spanish-title { font-size: 1.25em; font-weight: bold; color: #1a1a2e; }
            .english-title { font-size: 1.1em; font-weight: bold; color: #e94560; background: #fff5f7; padding: 6px 10px; border-radius: 4px; display: inline-block; }
            .content { font-size: 0.92em; line-height: 1.75; color: #555; }

            /* Word Frequency */
            .section { background: white; border-radius: 8px; padding: 24px; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }
            .section h2 { color: #1a1a2e; font-size: 1.05em; margin-bottom: 14px; border-bottom: 2px solid #f0f2f5; padding-bottom: 8px; }
            .freq-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0f2f5; }
            .freq-word { font-weight: bold; color: #1a1a2e; }
            .freq-count { background: #e94560; color: white; border-radius: 12px; padding: 2px 10px; font-size: 0.85em; font-weight: bold; }
            .no-freq { color: #999; font-style: italic; font-size: 0.9em; }

            /* Screenshots */
            .screenshots { background: white; border-radius: 8px; padding: 24px; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }
            .screenshots h2 { color: #1a1a2e; font-size: 1.05em; margin-bottom: 14px; border-bottom: 2px solid #f0f2f5; padding-bottom: 8px; }
            .screenshot-placeholder { background: #f8f9ff; border: 2px dashed #ccd; border-radius: 6px; padding: 30px; text-align: center; color: #aaa; font-size: 0.9em; }
        </style>
    </head>
    <body>

    <h1>El País — Opinion Section Report</h1>

    {% if metadata %}
    <div class="metadata">
        <h2>Test Execution Report</h2>
        <div class="meta-row"><span class="meta-key">Website</span><span class="meta-val">{{ metadata.website }}</span></div>
        <div class="meta-row"><span class="meta-key">Framework</span><span class="meta-val">{{ metadata.framework }}</span></div>
        <div class="meta-row"><span class="meta-key">Articles Extracted</span><span class="meta-val">{{ metadata.articles_extracted }}</span></div>
        <div class="meta-row"><span class="meta-key">Translation</span><span class="meta-val">{{ metadata.translation }}</span></div>
        <div class="meta-row"><span class="meta-key">Execution Time</span><span class="meta-val">{{ metadata.execution_time }}</span></div>
    </div>
    {% endif %}

    {% for a in articles %}
    <div class="article">
        <div class="article-number">Article {{ loop.index }} of {{ articles|length }}</div>

        <div class="label">Spanish Title</div>
        <p class="spanish-title">{{ a.spanish_title }}</p>

        <div class="label">English Translation</div>
        <span class="english-title">{{ a.english_title }}</span>

        <div class="label">Content</div>
        <p class="content">{{ a.content }}</p>
    </div>
    {% endfor %}

    <div class="section">
        <h2>Repeated Words (More than 2 occurrences)</h2>
        {% if word_freq %}
            {% for word, count in word_freq.items() %}
            <div class="freq-row">
                <span class="freq-word">{{ word }}</span>
                <span class="freq-count">{{ count }}</span>
            </div>
            {% endfor %}
        {% else %}
            <p class="no-freq">No words repeated more than 2 occurrences.</p>
        {% endif %}
    </div>

    </body>
    </html>
    """

    template = Template(html)
    output = template.render(articles=articles, word_freq=word_freq, metadata=metadata)

    os.makedirs("output", exist_ok=True)
    with open("output/report.html","w",encoding="utf-8") as f:
        f.write(output)

    print("\n-> Report saved: output/report.html")