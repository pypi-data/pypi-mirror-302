import plotly.graph_objects as go
import plotly.io as pio

pio.templates["humbl_dark"] = go.layout.Template(
    {
        "data": {
            "bar": [
                {
                    "error_x": {"color": "#f2f5fa"},
                    "error_y": {"color": "#f2f5fa"},
                    "marker": {
                        "line": {"color": "rgb(17,17,17)", "width": 0.5},
                        "pattern": {
                            "fillmode": "overlay",
                            "size": 10,
                            "solidity": 0.2,
                        },
                    },
                    "type": "bar",
                }
            ],
            "barpolar": [
                {
                    "marker": {
                        "line": {"color": "rgb(17,17,17)", "width": 0.5},
                        "pattern": {
                            "fillmode": "overlay",
                            "size": 10,
                            "solidity": 0.2,
                        },
                    },
                    "type": "barpolar",
                }
            ],
            "carpet": [
                {
                    "aaxis": {
                        "endlinecolor": "#A2B1C6",
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "minorgridcolor": "#506784",
                        "startlinecolor": "#A2B1C6",
                    },
                    "baxis": {
                        "endlinecolor": "#A2B1C6",
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "minorgridcolor": "#506784",
                        "startlinecolor": "#A2B1C6",
                    },
                    "type": "carpet",
                }
            ],
            "choropleth": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "type": "choropleth",
                }
            ],
            "contour": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "contour",
                }
            ],
            "contourcarpet": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "type": "contourcarpet",
                }
            ],
            "heatmap": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "heatmap",
                }
            ],
            "heatmapgl": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "heatmapgl",
                }
            ],
            "histogram": [
                {
                    "marker": {
                        "pattern": {
                            "fillmode": "overlay",
                            "size": 10,
                            "solidity": 0.2,
                        }
                    },
                    "type": "histogram",
                }
            ],
            "histogram2d": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "histogram2d",
                }
            ],
            "histogram2dcontour": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "histogram2dcontour",
                }
            ],
            "mesh3d": [
                {"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}
            ],
            "parcoords": [
                {
                    "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "parcoords",
                }
            ],
            "pie": [{"automargin": True, "type": "pie"}],
            "scatter": [
                {"marker": {"line": {"color": "#283442"}}, "type": "scatter"}
            ],
            "scatter3d": [
                {
                    "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatter3d",
                }
            ],
            "scattercarpet": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattercarpet",
                }
            ],
            "scattergeo": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattergeo",
                }
            ],
            "scattergl": [
                {"marker": {"line": {"color": "#283442"}}, "type": "scattergl"}
            ],
            "scattermapbox": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattermapbox",
                }
            ],
            "scatterpolar": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterpolar",
                }
            ],
            "scatterpolargl": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterpolargl",
                }
            ],
            "scatterternary": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterternary",
                }
            ],
            "surface": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "surface",
                }
            ],
            "table": [
                {
                    "cells": {
                        "fill": {"color": "#506784"},
                        "line": {"color": "rgb(17,17,17)"},
                    },
                    "header": {
                        "fill": {"color": "#2a3f5f"},
                        "line": {"color": "rgb(17,17,17)"},
                    },
                    "type": "table",
                }
            ],
        },
        "layout": {
            "legend": {
                "xanchor": "center",
                "x": 0.5,
                "y": -0.15,
                "orientation": "h",
                "traceorder": "normal",
                "font": {"family": "open-sans", "size": 12, "color": "white"},
                "bgcolor": "rgb(0,0,0,0)",
                "bordercolor": "rgb(63,70,139)",
                "borderwidth": 0.5,
            },
            "annotationdefaults": {
                "arrowcolor": "#f2f5fa",
                "arrowhead": 0,
                "arrowwidth": 1,
            },
            "autotypenumbers": "strict",
            "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
            "colorscale": {
                "diverging": [
                    [0, "#8e0152"],
                    [0.1, "#c51b7d"],
                    [0.2, "#de77ae"],
                    [0.3, "#f1b6da"],
                    [0.4, "#fde0ef"],
                    [0.5, "#f7f7f7"],
                    [0.6, "#e6f5d0"],
                    [0.7, "#b8e186"],
                    [0.8, "#7fbc41"],
                    [0.9, "#4d9221"],
                    [1, "#276419"],
                ],
                "sequential": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "sequentialminus": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
            },
            "colorway": [
                "#636efa",
                "#EF553B",
                "#00cc96",
                "#ab63fa",
                "#FFA15A",
                "#19d3f3",
                "#FF6692",
                "#B6E880",
                "#FF97FF",
                "#FECB52",
            ],
            "font": {"color": "white"},
            "geo": {
                "bgcolor": "rgb(17,17,17)",
                "lakecolor": "rgb(17,17,17)",
                "landcolor": "rgb(17,17,17)",
                "showlakes": True,
                "showland": True,
                "subunitcolor": "#506784",
            },
            "hoverlabel": {"align": "left"},
            "hovermode": "closest",
            "mapbox": {"style": "dark"},
            "paper_bgcolor": "rgb(0,0,0,0)",
            "plot_bgcolor": "rgb(0,0,0,0)",
            "polar": {
                "angularaxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
                "bgcolor": "rgb(17,17,17)",
                "radialaxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
            },
            "scene": {
                "xaxis": {
                    "backgroundcolor": "rgb(17,17,17)",
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
                "yaxis": {
                    "backgroundcolor": "rgb(17,17,17)",
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
                "zaxis": {
                    "backgroundcolor": "rgb(17,17,17)",
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
            },
            "shapedefaults": {"line": {"color": "#f2f5fa"}},
            "sliderdefaults": {
                "bgcolor": "#C8D4E3",
                "bordercolor": "rgb(17,17,17)",
                "borderwidth": 1,
                "tickwidth": 0,
            },
            "ternary": {
                "aaxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
                "baxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
                "bgcolor": "rgb(17,17,17)",
                "caxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
            },
            "title": {"x": 0.05},
            "updatemenudefaults": {"bgcolor": "#506784", "borderwidth": 0},
            "xaxis": {
                "automargin": True,
                "gridcolor": "#283442",
                "linecolor": "#506784",
                "ticks": "",
                "title": {"standoff": 15},
                "zerolinecolor": "#283442",
                "zerolinewidth": 2,
            },
            "yaxis": {
                "automargin": True,
                "gridcolor": "#283442",
                "linecolor": "#506784",
                "ticks": "",
                "title": {"standoff": 15},
                "zerolinecolor": "#283442",
                "zerolinewidth": 2,
                "side": "right",
            },
        },
    }
)

pio.templates["humbl_dark"].layout.annotations = [
    {
        "name": "draft watermark",
        "text": "humblDATA",
        "textangle": -25,
        "opacity": 0.1,
        "font": dict(color="black", size=90),
        "xref": "paper",
        "yref": "paper",
        "x": 0.5,
        "y": 0.5,
        "showarrow": False,
    }
]


pio.templates["humbl_light"] = go.layout.Template(
    {
        "data": {
            "bar": [
                {
                    "error_x": {"color": "#f2f5fa"},
                    "error_y": {"color": "#f2f5fa"},
                    "marker": {
                        "line": {"color": "rgb(17,17,17)", "width": 0.5},
                        "pattern": {
                            "fillmode": "overlay",
                            "size": 10,
                            "solidity": 0.2,
                        },
                    },
                    "type": "bar",
                }
            ],
            "barpolar": [
                {
                    "marker": {
                        "line": {"color": "rgb(17,17,17)", "width": 0.5},
                        "pattern": {
                            "fillmode": "overlay",
                            "size": 10,
                            "solidity": 0.2,
                        },
                    },
                    "type": "barpolar",
                }
            ],
            "carpet": [
                {
                    "aaxis": {
                        "endlinecolor": "#A2B1C6",
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "minorgridcolor": "#506784",
                        "startlinecolor": "#A2B1C6",
                    },
                    "baxis": {
                        "endlinecolor": "#A2B1C6",
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "minorgridcolor": "#506784",
                        "startlinecolor": "#A2B1C6",
                    },
                    "type": "carpet",
                }
            ],
            "choropleth": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "type": "choropleth",
                }
            ],
            "contour": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "contour",
                }
            ],
            "contourcarpet": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "type": "contourcarpet",
                }
            ],
            "heatmap": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "heatmap",
                }
            ],
            "heatmapgl": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "heatmapgl",
                }
            ],
            "histogram": [
                {
                    "marker": {
                        "pattern": {
                            "fillmode": "overlay",
                            "size": 10,
                            "solidity": 0.2,
                        }
                    },
                    "type": "histogram",
                }
            ],
            "histogram2d": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "histogram2d",
                }
            ],
            "histogram2dcontour": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "histogram2dcontour",
                }
            ],
            "mesh3d": [
                {"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}
            ],
            "parcoords": [
                {
                    "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "parcoords",
                }
            ],
            "pie": [{"automargin": True, "type": "pie"}],
            "scatter": [
                {"marker": {"line": {"color": "#283442"}}, "type": "scatter"}
            ],
            "scatter3d": [
                {
                    "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatter3d",
                }
            ],
            "scattercarpet": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattercarpet",
                }
            ],
            "scattergeo": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattergeo",
                }
            ],
            "scattergl": [
                {"marker": {"line": {"color": "#283442"}}, "type": "scattergl"}
            ],
            "scattermapbox": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattermapbox",
                }
            ],
            "scatterpolar": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterpolar",
                }
            ],
            "scatterpolargl": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterpolargl",
                }
            ],
            "scatterternary": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterternary",
                }
            ],
            "surface": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "surface",
                }
            ],
            "table": [
                {
                    "cells": {
                        "fill": {"color": "#506784"},
                        "line": {"color": "rgb(17,17,17)"},
                    },
                    "header": {
                        "fill": {"color": "#2a3f5f"},
                        "line": {"color": "rgb(17,17,17)"},
                    },
                    "type": "table",
                }
            ],
        },
        "layout": {
            "legend": {
                "xanchor": "center",
                "x": 0.5,
                "y": -0.15,
                "orientation": "h",
                "traceorder": "normal",
                "font": {
                    "family": "open-sans",
                    "size": 12,
                    "color": "rgb(17,19,34)",
                },
                "bgcolor": "rgb(255,255,255)",
                "bordercolor": "rgb(63,70,139)",
                "borderwidth": 0.5,
            },
            "annotationdefaults": {
                "arrowcolor": "#f2f5fa",
                "arrowhead": 0,
                "arrowwidth": 1,
            },
            "autotypenumbers": "strict",
            "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
            "colorscale": {
                "diverging": [
                    [0, "#8e0152"],
                    [0.1, "#c51b7d"],
                    [0.2, "#de77ae"],
                    [0.3, "#f1b6da"],
                    [0.4, "#fde0ef"],
                    [0.5, "#f7f7f7"],
                    [0.6, "#e6f5d0"],
                    [0.7, "#b8e186"],
                    [0.8, "#7fbc41"],
                    [0.9, "#4d9221"],
                    [1, "#276419"],
                ],
                "sequential": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "sequentialminus": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
            },
            "colorway": [
                "#636efa",
                "#EF553B",
                "#00cc96",
                "#ab63fa",
                "#FFA15A",
                "#19d3f3",
                "#FF6692",
                "#B6E880",
                "#FF97FF",
                "#FECB52",
            ],
            "font": {"color": "rgb(17,19,34)"},
            "geo": {
                "bgcolor": "rgb(17,17,17)",
                "lakecolor": "rgb(17,17,17)",
                "landcolor": "rgb(17,17,17)",
                "showlakes": True,
                "showland": True,
                "subunitcolor": "#506784",
            },
            "hoverlabel": {"align": "left"},
            "hovermode": "closest",
            "mapbox": {"style": "dark"},
            "paper_bgcolor": "rgb(0,0,0,0)",
            "plot_bgcolor": "rgb(0,0,0,0)",
            "polar": {
                "angularaxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
                "bgcolor": "rgb(17,17,17)",
                "radialaxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
            },
            "scene": {
                "xaxis": {
                    "backgroundcolor": "rgb(17,17,17)",
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
                "yaxis": {
                    "backgroundcolor": "rgb(17,17,17)",
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
                "zaxis": {
                    "backgroundcolor": "rgb(17,17,17)",
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
            },
            "shapedefaults": {"line": {"color": "#f2f5fa"}},
            "sliderdefaults": {
                "bgcolor": "#C8D4E3",
                "bordercolor": "rgb(17,17,17)",
                "borderwidth": 1,
                "tickwidth": 0,
            },
            "ternary": {
                "aaxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
                "baxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
                "bgcolor": "rgb(17,17,17)",
                "caxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
            },
            "title": {"x": 0.05},
            "updatemenudefaults": {"bgcolor": "#506784", "borderwidth": 0},
            "xaxis": {
                "automargin": True,
                "gridcolor": "#283442",
                "linecolor": "#506784",
                "ticks": "",
                "title": {"standoff": 15},
                "zerolinecolor": "#283442",
                "zerolinewidth": 2,
            },
            "yaxis": {
                "automargin": True,
                "gridcolor": "#283442",
                "linecolor": "#506784",
                "ticks": "",
                "title": {"standoff": 15},
                "zerolinecolor": "#283442",
                "zerolinewidth": 2,
                "side": "right",
            },
        },
    }
)
pio.templates["humbl_light"].layout.annotations = [
    {
        "name": "draft watermark",
        "text": "humblDATA",
        "textangle": -25,
        "opacity": 0.1,
        "font": dict(color="black", size=90),
        "xref": "paper",
        "yref": "paper",
        "x": 0.5,
        "y": 0.5,
        "showarrow": False,
    }
]
