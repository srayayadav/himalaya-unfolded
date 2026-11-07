"""Simple cartoon character kit (flat explainer style, original drawings).
Historical people are drawn as respectful, stylized characters identified by costume and labels,
not as realistic portraits.

character(x, y, s, look, t) -> SVG group. `t` (seconds) drives blinking, breathing and talking.
`talking=True` moves the mouth; `gesture` 0..1 raises the right arm.
"""
import math

SKIN = {"light": "#E8B98F", "mid": "#C98E62", "deep": "#9C6644"}

def _hat(kind, c1, c2):
    if kind == "shirpech":  # Rana-era plumed crown: jewelled cap + tall bird-of-paradise plumes
        return (f'<path d="M-62 -168 Q0 -215 62 -168 L56 -140 L-56 -140Z" fill="{c1}"/>'
                f'<path d="M-56 -150 L56 -150" stroke="{c2}" stroke-width="6"/>'
                + "".join(f'<circle cx="{x}" cy="-160" r="5" fill="#E8F1F5"/>' for x in (-36, -18, 0, 18, 36))
                + f'<path d="M0 -200 Q-10 -280 -70 -330 Q-20 -290 -6 -205Z" fill="#F4F1E8"/>'
                f'<path d="M4 -200 Q30 -290 90 -320 Q36 -280 12 -203Z" fill="#E9E2CE"/>'
                f'<path d="M2 -202 Q4 -300 20 -350 Q14 -290 8 -204Z" fill="#FFFFFF"/>'
                f'<circle cx="0" cy="-196" r="12" fill="#2E9E5B" stroke="{c2}" stroke-width="4"/>')
    if kind == "slouch":    # Gurkha slouch hat
        return (f'<ellipse cx="0" cy="-152" rx="95" ry="20" fill="{c1}"/>'
                f'<path d="M-52 -156 Q-50 -215 0 -218 Q50 -215 52 -156Z" fill="{c1}"/>'
                f'<path d="M-52 -168 L52 -168" stroke="{c2}" stroke-width="8"/>')
    if kind == "bicorne":   # 19th-century British officer
        return (f'<path d="M-95 -150 Q0 -240 95 -150 Q0 -175 -95 -150Z" fill="{c1}"/>'
                f'<circle cx="38" cy="-170" r="10" fill="{c2}"/>')
    if kind == "topi":      # Nepali dhaka-style topi
        return (f'<path d="M-58 -150 L-50 -195 Q0 -205 56 -190 L58 -150Z" fill="{c1}"/>'
                + "".join(f'<path d="M{x} -190 l10 12 l-10 12 l-10 -12Z" fill="{c2}"/>' for x in (-30, 0, 30)))
    return ""

