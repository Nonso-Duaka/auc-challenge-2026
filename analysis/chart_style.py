"""
Shared chart styling for AUC Data Challenge 2026
Publication-quality plotly defaults
"""

# Color palette
TEAL = '#2A9D8F'
CORAL = '#E63946'
NAVY = '#1D3557'
AMBER = '#F4A261'
SLATE = '#457B9D'
MUTED = '#8D99AE'
LIGHT_BG = '#F8F9FA'

PALETTE_3 = [TEAL, AMBER, CORAL]        # US → LA → St. Helena (green-to-red)
PALETTE_3R = [CORAL, AMBER, TEAL]       # St. Helena → LA → US (red-to-green)
PALETTE_2 = [TEAL, CORAL]               # US vs St. Helena

def base_layout(title, width=950, height=520, b_margin=130, l_margin=60, r_margin=50):
    """Return a base layout dict with consistent styling."""
    return dict(
        template='plotly_white',
        width=width, height=height,
        margin=dict(l=l_margin, r=r_margin, t=110, b=b_margin),
        title=dict(
            text=title,
            font=dict(size=20, color=NAVY, family='Arial'),
            x=0.5, xanchor='center',
        ),
        plot_bgcolor=LIGHT_BG,
        paper_bgcolor='white',
        font=dict(family='Arial'),
    )

def source_annotation(text, y=-0.28):
    """Return a source citation annotation dict."""
    return dict(
        text=text,
        xref='paper', yref='paper',
        x=0.5, y=y,
        showarrow=False,
        font=dict(size=8, color=MUTED, family='Arial'),
        xanchor='center',
    )

def hbar_axes(x_title=None, x_suffix='', x_range=None):
    """Return x/y axis dicts for horizontal bar charts."""
    xaxis = dict(
        tickfont=dict(size=11, color=NAVY),
        gridcolor='rgba(0,0,0,0.04)',
        zeroline=False,
    )
    if x_title:
        xaxis['title'] = dict(text=x_title, font=dict(size=12, color=NAVY))
    if x_suffix:
        xaxis['ticksuffix'] = x_suffix
    if x_range:
        xaxis['range'] = x_range

    yaxis = dict(
        tickfont=dict(size=13, color=NAVY, family='Arial'),
    )
    return xaxis, yaxis

def grouped_legend():
    """Return a horizontal legend at the top."""
    return dict(
        orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5,
        font=dict(size=12, color=NAVY),
        bgcolor='rgba(0,0,0,0)',
    )
