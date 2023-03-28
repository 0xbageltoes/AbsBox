import matplotlib.pyplot as plt
from matplotlib import font_manager
from absbox.local.util import guess_locale,aggStmtByDate,consolStmtByDate
from pyspecter import query, S
from itertools import reduce
import numpy as np


dmap = {
    "cn":{
        "bond":"债券","scenario":"场景"
    },
    "en":{
        "bond":"bond","scenario":"scenario"
    }
}


def init_plot_fonts():
    define_list = ['Source Han Serif CN','Microsoft Yahei','STXihei']
    support_list = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    font_p = font_manager.FontProperties()
    try:
        for sl in support_list:
            f = font_manager.get_font(sl)
            if f.family_name in set(define_list):
                font_p.set_family(f.family_name)
                font_p.set_size(14)
                return font_p
    except RuntimeError as e:
        logging.error("中文字体载入失败")
        return None

font_p = init_plot_fonts()

def plot_bond(rs, bnd, flow='本息合计'):
    """Plot bonds across scenarios"""
    plt.figure(figsize=(12,8))
    _alpha =  0.8
    locale = guess_locale(list(rs.values())[0])
    for idx,s in enumerate(rs):
        plt.step(s['bonds'][bnd].index,s['bonds'][bnd][[flow]], alpha=_alpha, linewidth=5, label=f"{dmap[locale]['scenario']}-{idx}")

    plt.legend(loc='upper left', prop=font_p)
    plt.title(f"{len(rs)} {dmap[locale]['scenario']} {dmap[locale]['bond']}:{bnd} - {flow}", fontproperties=font_p)

    plt.grid(True)
    plt.axis('tight')
    plt.xticks(rotation=30)

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:.0f}(w)'.format(x/10000) for x in current_values])
    return plt

def plot_bonds(r, bnds:list, flow='本息合计'):
    "Plot bond flows with in a single run"

    locale = guess_locale(r)
    plt.figure(figsize=(12,8))
    _alpha =  0.8

    for b in bnds:
        b_flow = r['bonds'][b]
        plt.step(b_flow.index,b_flow[[flow]], alpha=_alpha, linewidth=5, label=f"{dmap[locale]['bond']}-{b}")

    plt.legend(loc='upper left', prop=font_p)
    bnd_title = ','.join(bnds)
    plt.title(f"{dmap[locale]['bond']}:{bnd_title} - {flow}", fontproperties=font_p)

    plt.grid(True)
    plt.axis('tight')
    plt.xticks(rotation=30)

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:.0f}(w)'.format(x/10000) for x in current_values])
    return plt

def plot_by_scenario(rs, flowtype, flowpath):
    "Plot with multiple scenario"
    plt.figure(figsize=(12,8))
    scenario_names = rs.keys()
    dflows = [query(rs,[s]+flowpath) for s in scenario_names]
    _alpha =  0.8

    x_labels = reduce(lambda acc,x:acc.union(x) ,[ _.index for _ in dflows ]).unique()
    x = np.arange(len(x_labels))
    width = 1 
    step_length = width / (len(scenario_names)+1)

    for (idx,(scen,dflow)) in enumerate(zip(scenario_names,dflows)):
        if flowtype=="balance":
            cb = consolStmtByDate(dflow)
            plt.step(cb.index, cb, alpha=_alpha, linewidth=5, label=f"{scen}")
        elif flowtype=="amount":
            cb = aggStmtByDate(dflow)
            _bar = plt.bar(x+idx*step_length,cb,width=step_length,label=scen)
        else:
            plt.plot(dflow.index,dflow, alpha=_alpha, linewidth=5, label=f"{scen}")

    plt.legend(scenario_names,loc='upper right', prop=font_p)
    plt.grid(True)
    plt.axis('tight')
    plt.xticks(ticks=x,labels=x_labels,rotation=30)