def character(x, y, s=1.0, look=None, t=0.0, talking=False, gesture=0.0, flip=False, op=1.0):
    L = dict(skin="mid", coat="#7A1F2B", trim="#E2B44D", hat="topi", hat1="#2B2F4A", hat2="#E2B44D",
             mustache=True, sideburns=False, beard=False, sash=None, medals=0, sword=False)
    L.update(look or {})
    sk = SKIN.get(L["skin"], L["skin"])
    breathe = 1 + 0.012 * math.sin(t * 2.2)
    blink = 0.12 if (t % 3.7) < 0.12 else 1.0
    mouth = (6 + 7 * abs(math.sin(t * 13))) if talking else 3
    arm = -35 - 95 * gesture + (6 * math.sin(t * 3) if gesture > 0 else 0)
    f = -1 if flip else 1
    body = f'''
<g transform="scale(1 {breathe:.4f})">
  <path d="M-80 40 Q-90 -40 -60 -70 L60 -70 Q90 -40 80 40 L70 190 L-70 190Z" fill="{L['coat']}"/>
  <path d="M0 -70 L0 190" stroke="{L['trim']}" stroke-width="7"/>
  {''.join(f'<circle cx="12" cy="{-40 + i*36}" r="6" fill="{L["trim"]}"/>' for i in range(6))}
  <path d="M-60 -70 Q0 -40 60 -70" fill="none" stroke="{L['trim']}" stroke-width="8"/>
  {f'<path d="M-70 -55 L70 120" stroke="{L["sash"]}" stroke-width="22" opacity="0.95"/>' if L['sash'] else ''}
  {''.join(f'<circle cx="{-45 + i*16}" cy="-20" r="7" fill="#E2B44D" stroke="#7A5A1A" stroke-width="2"/>' for i in range(L['medals']))}
  <path d="M-62 190 L-58 290 L-18 290 L-10 190Z M10 190 L18 290 L58 290 L62 190Z" fill="#E9E4D8"/>
  <path d="M-64 285 L-12 285 L-10 305 L-70 305Z M12 285 L64 285 L70 305 L10 305Z" fill="#2A1E18"/>
  {f'<path d="M-70 120 Q-120 200 -150 230" stroke="#C9CFD6" stroke-width="10" fill="none"/><circle cx="-70" cy="118" r="10" fill="#E2B44D"/>' if L['sword'] else ''}
</g>
<g transform="translate(-72 -55) rotate(18)"><rect x="-18" y="0" width="36" height="140" rx="18" fill="{L['coat']}"/><circle cx="0" cy="145" r="17" fill="{sk}"/></g>
<g transform="translate(72 -55) rotate({arm:.1f})"><rect x="-18" y="0" width="36" height="140" rx="18" fill="{L['coat']}"/><circle cx="0" cy="145" r="17" fill="{sk}"/></g>
<rect x="-22" y="-100" width="44" height="40" fill="{sk}"/>
<ellipse cx="0" cy="-130" rx="56" ry="62" fill="{sk}"/>
<ellipse cx="-56" cy="-125" rx="10" ry="16" fill="{sk}"/><ellipse cx="56" cy="-125" rx="10" ry="16" fill="{sk}"/>
<path d="M-30 -150 q10 -8 20 0 M10 -150 q10 -8 20 0" stroke="#1E1A18" stroke-width="5" fill="none"/>
<ellipse cx="-20" cy="-135" rx="7" ry="{8*blink:.1f}" fill="#1E1A18"/><ellipse cx="20" cy="-135" rx="7" ry="{8*blink:.1f}" fill="#1E1A18"/>
<path d="M0 -128 q6 14 -3 18" stroke="#8A5A3C" stroke-width="4" fill="none"/>
{f'<path d="M-40 -96 Q-20 -112 0 -104 Q20 -112 40 -96 Q22 -100 0 -96 Q-22 -100 -40 -96Z" fill="#1E1A18"/>' if L['mustache'] else ''}
{f'<path d="M-54 -150 Q-62 -110 -44 -92 L-36 -100 Q-46 -120 -44 -150Z M54 -150 Q62 -110 44 -92 L36 -100 Q46 -120 44 -150Z" fill="#1E1A18"/>' if L['sideburns'] else ''}
{f'<path d="M-50 -110 Q-40 -50 0 -42 Q40 -50 50 -110 Q30 -80 0 -78 Q-30 -80 -50 -110Z" fill="#2A2420"/>' if L['beard'] else ''}
<ellipse cx="0" cy="-88" rx="12" ry="{mouth/2:.1f}" fill="#5A1E1E"/>
{_hat(L['hat'], L['hat1'], L['hat2'])}'''
    return f'<g transform="translate({x:.0f} {y:.0f}) scale({f*s:.3f} {s:.3f})" opacity="{op:.2f}">{body}</g>'

# Ready-made looks for recurring people (stylized; identified by costume + on-screen label)
JUNG_BAHADUR = dict(skin="mid", coat="#1F3A5F", trim="#E2B44D", hat="shirpech", hat1="#1E2B3C", hat2="#E2B44D",
                    mustache=True, sideburns=True, sash="#C8553D", medals=4, sword=True)
PRITHVI_NARAYAN = dict(skin="mid", coat="#F2EDE2", trim="#B8862B", hat="topi", hat1="#5A2A2A", hat2="#E2B44D",
                       mustache=True, sash="#7A1F2B", sword=True)
GURKHA = dict(skin="mid", coat="#3E5A3A", trim="#C9B27A", hat="slouch", hat1="#4A5A3A", hat2="#2A2A2A",
              mustache=False, sword=False)
BRITISH_OFFICER = dict(skin="light", coat="#B3261E", trim="#F2D27A", hat="bicorne", hat1="#1E1A18", hat2="#F2D27A",
                       mustache=True, sideburns=True, medals=2, sword=True)
